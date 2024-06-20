from jinja2 import Environment, BaseLoader
import json
from pathlib import Path

from src.config import Config
from src.filesystem import ReadCode
from src.llm import LLM
from src.logger import Logger
from src.services.utils import retry_wrapper


class ReferenceCodeFinder:
    def __init__(self, base_model: str):
        config = Config()
        self.project_dir = config.get_projects_dir()
        self.logger = Logger()
        self.llm = LLM(model_id=base_model)
        parent = Path(__file__).resolve().parent
        with open(parent.joinpath("reference.jinja2"), 'r') as file:
            self.prompt_template = file.read().strip()

    def render(self, instruction: str, classes: list[str], methods: list[str]) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.prompt_template)
        return template.render(
            instruction=instruction,
            classes=classes,
            methods=methods,
        )

    def validate_response(self, response: str) -> tuple[list[str], list[str]]:
        """
        以下の形式でレスポンスが返却されていることを確認し、classesとmethodsを返却する

        ```
        {
          "classes": [
            "com.example.task.Task",
          ],
          "methods": [
            "com.example.task.TaskService#createTask",
            "com.example.user.UserService#createUser"
          ]
        }
        ```
        """

        try:
            # \nやスペースの他に、```がJSONの前後にある場合があるので、削除する
            stripped = response.strip().replace('```', '')
            response = json.loads(stripped)
            return response["classes"], response["methods"]
        except json.JSONDecodeError:
            self.logger.error(f'Failed to decode response as JSON: {response}')
            return [], []

    @retry_wrapper
    def execute(self, instruction: str, project_name: str) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
        classes, methods = ReadCode(project_name).get_class_method_names()
        prompt = self.render(
            instruction=instruction,
            classes=list(classes.keys()),
            methods=list(methods.keys())
        )
        response = self.llm.inference(prompt, project_name)

        extracted_class_names, extracted_method_names = self.validate_response(response)
        return (
            self.extract_file_paths_and_names(extracted_class_names, classes),
            self.extract_file_paths_and_names(extracted_method_names, methods)
        )

    @staticmethod
    def extract_file_paths_and_names(
            names_to_extract: list[str], name_to_path_mapping: dict[str, str]
    ) -> dict[str, list[str]]:
        """
        This static method is used to extract file paths and names from a given list
        of names and a mapping of names to paths.

        Parameters:
        names_to_extract (list[str]): A list of names that need to be extracted.
        name_to_path_mapping (dict[str, str]): A dictionary mapping names to file paths.

        Returns:
        dict[str, list[str]]: A dictionary where the keys are the file paths and
        the values are lists of names that were found in the corresponding file path.

        """
        extracted_file_paths: dict[str, list[str]] = {}
        for name in names_to_extract:
            file_path = name_to_path_mapping.get(name)
            # LLMがクラスやメソッドの名前を間違えて返すケースがあり、存在しないキーアクセスがありうるので、その場合は無視する
            if file_path is None:
                continue
            if file_path not in extracted_file_paths:
                extracted_file_paths[file_path] = []
            extracted_file_paths[file_path].append(name)
        return extracted_file_paths
