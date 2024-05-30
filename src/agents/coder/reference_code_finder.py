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
    def execute(self, instruction: str, project_name: str) -> tuple[list[str], list[str]]:
        classes, methods = ReadCode(project_name).get_class_method_names()
        class_names: list[str] = list(classes.keys())
        method_names: list[str] = list(methods.keys())
        prompt = self.render(instruction=instruction, classes=class_names, methods=method_names)
        response = self.llm.inference(prompt, project_name)

        return self.validate_response(response)
