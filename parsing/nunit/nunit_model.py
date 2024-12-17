from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Property:
    name: str
    value: str

@dataclass
class Failure:
    message: str
    stack_trace: Optional[str] = None

@dataclass
class Assertion:
    result: str
    message: Optional[str] = None
    stack_trace: Optional[str] = None

@dataclass
class NUnitTestCase:
    id: str
    name: str
    fullname: str
    methodname: str
    classname: str
    runstate: str
    seed: str
    result: str
    start_time: str
    end_time: str
    duration: str
    asserts: str
    properties: List[Property]
    failure: Optional[Failure] = None
    assertions: List[Assertion] = None

@dataclass
class Environment:
    framework_version: str
    clr_version: str
    os_version: str
    platform: str
    cwd: str
    machine_name: str
    user: str
    user_domain: str
    culture: str
    uiculture: str
    os_architecture: str

@dataclass
class Setting:
    name: str
    value: str

@dataclass
class NUnitTestSuite:
    type: str
    id: str
    name: str
    fullname: str
    runstate: str
    testcasecount: str
    result: str
    site: str
    start_time: str
    end_time: str
    duration: str
    total: str
    passed: str
    failed: str
    warnings: str
    inconclusive: str
    skipped: str
    asserts: str
    environment: Optional[Environment] = None
    settings: List[Setting] = None
    properties: List[Property] = None
    failure: Optional[Failure] = None
    test_suites: List['NUnitTestSuite'] = None
    test_cases: List[NUnitTestCase] = None

@dataclass
class NunitTestRun:
    id: str
    name: str
    fullname: str
    runstate: str
    testcasecount: str
    result: str
    total: str
    passed: str
    failed: str
    warnings: str
    inconclusive: str
    skipped: str
    asserts: str
    engine_version: str
    clr_version: str
    start_time: str
    end_time: str
    duration: str
    command_line: str
    filter: str
    test_suites: List[NUnitTestSuite]