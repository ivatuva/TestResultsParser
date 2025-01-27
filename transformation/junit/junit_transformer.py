from typing import Any, List, Optional, Union
from transformation import TestRun, TestSuite, TestCase
from parsing import JUnitTestRun, Failure, JUnitTestCase, JUnitTestSuite
import pprint, uuid, datetime

class JunitTransformer:

    def transform(self, test_run: 'JUnitTestRun') -> TestRun:
        testcasecount = self._count_test_cases(test_run)
        result = self._calculate_execution_result(test_run)
        failed = self._count_failed_tests(test_run)
        start_time = self._get_execution_start_time(test_run)
        duration = self._get_execution_duration(test_run)
        end_time = self._calculate_end_time(start_time, duration)
        testsuites = [self._transform_test_suite(suite) for suite in test_run.testsuites]
        
        warnings = 0
        inconclusive = 0
        skipped = 0
        passed = testcasecount - failed - warnings - inconclusive - skipped
        return TestRun(
            id=str(uuid.uuid4()),
            name=str(uuid.uuid4()),
            testcasecount=testcasecount,
            result=result,
            total=testcasecount,
            passed=passed,
            failed=failed,
            warnings=warnings,
            inconclusive=inconclusive,
            skipped=skipped,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            test_suites=testsuites
        )
    
    def _count_test_cases(self, test_run: 'JUnitTestRun') -> int:
        counter = 0

        for suite in test_run.testsuites:
            counter = counter + suite.tests
        return counter
    
    def _calculate_execution_result(self, test_run: 'JUnitTestRun') -> str:
        for suite in test_run.testsuites:
            if suite.failures > 0:
                return 'Failed'
        return 'Passed'
    
    def _count_failed_tests(self, test_run: 'JUnitTestRun') -> int:
        counter = 0
        for suite in test_run.testsuites:
            counter = counter + suite.failures
        return counter
    
    def _get_execution_start_time(self, test_run: 'JUnitTestRun') -> datetime.datetime:
        start_time = datetime.datetime.now()
        for suite in test_run.testsuites:
            suite_start_time = datetime.datetime.strptime(suite.timestamp, "%Y-%m-%dT%H:%M:%S")
            if suite_start_time < start_time:
                start_time = suite_start_time
        return start_time        
        
    def _get_execution_duration(self, test_run: 'JUnitTestRun') -> float:
        duration = 0
        for suite in test_run.testsuites:
            suite_duration = float(suite.time)
            duration = duration + suite_duration
        return duration
    
    def _calculate_end_time(self, start_time: 'datetime.datetime', duration: 'float') -> datetime:
        return start_time + datetime.timedelta(0, duration)
                
    def _transform_test_suite(self, test_suite: 'JUnitTestSuite') -> TestSuite:
        suite_start_time = datetime.datetime.strptime(test_suite.timestamp, "%Y-%m-%dT%H:%M:%S")
        test_cases = [self._transform_test_case(case, suite_start_time) for case in test_suite.testcases]
        result = self._calculate_suite_result(test_suite)
        start_time = datetime.datetime.strptime(test_suite.timestamp, "%Y-%m-%dT%H:%M:%S")
        end_time = self._calculate_end_time(start_time, test_suite.time)
        
        warnings = 0
        inconclusive = 0
        skipped = 0
        passed = test_suite.tests - test_suite.failures - warnings - inconclusive - skipped
        
        return TestSuite(
            name=test_suite.name,
            testcasecount=test_suite.tests,
            result=result,
            start_time=test_suite.timestamp,
            end_time=end_time,
            duration=test_suite.time,
            total=test_suite.tests,
            passed=passed,
            failed=test_suite.failures,
            warnings=warnings,
            inconclusive=inconclusive,
            skipped=skipped,
            test_cases=test_cases,
            failure=None
        )
        
    def _calculate_suite_result(self, test_suite: 'JUnitTestSuite') -> str:
        if test_suite.failures > 0:
            return 'Failed'
        return 'Passed'
    
    def _transform_test_case(self, test_case: 'JUnitTestCase', suite_start_time: 'datetime.datetime') -> TestCase:
        result = self._calculate_test_case_result(test_case)
        end_time = self._calculate_end_time(suite_start_time, test_case.time)
        failures = self._transform_failure(test_case.failure)
        
        return TestCase(
            name=test_case.name,
            description=test_case.classname,
            result=result,
            start_time=suite_start_time,
            end_time=end_time,
            duration=test_case.time,
            failure=failures
        )
            
    def _calculate_test_case_result(self, test_case: 'JUnitTestCase') -> str:
        if test_case.failure == None:
            return 'Passed'
        return 'Failed'
    
    def _transform_failure(self, failure: Optional[Failure]) -> Optional[dict]:
        if failure is None:
            return None
        return {
            "message": failure.message,
            "type": failure.type
        }