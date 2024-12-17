from typing import List, Optional

class TestRun:
    def __init__(self, id: str, name: str, testcasecount: int, result: str, total: int, passed: int, failed: int, 
                 warnings: int, inconclusive: int, skipped: int, start_time: str, end_time: str, duration: str, 
                 test_suites: List['TestSuite']):
        self.id = id
        self.name = name
        self.testcasecount = testcasecount
        self.result = result
        self.total = total
        self.passed = passed
        self.failed = failed
        self.warnings = warnings
        self.inconclusive = inconclusive
        self.skipped = skipped
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.test_suites = test_suites

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "testcasecount": self.testcasecount,
            "result": self.result,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "inconclusive": self.inconclusive,
            "skipped": self.skipped,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "test_suites": [suite.to_dict() for suite in self.test_suites]
        }

class TestSuite:
    def __init__(self, name: str, testcasecount: int, result: str, start_time: str, end_time: str, duration: str, 
                 total: int, passed: int, failed: int, warnings: int, inconclusive: int, skipped: int, 
                 failure: Optional[dict], test_cases: List['TestCase']):
        self.name = name
        self.testcasecount = testcasecount
        self.result = result
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.total = total
        self.passed = passed
        self.failed = failed
        self.warnings = warnings
        self.inconclusive = inconclusive
        self.skipped = skipped
        self.failure = failure
        self.test_cases = test_cases

    def to_dict(self):
        return {
            "name": self.name,
            "testcasecount": self.testcasecount,
            "result": self.result,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "inconclusive": self.inconclusive,
            "skipped": self.skipped,
            "failure": self.failure,
            "test_cases": [case.to_dict() for case in self.test_cases]
        }

class TestCase:
    def __init__(self, name: str, description: Optional[str], result: str, start_time: str, end_time: str, 
                 duration: str, failure: Optional[dict]):
        self.name = name
        self.description = description
        self.result = result
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.failure = failure

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "result": self.result,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "failure": self.failure
        }