from .nunit import NUnitParser
from .junit import JUnitParser 
from typing import Any
from utils import Tech
import logging

class Parser:
    
    def __init__(self, logger: logging.Logger):
        
        self.parsers = {
            Tech.NUNIT.value: NUnitParser(logger),
            Tech.JUNIT.value: JUnitParser(logger),
        }

    def parse(self, xml_content: str, tech: str) -> Any:
        if tech not in self.parsers:
            raise ValueError(f"Unsupported technology: {tech}")
        parser = self.parsers[tech]
        return parser.parse(xml_content)