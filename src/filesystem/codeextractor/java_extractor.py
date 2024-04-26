from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream
from .grammer.JavaLexer import JavaLexer
from .grammer.JavaParser import JavaParser
from .grammer.JavaParserListener import JavaParserListener


class JavaExtractor:
    def extract(self, file_content: str, methods: list[str]) -> str:  # dict[str, str]:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = Listener(['existAll'])
        walker.walk(listener, parser.compilationUnit())
        return listener.to_string()


class Listener(JavaParserListener):
    def __init__(self, target_methods: list[str]):
        self.contents: dict[int, str] = {}
        self.internal_methods: list[str] = []
        self.target_methods: list[str] = target_methods

    def to_string(self) -> str:
        """
        self.contentsの内容をキーの昇順に並べ替え、文字列として結合する。
        """
        return ''.join([self.contents[key] for key in sorted(self.contents.keys())])

    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        children = list(ctx.getChildren())
        child_count = len(children)

        package_line = ' '.join(child.getText() for child in children[:child_count-1])
        # 最後のgetText()で得られる文字列は';'なので、その後ろに改行を追加する
        package_line += ctx.getChild(child_count - 1).getText() + '\n\n'

        self.contents[ctx.start.line] = package_line

    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        children = list(ctx.getChildren())
        child_count = len(children)

        import_line = ' '.join(child.getText() for child in children[:child_count-1])
        # 最後のgetText()で得られる文字列は';'なので、その後ろに改行を追加する
        import_line += ctx.getChild(child_count - 1).getText() + '\n'

        self.contents[ctx.start.line] = import_line

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.getChild(1).getText()
        self.internal_methods.append(method_name)

    def exitClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        class_lines = '\n'  # classの前に空行を入れる。enterImportDeclarationでimportの終了が検知できないため、このタイミングで空行を入れる
        # get Annotation and AccessModifier
        parent = ctx.parentCtx
        parent_child_count = parent.getChildCount()
        for i in range(parent_child_count - 1):  # 最後のchildはparentの子要素であるctxなので、ここでは含めない
            annotation_or_access_modifier = parent.getChild(i).getText()
            if annotation_or_access_modifier[0] == '@':  # アノテーションの場合
                class_lines += annotation_or_access_modifier + '\n'
            else:  # アクセス修飾子の場合
                class_lines += annotation_or_access_modifier + ' '

        # クラスの宣言文を取得する
        children = list(ctx.getChildren())
        class_declaration = ' '.join(child.getText() for child in children[:len(children)-1])
        class_lines += class_declaration + ' '  # 後に続く'{'の前にスペースを入れるため、ここでスペースを入れる

        # クラスの内部の要素を取得する
        class_internal = ctx.getChild(len(children) - 1)
        # 最初の要素は'{'、最後の要素は'}'なので、それらを除いた要素を取得する
        class_internal_children = list(class_internal.getChildren())
        members = class_internal_children[1:len(class_internal_children)-1]

        members_lines = ''
        methods: dict[str, JavaParser.MethodDeclarationContext] = {}
        extracted_members: dict[int, object] = {}
        for member in members:
            # メンバの最後の要素がアクセス修飾子やアノテーションでない部分
            main_part = member.getChild(-1)
            declared_context = main_part.getChild(0)

            if type(declared_context) is JavaParser.MethodDeclarationContext:
                # メソッドの場合は一旦すべてdictに格納し、後から必要かどうかを判断する
                for context in list(declared_context.getChildren()):
                    if type(context) is JavaParser.IdentifierContext:
                        methods[context.getText()] = declared_context
            else:
                # メソッド以外の場合は一旦extract_membersに格納し、後から一つの文字列にまとめる
                extracted_members[member.start.line] = member

        # 必要なメソッドのみ抽出する
        for target_method in self.target_methods:
            if target_method not in methods:
                continue

            target = methods[target_method]
            extracted_members[target.start.line] = target

            # 抽出対象のメソッドが同じクラスの別のメソッドを呼び出している場合、それらも抽出する
            for internal_method in self.internal_methods:
                if internal_method is target_method:
                    continue

                if 'self.' + internal_method in target.getText():
                    extracted_members[methods[internal_method].start.line] = methods[internal_method]

        # extracted_membersを行番号の昇順に並べ替え、文字列に変換する
        for key in sorted(extracted_members.keys()):
            member = extracted_members[key]
            members_lines += member.getText() + '\n'

        class_lines += '{\n' + members_lines + '}\n'

        self.contents[ctx.start.line] = class_lines + '\n'


