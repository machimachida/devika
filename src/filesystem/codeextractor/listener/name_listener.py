from src.filesystem.codeextractor.grammer import JavaParser, JavaParserListener


class NameListener(JavaParserListener):
    """
    A listener class that extracts information about class and method names from a Java file.

    Attributes:
    - current_package_name (str): The name of the current package.
    - current_class_name (str): The name of the current class in the format 'package_name.class_name'.
    - is_found_method_in_class (bool): Indicates whether a method has been found in the class.
    - class_names_have_no_method (list[str]): A list of class names that have no methods. The format is 'package_name.class_name'.
    - method_names (list[str]): A list of method names. The format is 'package_name.class_name#method_name'.
    """

    def __init__(self):
        """
        Initializes a new instance of the NameListener class.
        """
        self.current_package_name: str = ''
        self.current_class_name: str = ''
        self.class_names: list[str] = []
        self.method_names: list[str] = []

    def get_class_method_names(self) -> tuple[list[str], list[str]]:
        """
        Returns the class names that have no methods and the list of method names.

        Returns:
        - class_names_have_no_method (list[str]): A list of class names that have no methods. The format is 'package_name.class_name'.
        - method_names (list[str]): A list of method names. The format is 'package_name.class_name#method_name'.
        """
        return self.class_names, self.method_names

    def enterPackageDeclaration(self, ctx: JavaParser.PackageDeclarationContext):
        """
        Called when entering a package declaration.

        Args:
        - ctx (JavaParser.PackageDeclarationContext): The context of the package declaration.
        """
        self.current_package_name = ctx.qualifiedName().getText()

    def enterClassDeclaration(self, ctx: JavaParser.ClassDeclarationContext):
        """
        Called when entering a class declaration.

        Args:
        - ctx (JavaParser.ClassDeclarationContext): The context of the class declaration.
        """
        self.current_class_name = self.current_package_name + '.' + ctx.getChild(1).getText()
        self.class_names.append(self.current_class_name)

    def enterMethodDeclaration(self, ctx: JavaParser.MethodDeclarationContext):
        """
        Called when entering a method declaration.

        Args:
        - ctx (JavaParser.MethodDeclarationContext): The context of the method declaration.
        """
        method_name = ctx.getChild(1).getText()
        self.method_names.append(self.current_class_name + '#' + method_name)
