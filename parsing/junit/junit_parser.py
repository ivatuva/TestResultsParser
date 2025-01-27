import xml.etree.ElementTree as ET
from typing import List
from .junit_model import JUnitTestRun, JUnitTestSuite, JUnitTestCase, Failure
import logging

class JUnitParser:
    _logger: logging.Logger
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        
    def parse(self, xml_contents: List[str]) -> JUnitTestRun:
        try:
            run = JUnitTestRun(testsuites=[])
            for content in xml_contents:
                root = ET.fromstring(content)
                result = self._parse_test_run(root)
                run.testsuites.extend(result.testsuites)
            return run
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
            raise

    def _parse_test_run(self, element) -> JUnitTestRun:
        test_suites = [self._parse_test_suite(suite) for suite in element.findall('testsuite')]
        return JUnitTestRun(
            testsuites=test_suites
        )

    def _parse_test_suite(self, element) -> JUnitTestSuite:
        test_cases = [self._parse_test_case(case) for case in element.findall('testcase')]

        return JUnitTestSuite(
            name=element.get('name'),
            timestamp=element.get('timestamp'),
            tests=int(element.get('tests', 0)),
            time=float(element.get('time', 0.0)),
            failures=int(element.get('failures', 0)),
            file=element.get('file', ''),
            testcases=test_cases
        )

    def _parse_test_case(self, element) -> JUnitTestCase:
        failure_element = element.find('failure')
        failure = self._parse_failure(failure_element) if failure_element is not None else None
        return JUnitTestCase(
            name=element.get('name'),
            classname=element.get('classname'),
            time=float(element.get('time', 0.0)),
            failure=failure
        )

    def _parse_failure(self, element) -> Failure:
        return Failure(
            message=element.get('message'),
            type=element.get('type')
        )