from pathlib import Path

from testops_commons.core.constants import *
from testops_commons.helper.helper import ConfigurationHelper, is_blank


class ProxyInformation:
    def __init__(self,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 protocol: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.protocol = protocol


class Configuration:
    def __init__(self,
                 server_url: str,
                 api_key: str,
                 project_id: int,
                 report_folder: str,
                 build_label: str,
                 build_url: str,
                 proxy_information: ProxyInformation):
        self.server_url = server_url
        self.api_key = api_key
        self.project_id = project_id
        self.report_folder = report_folder
        self.build_url = build_url
        self.build_label = build_label
        self.proxy_information = proxy_information


class TestOpsConfigurationCreator:

    def __init__(self):
        self.conf = ConfigurationHelper()

    def create_proxy_information(self) -> ProxyInformation:
        host = self.conf.get_config(
            TESTOPS_PROXY_HOST,
            env_name=TESTOPS_PROXY_HOST_ENV)

        port_str = self.conf.get_config(
            TESTOPS_PROXY_PORT,
            env_name=TESTOPS_PROXY_PORT_ENV)
        port = -1
        if not is_blank(port_str):
            port = int(port_str)

        username = self.conf.get_config(
            TESTOPS_PROXY_USERNAME,
            env_name=TESTOPS_PROXY_USERNAME_ENV,
            default='')

        password = self.conf.get_config(
            TESTOPS_PROXY_PASSWORD,
            env_name=TESTOPS_PROXY_PASSWORD_ENV,
            default='')

        protocol = self.conf.get_config(
            TESTOPS_PROXY_SERVER_TYPE,
            env_name=TESTOPS_PROXY_SERVER_TYPE_ENV,
            default=TESTOPS_PROXY_SERVER_TYPE_DEFAULT)

        return ProxyInformation(host=host,
                                port=port,
                                username=username,
                                password=password,
                                protocol=protocol)

    def create_configuration(self) -> Configuration:
        server_url = self.conf.get_config(
            TESTOPS_SERVER_URL,
            env_name=TESTOPS_SERVER_URL_ENV,
            default=TESTOPS_SERVER_URL_DEFAULT)

        project_id_str = self.conf.get_config(
            TESTOPS_PROJECT_ID,
            env_name=TESTOPS_PROJECT_ID_ENV)
        project_id = -1
        if not is_blank(project_id_str):
            project_id = int(project_id_str)

        report_folder_path = self.conf.get_config(
            TESTOPS_REPORT_FOLDER,
            env_name=TESTOPS_REPORT_FOLDER_ENV,
            default=TESTOPS_REPORT_FOLDER_DEFAULT)
        report_folder: Path = Path(report_folder_path)

        api_key = self.conf.get_config(
            TESTOPS_API_KEY,
            env_name=TESTOPS_API_KEY_ENV)

        build_label = self.conf.get_config(
            TESTOPS_BUILD_LABEL,
            env_name=TESTOPS_BUILD_LABEL_ENV)

        build_url = self.conf.get_config(
            TESTOPS_BUILD_URL,
            env_name=TESTOPS_BUILD_URL_ENV)

        proxy_information = self.create_proxy_information()

        return Configuration(server_url=server_url,
                             api_key=api_key,
                             project_id=project_id,
                             report_folder=report_folder,
                             build_label=build_label,
                             build_url=build_url,
                             proxy_information=proxy_information)
