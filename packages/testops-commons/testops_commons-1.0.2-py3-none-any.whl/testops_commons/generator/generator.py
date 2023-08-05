from os import path
from pathlib import Path

from testops_commons.configuration.configuration import Configuration
from testops_commons.core import constants
from testops_commons.helper import file_helper, helper
from testops_commons.model.models import (Execution, Metadata, TestResults,
                                          TestSuites)


class ReportGenerator:
    def write_execution(self, execution: Execution):
        pass

    def write_test_suites(self, suites: TestSuites):
        pass

    def write_test_results(self, results: TestResults):
        pass

    def write_metadata(self, metadata: Metadata):
        pass


class TestOpsReportGenerator(ReportGenerator):

    configuration: Configuration
    output_directory: Path

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.output_directory = configuration.report_folder
        file_helper.ensure_directory(self.output_directory)
        pass

    def write_execution(self, execution: Execution):
        self.write_to_file(execution, 'execution' + constants.REPORT_FILE_EXTENSION)

    def write_test_suites(self, suites: TestSuites):
        self.write_to_file(suites, 'suites' + constants.REPORT_FILE_EXTENSION)
        pass

    def write_test_results(self, results: TestResults):
        self.write_to_file(results, 'results' + constants.REPORT_FILE_EXTENSION)
        pass

    def write_metadata(self, metadata: Metadata):
        build_label: str = self.configuration.build_label
        build_url: str = self.configuration.build_url
        metadata.build_url = build_url
        metadata.build_label = build_label
        self.write_to_file(metadata, 'metadata' + constants.REPORT_FILE_EXTENSION)

    def write_to_file(self, data, file_name: str):
        helper.write_json(data, path.join(self.output_directory, file_name))