class BasicInfoListener(JavaParserListener):
    def __init__(self):
        self.call_methods = []
        self.ast_info = {
            'packageName': '',
            'className': '',
            'implements': [],
            'extends': '',
            'imports': [],
            'fields': [],
            'methods': []
        }

    def enterClassOrInterfaceModifier(self, ctx:JavaParser.CompilationUnitContext):
        print("a")

    def exitClassOrInterfaceModifier(self, ctx:JavaParser.CompilationUnitContext):
        print("a")

    # ★ポイント５
    # Enter a parse tree produced by JavaParser#packageDeclaration.
    def enterPackageDeclaration(self, ctx:JavaParser.PackageDeclarationContext):
        self.ast_info['packageName'] = ctx.qualifiedName().getText()

    # Enter a parse tree produced by JavaParser#importDeclaration.
    def enterImportDeclaration(self, ctx:JavaParser.ImportDeclarationContext):
        import_class = ctx.qualifiedName().getText()
        self.ast_info['imports'].append(import_class)

    # Enter a parse tree produced by JavaParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):

        print("{0} {1} {2}".format(ctx.start.line, ctx.start.column, ctx.getText()))
        self.call_methods = []

    # Exit a parse tree produced by JavaParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:JavaParser.MethodDeclarationContext):

        # ★ポイント６
        c1 = ctx.getChild(0).getText()  # ---> return type
        c2 = ctx.getChild(1).getText()  # ---> method name
        # c3 = ctx.getChild(2).getText()  # ---> params
        params = self.parse_method_params_block(ctx.getChild(2))

        method_info = {
            'returnType': c1,
            'methodName': c2,
            'params': params,
            'callMethods': self.call_methods
        }
        self.ast_info['methods'].append(method_info)

    # Enter a parse tree produced by JavaParser#methodCall.
    def enterMethodCall(self, ctx:JavaParser.MethodCallContext):
        # ★ポイント７
        line_number = str(ctx.start.line)
        column_number = str(ctx.start.column)
        self.call_methods.append(line_number + ' ' + column_number + ' ' + ctx.parentCtx.getText())

    # Enter a parse tree produced by JavaParser#classDeclaration.
    def enterClassDeclaration(self, ctx:JavaParser.ClassDeclarationContext):
        child_count = int(ctx.getChildCount())
        if child_count == 7:
            # class Foo extends Bar implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> extends
            c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name
            # c5 = ctx.getChild(4)  # ---> implements
            # c7 = ctx.getChild(6)  # ---> method body
            self.ast_info['className'] = c2
            self.ast_info['implements'] = self.parse_implements_block(ctx.getChild(5))
            self.ast_info['extends'] = c4
        elif child_count == 5:
            # class Foo extends Bar
            # or
            # class Foo implements Hoge
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            c3 = ctx.getChild(2).getText()  # ---> extends or implements

            # c5 = ctx.getChild(4)  # ---> method body
            self.ast_info['className'] = c2
            if c3 == 'implements':
                self.ast_info['implements'] = self.parse_implements_block(ctx.getChild(3))
            elif c3 == 'extends':
                c4 = ctx.getChild(3).getChild(0).getText()  # ---> extends class name or implements class name
                self.ast_info['extends'] = c4
        elif child_count == 3:
            # class Foo
            # c1 = ctx.getChild(0)  # ---> class
            c2 = ctx.getChild(1).getText()  # ---> class name
            # c3 = ctx.getChild(2)  # ---> method body
            self.ast_info['className'] = c2

    # Enter a parse tree produced by JavaParser#fieldDeclaration.
    def enterFieldDeclaration(self, ctx:JavaParser.FieldDeclarationContext):
        field = {
            'fieldType': ctx.getChild(0).getText(),
            'fieldDefinition': ctx.getChild(1).getText()
        }
        self.ast_info['fields'].append(field)

    def parse_implements_block(self, ctx):
        implements_child_count = int(ctx.getChildCount())
        result = []
        if implements_child_count == 1:
            impl_class = ctx.getChild(0).getText()
            result.append(impl_class)
        elif implements_child_count > 1:
            for i in range(implements_child_count):
                if i % 2 == 0:
                    impl_class = ctx.getChild(i).getText()
                    result.append(impl_class)
        return result

    def parse_method_params_block(self, ctx):
        params_exist_check = int(ctx.getChildCount())
        result = []
        # () ---> 2
        # (Foo foo) ---> 3
        # (Foo foo, Bar bar) ---> 3
        # (Foo foo, Bar bar, int count) ---> 3
        if params_exist_check == 3:
            params_child_count = int(ctx.getChild(1).getChildCount())
            if params_child_count == 1:
                param_type = ctx.getChild(1).getChild(0).getChild(0).getText()
                param_name = ctx.getChild(1).getChild(0).getChild(1).getText()
                param_info = {
                    'paramType': param_type,
                    'paramName': param_name
                }
                result.append(param_info)
            elif params_child_count > 1:
                for i in range(params_child_count):
                    if i % 2 == 0:
                        param_type = ctx.getChild(1).getChild(i).getChild(0).getText()
                        param_name = ctx.getChild(1).getChild(i).getChild(1).getText()
                        param_info = {
                            'paramType': param_type,
                            'paramName': param_name
                        }
                        result.append(param_info)
        return result
