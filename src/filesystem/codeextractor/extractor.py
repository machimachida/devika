from enum import Enum
from .java_extractor import JavaExtractor


class SupportedLanguages(Enum):
    JAVA = 'java'


class Extractor:
    def __init__(self, language: str):
        """
        Constructor for Extractor class.
        
        Args:
            language (str): Language of the code.

        Returns:
            None
        
        Raises:
            ValueError: If the language is not supported.
        """

        language = SupportedLanguages[language]
        extractors = {
            SupportedLanguages.JAVA: JavaExtractor
        }
        self.extractor = extractors[language]

    def extract_method_names(self, file_content: str) -> list[str]:
        """
        Extract method names from the code.

        Args:
            file_content (str): Content of the file.

        Returns:
            list[str]: List of method names.
        """
        return self.extractor.extract_method_names(file_content)

    def extract_methods(self, file_content: str, methods: list[str]) -> str:
        """
        Extract methods from the code.

        Args:
            file_content (str): Content of the file.
            methods (list[str]): List of method names.

        Returns:
            str: Extracted methods.
        """
        return self.extractor.extract_methods(file_content, methods)
