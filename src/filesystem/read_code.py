import os
from pathlib import Path

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
        self.extractor = Extractor('java')

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

    def get_class_method_names(self) -> tuple[dict[str, str], dict[str, str]]:
        classes: dict[str, str] = {}
        methods: dict[str, str] = {}

        for root, _dirs, files in os.walk(self.directory_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                        class_names, method_names = self.extractor.extract_class_method_names(content)
                        for class_name in class_names:
                            classes[class_name] = file_path
                        for method_name in method_names:
                            methods[method_name] = file_path
                except Exception as e:
                    print(e)
                    pass

        return classes, methods

    def set_classes_to_markdown(self, classes: dict[str, list[str]]) -> str:
        markdown = ""
        for file_path in classes.keys():
            with open(file_path, 'r', encoding='utf-8') as file_content:
                content = file_content.read()

                path_from_app_root_directory = Path(file_path)
                directory_path = Path(self.directory_path)
                project_path = path_from_app_root_directory.relative_to(directory_path)

                markdown += f"### {project_path}:\n\n"
                markdown += f"```\n{content}\n```\n\n"
                markdown += "---\n\n"
        return markdown

    def set_methods_to_markdown(self, methods: dict[str, list[str]]) -> str:
        markdown = ""
        for file_path, method_names in methods.items():
            with open(file_path, 'r', encoding='utf-8') as file_content:
                content = file_content.read()
                extracted = self.extractor.extract_methods(content, method_names)

                path_from_app_root_directory = Path(file_path)
                directory_path = Path(self.directory_path)
                project_path = path_from_app_root_directory.relative_to(directory_path)

                markdown += f"### {project_path}:\n\n"
                markdown += f"```\n{extracted}\n```\n\n"
                markdown += "---\n\n"
        return markdown

    def get_project_directory_tree(self) -> str:
        """
        TODO: 仮実装なのでsrcディレクトリのみを取得する
        """

        src_path = Path(self.directory_path) / "src"
        return get_tree_structure(str(src_path))


def get_tree_structure(target_path: str, indent: str = "") -> str:
    result = ""
    items = os.listdir(target_path)
    for i, item in enumerate(items):
        result += "└── " + item + "\n"
        item_path = os.path.join(target_path, item)
        if os.path.isdir(item_path):
            # If it's the last item, adjust the indentation for child items
            if i == len(items) - 1:
                new_indent = indent + "    "
            else:
                new_indent = indent + "│   "
            # Recurse into the directory
            result += get_tree_structure(item_path, new_indent)

    return result
