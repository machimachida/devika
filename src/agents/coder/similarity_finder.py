from jinja2 import Environment, BaseLoader
import json
from pathlib import Path

from src.config import Config
from src.filesystem import ReadCode
from src.llm import LLM
from src.logger import Logger
from src.services.utils import retry_wrapper


class SimilarityFinder:
    def __init__(self, base_model: str):
        config = Config()
        self.project_dir = config.get_projects_dir()
        self.logger = Logger()
        self.llm = LLM(model_id=base_model)
        parent = Path(__file__).resolve().parent
        with open(parent.joinpath("similarity.jinja2"), 'r') as file:
            self.prompt_template = file.read().strip()

    def render(self, step_by_step_plan: str, methods: list[str]) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.prompt_template)
        return template.render(
            step_by_step_plan=step_by_step_plan,
            methods=methods,
        )

    def validate_response(self, response: str) -> list[str]:
        """
        以下の形式でレスポンスが返却されていることを確認し、methodsのもつlistを返却する

        ```
        {
          "methods": [
            "com.example.task.TaskService#createTask",
            "com.example.user.UserService#createUser"
          ]
        }
        }
        ```
        """

        try:
            # \nやスペースの他に、```がJSONの前後にある場合があるので、削除する
            stripped = response.strip().replace('```', '')
            response_dict = json.loads(stripped)
            return response_dict.get('methods', [])
        except json.JSONDecodeError:
            self.logger.error(f'Failed to decode response as JSON: {response}')
            return []

    @retry_wrapper
    def execute(self, step_by_step_plan: str, project_name: str) -> list[str]:
        methods_dict: dict[str, str] = ReadCode(project_name).get_methods_names()
        methods: list[str] = list(methods_dict.keys())
        prompt = self.render(step_by_step_plan=step_by_step_plan, methods=methods)
        response = self.llm.inference(prompt, project_name)

        return self.validate_response(response)
