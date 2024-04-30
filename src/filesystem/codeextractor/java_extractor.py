from antlr4 import CommonTokenStream, ParseTreeWalker, InputStream

from src.filesystem.codeextractor.grammer import JavaLexer, JavaParser
from src.filesystem.codeextractor.listener import MethodExtractListener, MethodNameListener


class JavaExtractor:
    @staticmethod
    def extract_method_names(file_content: str) -> list[str]:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = MethodNameListener()
        walker.walk(listener, parser.compilationUnit())
        return listener.get_method_names()

    @staticmethod
    def extract_methods(file_content: str, methods: list[str]) -> str:
        parser = JavaParser(CommonTokenStream(JavaLexer(InputStream(file_content))))
        walker = ParseTreeWalker()
        listener = MethodExtractListener(file_content, methods)
        walker.walk(listener, parser.compilationUnit())
        return listener.get_methods()
