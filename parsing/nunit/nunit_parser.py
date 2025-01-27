import xml.etree.ElementTree as ET
from typing import List
from .nunit_model import NunitTestRun, NUnitTestSuite, NUnitTestCase, Property, Failure, Assertion, Environment, Setting
import logging

class NUnitParser:
    _logger: logging.Logger
    
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        
    def parse(self, xml_contents: List[str]) -> NunitTestRun:
        try:
            root = ET.fromstring(xml_contents[0])
            return self._parse_test_run(root)
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
            raise

    def _parse_test_run(self, element) -> NunitTestRun:
        test_suites = [self._parse_test_suite(suite) for suite in element.findall('test-suite')]
        return NunitTestRun(
            id=element.get('id'),
            name=element.get('name'),
            fullname=element.get('fullname'),
            runstate=element.get('runstate'),
            testcasecount=element.get('testcasecount'),
            result=element.get('result'),
            total=element.get('total'),
            passed=element.get('passed'),
            failed=element.get('failed'),
            warnings=element.get('warnings'),
            inconclusive=element.get('inconclusive'),
            skipped=element.get('skipped'),
            asserts=element.get('asserts'),
            engine_version=element.get('engine-version'),
            clr_version=element.get('clr-version'),
            start_time=element.get('start-time'),
            end_time=element.get('end-time'),
            duration=element.get('duration'),
            command_line=element.findtext('command-line'),
            filter=ET.tostring(element.find('filter'), encoding='unicode'),
            test_suites=test_suites
        )

    def _parse_test_suite(self, element) -> NUnitTestSuite:
        environment = self._parse_environment(element.find('environment'))
        settings = [self._parse_setting(setting) for setting in element.findall('settings/setting')]
        properties = [self._parse_property(prop) for prop in element.findall('properties/property')]
        failure = self._parse_failure(element.find('failure'))
        test_suites = [self._parse_test_suite(suite) for suite in element.findall('test-suite')]
        test_cases = [self._parse_test_case(case) for case in element.findall('test-case')]
        return NUnitTestSuite(
            type=element.get('type'),
            id=element.get('id'),
            name=element.get('name'),
            fullname=element.get('fullname'),
            runstate=element.get('runstate'),
            testcasecount=element.get('testcasecount'),
            result=element.get('result'),
            site=element.get('site'),
            start_time=element.get('start-time'),
            end_time=element.get('end-time'),
            duration=element.get('duration'),
            total=element.get('total'),
            passed=element.get('passed'),
            failed=element.get('failed'),
            warnings=element.get('warnings'),
            inconclusive=element.get('inconclusive'),
            skipped=element.get('skipped'),
            asserts=element.get('asserts'),
            environment=environment,
            settings=settings,
            properties=properties,
            failure=failure,
            test_suites=test_suites,
            test_cases=test_cases
        )

    def _parse_test_case(self, element) -> NUnitTestCase:
        properties = [self._parse_property(prop) for prop in element.findall('properties/property')]
        failure = self._parse_failure(element.find('failure'))
        assertions = [self._parse_assertion(assertion) for assertion in element.findall('assertions/assertion')]
        return NUnitTestCase(
            id=element.get('id'),
            name=element.get('name'),
            fullname=element.get('fullname'),
            methodname=element.get('methodname'),
            classname=element.get('classname'),
            runstate=element.get('runstate'),
            seed=element.get('seed'),
            result=element.get('result'),
            start_time=element.get('start-time'),
            end_time=element.get('end-time'),
            duration=element.get('duration'),
            asserts=element.get('asserts'),
            properties=properties,
            failure=failure,
            assertions=assertions
        )

    def _parse_property(self, element) -> Property:
        return Property(
            name=element.get('name'),
            value=element.get('value')
        )

    def _parse_failure(self, element) -> Failure:
        if element is None:
            return None
        return Failure(
            message=element.findtext('message'),
            stack_trace=element.findtext('stack-trace')
        )

    def _parse_assertion(self, element) -> Assertion:
        return Assertion(
            result=element.get('result'),
            message=element.findtext('message'),
            stack_trace=element.findtext('stack-trace')
        )

    def _parse_environment(self, element) -> Environment:
        if element is None:
            return None
        return Environment(
            framework_version=element.get('framework-version'),
            clr_version=element.get('clr-version'),
            os_version=element.get('os-version'),
            platform=element.get('platform'),
            cwd=element.get('cwd'),
            machine_name=element.get('machine-name'),
            user=element.get('user'),
            user_domain=element.get('user-domain'),
            culture=element.get('culture'),
            uiculture=element.get('uiculture'),
            os_architecture=element.get('os-architecture')
        )

    def _parse_setting(self, element) -> Setting:
        return Setting(
            name=element.get('name'),
            value=element.get('value')
        )