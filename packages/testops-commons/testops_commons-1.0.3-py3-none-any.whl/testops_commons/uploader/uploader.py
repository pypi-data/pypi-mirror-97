from os import path
from pathlib import Path

import testops_api
from testops_api import ApiClient
from testops_api.model.file_resource import FileResource
from testops_api.model.upload_batch_file_resource import \
    UploadBatchFileResource
from urllib3 import make_headers, HTTPConnectionPool, HTTPSConnectionPool

from testops_commons.configuration.configuration import \
    Configuration
from testops_commons.core import constants
from testops_commons.helper import file_helper, helper
from testops_commons.testops_connector import TestOpsConnector

PROXY_PROTOCOL_HTTP = "http"

PROXY_PROTOCOL_HTTPS = "https"


class ReportUploader:
    def upload(self):
        pass


class TestOpsReportUploader(ReportUploader):
    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.report_pattern = constants.REPORT_PATTERN
        self.testops_connector = TestOpsConnector(self.create_api_client())

    def create_api_client(self) -> ApiClient:
        config: testops_api.Configuration = testops_api.Configuration(
            host=self.configuration.server_url,
            username='',
            password=self.configuration.api_key
        )
        config.verify_ssl = False

        if self.configuration.proxy_information.host:
            if self.configuration.proxy_information.protocol == PROXY_PROTOCOL_HTTP:
                config.proxy = HTTPConnectionPool(host=self.configuration.proxy_information.host
                                                  , port=self.configuration.proxy_information.port)
            elif self.configuration.proxy_information.protocol == PROXY_PROTOCOL_HTTPS:
                config.proxy = HTTPSConnectionPool(host=self.configuration.proxy_information.host
                                                   , port=self.configuration.proxy_information.port)
            proxy_user = self.configuration.proxy_information.username
            proxy_pass = self.configuration.proxy_information.password
            if (proxy_user is not None) and (proxy_pass is not None):
                config.proxy_headers = make_headers(proxy_basic_auth="{}:{}"
                                                    .format(self.configuration.proxy_information.username,
                                                            self.configuration.proxy_information.password))

        client: ApiClient = ApiClient(config)
        return client

    def upload_file(self, info: FileResource, file_path: str, is_end: bool) -> UploadBatchFileResource:
        file_resource: UploadBatchFileResource = UploadBatchFileResource()
        file_path_absolute = path.realpath(file_path)
        parent_path_absolute = path.dirname(file_path_absolute)
        file_name = path.basename(file_path)
        try:
            self.testops_connector.upload_file(
                info.upload_url, file_path_absolute)
            file_resource.file_name = file_name
            file_resource.folder_path = parent_path_absolute
            file_resource.uploaded_path = info.path
            file_resource.end = is_end
            return file_resource
        except Exception as e:
            return None

    def upload(self):
        api_key = self.configuration.api_key
        if helper.is_blank(api_key):
            return

        project_id = self.configuration.project_id
        if project_id is None:
            return

        report_path: Path = self.configuration.report_folder
        files: list = file_helper.scan_files(report_path)
        file_resources: list = self.testops_connector.get_upload_urls(
            project_id, len(files))
        bath: str = helper.generate_upload_batch()
        uploaded = []
        for i, (file, file_resource) in enumerate(zip(files, file_resources)):
            is_end = i == len(files) - 1
            rel = self.upload_file(file_resource, file, is_end)
            if rel:
                uploaded.append(rel)
        self.testops_connector.upload_testops_report(
            uploaded, project_id, bath)
