import json
from typing import List

from jinja2 import Environment, BaseLoader

from src.llm import LLM
from src.services.utils import retry_wrapper
from src.browser.search import BingSearch

PROMPT = open("src/agents/researcher/prompt.jinja2").read().strip()


class Researcher:
    def __init__(self, base_model: str):
        self.bing_search = BingSearch()
        self.llm = LLM(model_id=base_model)

    def render(self, step_by_step_plan: str, contextual_keywords: str) -> str:
        env = Environment(loader=BaseLoader())
        template = env.from_string(PROMPT)
        return template.render(
            step_by_step_plan=step_by_step_plan,
            contextual_keywords=contextual_keywords
        )

    def validate_response(self, response: str) -> dict | bool:
        response = response.strip().replace("```json", "```")

        if response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
        try:
            response = json.loads(response)
        except Exception as _:
            return False

        if "plans" not in response:
            return False

        query_list: list[dict[str, str]] = []
        for plan in response["plans"]:
            if "queries" not in plan and "ask_user" not in plan:
                return False
            else:
                query_list.append({
                    "queries": plan["queries"],
                    "ask_user": plan["ask_user"]
                })

        queries: list[str] = []
        ask_user: str = ""
        for i, query in enumerate(query_list):
            queries.extend(query["queries"])
            if query["ask_user"] != "":
                ask_user = ask_user + str(i+1) + query["ask_user"] + "\n"
        return {
            "queries": queries,
            "ask_user": ask_user
        }

    @retry_wrapper
    def execute(self, step_by_step_plan: str, contextual_keywords: List[str], project_name: str) -> dict | bool:
        contextual_keywords_str = ", ".join(map(lambda k: k.capitalize(), contextual_keywords))
        prompt = self.render(step_by_step_plan, contextual_keywords_str)
        
        response = self.llm.inference(prompt, project_name)
        
        valid_response = self.validate_response(response)

        return valid_response
