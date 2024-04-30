from src.filesystem.codeextractor.grammer import JavaParser, JavaParserListener


class MethodNameListener(JavaParserListener):
    def __init__(self):
        self.package_name: str = ''
        self.class_name: str = ''
        self.method_names: list[str] = []

    def get_method_names(self) -> list[str]:
        return [
            self.package_name + '.' +
            self.class_name + '#' + method_name
            for method_name in self.method_names
        ]

    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        self.package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        self.class_name = ctx.getChild(1).getText()
        self.method_names = []

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        method_name = ctx.getChild(1).getText()
        self.method_names.append(method_name)
