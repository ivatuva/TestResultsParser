from enum import Enum

class Tech(Enum):
    NUNIT = "nunit"
    JUNIT = "junit"
    CYPRESS = "cypress"
    APPIUM = "appium"

    @staticmethod
    def list():
        return list(map(lambda t: t.value, Tech))