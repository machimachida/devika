import os

from src.config import Config
from src.filesystem.codeextractor.extractor import Extractor

"""
TODO: Replace this with `code2prompt` - https://github.com/mufeedvh/code2prompt
"""


class ReadCode:
    def __init__(self, project_name: str):
        config = Config()
        project_path = config.get_projects_dir()
        self.directory_path = os.path.join(project_path, project_name.lower().replace(" ", "-"))

    def read_directory(self):
        files_list = []
        for root, _dirs, files in os.walk(self.directory_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as file_content:
                        files_list.append({"filename": file_path, "code": file_content.read()})
                except:
                    pass

        return files_list

    def code_set_to_markdown(self):
        code_set = self.read_directory()
        markdown = ""
        for code in code_set:
            markdown += f"### {code['filename']}:\n\n"
            markdown += f"```\n{code['code']}\n```\n\n"
            markdown += "---\n\n"
        return markdown

    def get_methods_names(self) -> dict[str, str]:
        method_dict: dict[str, str] = {}

        extractor = Extractor('java')
        for root, _dirs, files in os.walk(self.directory_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                        method_names = extractor.extract_method_names(content)
                        for method_name in method_names:
                            method_dict[method_name] = file_path
                except Exception as e:
                    print(e)
                    pass

        return method_dict
