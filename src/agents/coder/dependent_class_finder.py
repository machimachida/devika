import json

from jinja2 import Environment, BaseLoader
from pathlib import Path

from src.config import Config
from src.llm import LLM
from src.logger import Logger
from src.services.utils import retry_wrapper
from src.socket_instance import EmitAgent


class DependentClassFinder:
    def __init__(self, base_model: str):
        config = Config()
        self.project_dir = config.get_projects_dir()
        self.logger = Logger()
        self.llm = LLM(model_id=base_model)
        parent = Path(__file__).resolve().parent
        with open(parent.joinpath("dependent_class_finder.jinja2"), 'r') as file:
            self.prompt_template = file.read().strip()

    def render(
            self, instruction: str
    ) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(self.prompt_template)
        return template.render(
            instruction=instruction,
        )

    def validate_response(self, response: str) -> tuple[list[str], list[str]]:
        try:
            # \nやスペースの他に、```がJSONの前後にある場合があるので、削除する
            stripped = response.strip().replace('```', '')
            response = json.loads(stripped)
            return response["classes"], response["methods"]
        except json.JSONDecodeError:
            self.logger.error(f'Failed to decode response as JSON: {response}')
            return [], []

    @retry_wrapper
    def execute(
            self,
            instruction: str,
            project_name: str,
    ) -> tuple[list[str], list[str]]:
        prompt = self.render(instruction)
        response = self.llm.inference(prompt, project_name)
        return self.validate_response(response)
