from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Failure:
    message: str
    type: str

    def __init__(self, message: str, type: str) -> None:
        self.message = message
        self.type = type

@dataclass
class JUnitTestCase:
    failure: Failure
    name: str
    time: str
    classname: str

    def __init__(self, failure: Failure, name: str, time: str, classname: str) -> None:
        self.failure = failure
        self.name = name
        self.time = time
        self.classname = classname

@dataclass
class JUnitTestSuite:
    name: str
    timestamp: str
    tests: int
    file: Optional[str]
    time: str
    failures: int
    testcases: Optional[JUnitTestCase]

    def __init__(self, name: str, timestamp: str, tests: int, file: Optional[str], time: str, failures: int, testcases: Optional[JUnitTestCase]) -> None:
        self.name = name
        self.timestamp = timestamp
        self.tests = tests
        self.file = file
        self.time = time
        self.failures = failures
        self.testcases = testcases

@dataclass
class JUnitTestRun:
    testsuites: List[JUnitTestSuite]

    def __init__(self, testsuites: List[JUnitTestSuite]) -> None:
        self.testsuites = testsuites
