from src.filesystem.codeextractor.grammer import JavaParser, JavaParserListener
from src.logger import Logger


class MethodExtractListener(JavaParserListener):
    def __init__(self, original: str, target_methods: list[str]):
        self.original: str = original
        self.target_methods: list[str] = target_methods
        # ClassBodyDeclarationContextはアクセス修飾子やメソッド名などを含むメンバの情報を持つ
        self.removing_methods: list[JavaParser.ClassBodyDeclarationContext] = []
        self.logger = Logger()

    def get_methods(self) -> str:
        lines = self.original.split('\n')

        # 削除予定のメソッドのリストを開始行降順にソート
        sorted_removing_methods = sorted(self.removing_methods, key=lambda x: x.start.line, reverse=True)

        # 削除予定のメソッドをoriginal文字列から削除
        for method in sorted_removing_methods:
            start = method.start.line
            stop = method.stop.line
            del lines[start - 1:stop]

            # 削除したメソッドの前の行に空行やコメントがある場合は、それも削除
            while start > 1:
                stripped = lines[start - 2].strip()

                if (stripped == '' or  # empty line
                        stripped.startswith('//') or  # inline comment
                        stripped.startswith('*') or  # javadoc
                        stripped.startswith('/*')):  # javadoc
                    del lines[start - 2]
                    start -= 1
                else:
                    break

        return '\n'.join(lines)

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        class_internal = ctx.getChild(-1)
        if type(class_internal) is not JavaParser.ClassBodyContext:
            self.logger.error('unexpected error: class_internal is not ClassBodyContext')
            return

        for child in list(class_internal.getChildren()):
            if type(child) is not JavaParser.ClassBodyDeclarationContext:
                continue
            member = child.getChild(-1)
            if type(member) is not JavaParser.MemberDeclarationContext:
                continue
            declared_context = member.getChild(0)
            if type(declared_context) is not JavaParser.MethodDeclarationContext:
                continue
            method_name = declared_context.getChild(1).getText()

            if method_name not in self.target_methods:
                self.removing_methods.append(child)
