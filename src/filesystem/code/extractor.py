from enum import Enum


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

        self.language = SupportedLanguages[language]

    def extract_code(self, file_content: str, methods: list[str]) -> dict[str, str]:
        return {'fileName': '', 'code': ''}
