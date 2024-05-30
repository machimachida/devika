from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

from src.filesystem.codeextractor.grammer import JavaLexer, JavaParser
from src.filesystem.codeextractor.listener import MethodExtractListener, NameListener


class JavaExtractor:
    @staticmethod
    def extract_class_method_names(file_content: str) -> tuple[list[str], list[str]]:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = NameListener()
        walker.walk(listener, parser.compilationUnit())
        return listener.get_class_method_names()

    @staticmethod
    def extract_methods(file_content: str, methods: list[str]) -> str:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = MethodExtractListener(file_content, methods)
        walker.walk(listener, parser.compilationUnit())
        return listener.get_methods()
