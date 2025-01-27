from typing import Any
from utils import Tech
from .nunit import NunitTransformer
from .test_run_model import TestRun
from .junit import JunitTransformer

class Transformer:
    def __init__(self):
        self.transformers = {
            Tech.NUNIT.value: NunitTransformer(),
            Tech.JUNIT.value: JunitTransformer(),
        }

    def transform(self, parsed_data: Any, tech: str) -> TestRun:
        if tech not in self.transformers:
            raise ValueError(f"Unsupported technology: {tech}")
        parser = self.transformers[tech]
        return parser.transform(parsed_data)