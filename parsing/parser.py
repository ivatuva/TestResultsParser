from .nunit import NUnitParser
from typing import Any
from utils import Tech

class Parser:
    def __init__(self):
        self.parsers = {
            Tech.NUNIT.value: NUnitParser(),
            # Add other parsers here as they are implemented
        }

    def parse(self, xml_content: str, tech: str) -> Any:
        if tech not in self.parsers:
            raise ValueError(f"Unsupported technology: {tech}")
        parser = self.parsers[tech]
        return parser.parse(xml_content)