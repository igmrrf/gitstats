from jinja2 import Environment, FileSystemLoader
import os

template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(loader=FileSystemLoader(template_dir))

class RenderService:
    @staticmethod
    def render_stats_card(data: dict) -> str:
        template = env.get_template("stats_card.svg")
        return template.render(**data)

    @staticmethod
    def render_top_langs(data: dict) -> str:
        # To be implemented
        pass
