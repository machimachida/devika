from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream
from .grammer.JavaLexer import JavaLexer
from .grammer.JavaParser import JavaParser
from .grammer.JavaParserListener import JavaParserListener


class JavaExtractor:
    def extract(self, file_content: str, methods: list[str]) -> str:  # dict[str, str]:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = Listener()
        walker.walk(listener, parser.compilationUnit())
        return listener.to_string()


class Listener(JavaParserListener):
    def __init__(self):
        self.contents: dict[int, str] = {}

    def to_string(self) -> str:
        """
        self.contentsの内容をキーの昇順に並べ替え、文字列として結合する。
        """
        return "".join([self.contents[key] for key in sorted(self.contents.keys())])

    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        child_count = int(ctx.getChildCount())
        package_line = ''
        for i in range(child_count):
            if i == child_count - 1:  # 最後のgetText()で得られる文字列は';'なので、その後ろに改行を追加する
                package_line += ctx.getChild(i).getText() + '\n\n'
                continue
            if i != 0:
                package_line += ' '
            package_line += ctx.getChild(i).getText()

        self.contents[ctx.start.line] = package_line

    def enterImportDeclaration(self, ctx: JavaParser.ImportDeclarationContext):
        child_count = int(ctx.getChildCount())
        import_line = ''
        for i in range(child_count):
            if i == child_count - 1:  # 最後のgetText()で得られる文字列は';'なので、その後ろに改行を追加する
                import_line += ctx.getChild(i).getText() + '\n'
                continue
            if i != 0:
                import_line += ' '
            import_line += ctx.getChild(i).getText()

        self.contents[ctx.start.line] = import_line

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        class_lines = ''
        # get Annotation and AccessModifier
        parent = ctx.parentCtx
        parent_child_count = parent.getChildCount()
        for i in range(parent_child_count):  # 最後のchildはクラスなので、ここでは含めない
            if parent.getChild(i) == ctx:
                class_line = parent.getChild(i - 1).getText() + ' ' + ctx.getText() + ' {\n'
                self.contents[ctx.start.line] = class_line

        class_line = ctx.getText() + ' {\n'
        self.contents[ctx.start.line] = class_line


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
