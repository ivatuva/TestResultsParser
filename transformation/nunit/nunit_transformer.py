from typing import Any, List, Optional, Union
from transformation import TestRun, TestSuite, TestCase
from parsing import NunitTestRun, Failure, NUnitTestCase, NUnitTestSuite
import pprint, datetime

class NunitTransformer:

    def transform(self, test_run: 'NunitTestRun') -> TestRun:
        test_suites = [self.process_leaf_suites(suite) for suite in test_run.test_suites]
        processed_suites = self.flatten(test_suites)

        return TestRun(
            id=test_run.id,
            name=test_run.name,
            testcasecount=test_run.testcasecount,
            result=test_run.result,
            total=test_run.total,
            passed=test_run.passed,
            failed=test_run.failed,
            warnings=test_run.warnings,
            inconclusive=test_run.inconclusive,
            skipped=test_run.skipped,
            start_time=datetime.datetime.strptime(test_run.start_time[:-1], "%Y-%m-%d %H:%M:%S"),
            end_time=datetime.datetime.strptime(test_run.end_time[:-1], "%Y-%m-%d %H:%M:%S"),
            duration=float(test_run.duration),
            test_suites=processed_suites
        )
        
    def process_leaf_suites(self, suite: NUnitTestSuite) -> Union[NUnitTestSuite, List[Union[NUnitTestSuite, List]]]:
        # If the suite has no inner suites, process it
        if not suite.test_suites:
            return self._transform_test_suite(suite)
        # Otherwise, recursively process inner suites
        else:
            return [self.process_leaf_suites(inner_suite) for inner_suite in suite.test_suites]
        
    def flatten(self, suites: List[Union[NUnitTestSuite, List]]) -> List[NUnitTestSuite]:
        flat_list = []
        for item in suites:
            if isinstance(item, list):
                flat_list.extend(self.flatten(item))
            else:
                flat_list.append(item)
        return flat_list
    
    def _transform_test_suite(self, test_suite: 'NUnitTestSuite') -> TestSuite:
        test_cases = [self._transform_test_case(case) for case in test_suite.test_cases]

        return TestSuite(
            name=test_suite.name,
            testcasecount=test_suite.testcasecount,
            result=test_suite.result,
            start_time=test_suite.start_time,
            end_time=test_suite.end_time,
            duration=test_suite.duration,
            total=test_suite.total,
            passed=test_suite.passed,
            failed=test_suite.failed,
            warnings=test_suite.warnings,
            inconclusive=test_suite.inconclusive,
            skipped=test_suite.skipped,
            failure=self._transform_failure(test_suite.failure),
            test_cases=test_cases
        )

    def _transform_test_case(self, test_case: 'NUnitTestCase') -> TestCase:
        return TestCase(
            name=test_case.name,
            description=self._get_property(test_case.properties, "Description"),
            result=test_case.result,
            start_time=test_case.start_time,
            end_time=test_case.end_time,
            duration=test_case.duration,
            failure=self._transform_failure(test_case.failure)
        )

    def _transform_failure(self, failure: Optional[Failure]) -> Optional[dict]:
        if failure is None:
            return None
        return {
            "message": failure.message,
            "stack_trace": failure.stack_trace
        }

    def _get_property(self, properties: List[dict], name: str) -> Optional[str]:
        for prop in properties:
            if prop.name == name:
                return prop.value
        return None