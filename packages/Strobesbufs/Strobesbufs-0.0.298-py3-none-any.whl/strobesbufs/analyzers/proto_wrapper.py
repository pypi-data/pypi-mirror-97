from google.protobuf.struct_pb2 import Struct
from strobesbufs.analyzers.enums import SeverityType
from google.protobuf.json_format import MessageToDict
from strobesbufs.analyzers import analyzers_pb2 as pb2


class ProtoWrapper:
    def __init__(self, analyzer):
        self.result = pb2.Result()
        self.scan_meta = pb2.ScanMeta()
        self.bugs_list = []
        self.assets_list = []
        self.result.analyzer = getattr(pb2.Result.Analyzer, analyzer.upper())
        self.report = None

    def add_bug_count(self, severity: int):
        self.scan_meta.total_bugs += 1
        setattr(self.scan_meta, SeverityType(severity).name,
                getattr(self.scan_meta,
                        SeverityType(severity).name) + 1)

    def generate_report(self):
        self.result.bugs_list.extend(self.bugs_list)
        self.result.assets_list.extend(self.assets_list)
        self.result.scan_meta.CopyFrom(self.scan_meta)
        self.report = MessageToDict(
            self.result, including_default_value_fields=True)

    @staticmethod
    def create_sast_object(**kwargs) -> pb2.SAST:
        sast = pb2.SAST()
        if "file_name" in kwargs:
            sast.file_name = kwargs.get("file_name")
        if "vulnerable_code" in kwargs:
            sast.vulnerable_code = kwargs.get("vulnerable_code")
        if "start_line_no" in kwargs:
            sast.start_line_no = kwargs.get("start_line_no")
        if "end_line_no" in kwargs:
            sast.end_line_no = kwargs.get("end_line_no")
        if "commit" in kwargs:
            sast.commit = kwargs.get("commit")
        return sast

    @staticmethod
    def create_dast_object(**kwargs) -> pb2.DAST:
        dast = pb2.DAST()
        if "uri" in kwargs:
            uri = kwargs.get("uri")
            if isinstance(uri, list):
                dast.uri.extend(uri)
        if "port" in kwargs:
            port = kwargs.get("port")
            if isinstance(port, dict):
                port = ProtoWrapper.create_port_object(**port)
            if isinstance(port, pb2.Port):
                dast.port.CopyFrom(port)
        if "method" in kwargs:
            dast.method = kwargs.get("method")
        if "param" in kwargs:
            dast.param = kwargs.get("param")
        if "evidence" in kwargs:
            dast.evidence = kwargs.get("evidence")
        if "request_headers" in kwargs:
            dast.request_headers = kwargs.get("request_headers")
        if "response_headers" in kwargs:
            dast.response_headers = kwargs.get("response_headers")
        return dast

    @staticmethod
    def create_network_object(**kwargs) -> pb2.Network:
        network = pb2.Network()
        if "ipaddress" in kwargs:
            network.ipaddress = kwargs.get("ipaddress")
        if "port" in kwargs:
            port = kwargs.get("port")
            if isinstance(port, dict):
                port = ProtoWrapper.create_port_object(**port)
            if isinstance(port, pb2.Port):
                network.port.CopyFrom(port)
        if "hostname" in kwargs:
            network.hostname = kwargs.get("hostname")
        if "macaddress" in kwargs:
            network.macaddress = kwargs.get("macaddress")
        if "cpe" in kwargs:
            network.cpe = kwargs.get("cpe")
        return network

    @staticmethod
    def create_package_object(**kwargs) -> pb2.Package:
        package = pb2.Package()
        if "name" in kwargs:
            package.name = kwargs.get("name")
        if "installed_version" in kwargs:
            package.installed_version = kwargs.get("installed_version")
        if "affected_versions" in kwargs:
            package.affected_versions = kwargs.get("affected_versions")
        if "commit" in kwargs:
            package.commit = kwargs.get("commit")
        return package

    @staticmethod
    def create_container_object(**kwargs) -> pb2.Container:
        container = pb2.Container()
        if "package_name" in kwargs:
            container.package_name = kwargs.get("package_name")
        if "fixed_version" in kwargs:
            container.fixed_version = kwargs.get("fixed_version")
        if "installed_version" in kwargs:
            container.installed_version = kwargs.get("installed_version")
        if "cpe" in kwargs:
            cpes = kwargs.get("cpe")
            if isinstance(cpes, list):
                container.cpe.extend(cpes)
        if "digest" in kwargs:
            container.digest = kwargs.get("digest")
        return container

    @staticmethod
    def create_cloud_object(**kwargs) -> pb2.Cloud:
        cloud = pb2.Cloud()
        if "region" in kwargs:
            cloud.region = kwargs.get("region")
        if "aws" in kwargs:
            aws_details = kwargs.get("aws")
            if isinstance(aws_details, dict):
                aws_details = ProtoWrapper.create_aws_object(**aws_details)
            if isinstance(aws_details, pb2.AWS):
                cloud.aws.CopyFrom(aws_details)
        return cloud

    @staticmethod
    def create_aws_object(**kwargs) -> pb2.AWS:
        aws = pb2.AWS()
        if "resource_id" in kwargs:
            aws.resource_id = kwargs.get("resource_id")
        if "type" in kwargs:
            aws_type = kwargs.get("type")
            if isinstance(aws_type, int):
                aws.type = aws_type
        if "category" in kwargs:
            aws.category = kwargs.get("category")
        return aws

    @staticmethod
    def create_port_object(**kwargs) -> pb2.Port:
        port = pb2.Port()
        if "protocol" in kwargs:
            port.protocol = kwargs.get("protocol")
        if "port_id" in kwargs:
            port.port_id = kwargs.get("port_id")
        if "service" in kwargs:
            port.service = kwargs.get("service")
        if "product" in kwargs:
            port.product = kwargs.get("product")
        if "state" in kwargs:
            state = kwargs.get("state")
            if isinstance(state, int):
                port.state = state
        return port

    @staticmethod
    def create_asset_object(**kwargs) -> pb2.Asset:
        asset = pb2.Asset()
        if "name" in kwargs:
            asset.name = kwargs.get("name")
        if "ipaddress" in kwargs:
            asset.ipaddress = kwargs.get("ipaddress")
        if "os" in kwargs:
            os = kwargs.get("os")
            if isinstance(os, list):
                asset.os.extend(os)
        if "mac_address" in kwargs:
            asset.mac_address = kwargs.get("mac_address")
        if "hostname" in kwargs:
            asset.hostname = kwargs.get("hostname")
        if "netbios" in kwargs:
            asset.netbios = kwargs.get("netbios")
        if "cpe" in kwargs:
            cpe = kwargs.get("cpe")
            if isinstance(cpe, list):
                asset.cpe.extend(cpe)
        if "tags" in kwargs:
            tags = kwargs.get("tags")
            if isinstance(tags, list):
                asset.tags.extend(tags)
        if "risk_score" in kwargs:
            asset.risk_score = kwargs.get("risk_score")
        if "ports" in kwargs:
            ports = kwargs.get("ports")
            if isinstance(ports, list):
                refined_ports = []
                for port in ports:
                    if isinstance(port, dict):
                        port = ProtoWrapper.create_port_object(**port)
                    refined_ports.append(port)
                asset.ports.extend(refined_ports)
        if "state" in kwargs:
            state = kwargs.get("state")
            if isinstance(state, int):
                asset.state = state
        return asset

    @staticmethod
    def create_bug_object(**kwargs) -> pb2.Bug:
        bug = pb2.Bug()
        if "title" in kwargs:
            bug.title = kwargs.get("title")
        if "description" in kwargs:
            bug.description = kwargs.get("description")
        if "severity" in kwargs:
            severity = kwargs.get("severity")
            if isinstance(severity, int):
                bug.severity = severity
        if "CVSS" in kwargs:
            cvss = kwargs.get("CVSS")
            if isinstance(cvss, float):
                bug.CVSS = cvss
        if "step_to_reproduce" in kwargs:
            bug.step_to_reproduce = kwargs.get("step_to_reproduce")
        if "mitigation" in kwargs:
            bug.mitigation = kwargs.get("mitigation")
        if "CVE" in kwargs:
            cve = kwargs.get("CVE")
            if isinstance(cve, list):
                bug.CVE.extend(cve)
        if "CWE" in kwargs:
            cwe = kwargs.get("CWE")
            if isinstance(cwe, list):
                bug.CWE.extend(cwe)
        if "references" in kwargs:
            references = kwargs.get("references")
            if isinstance(references, list):
                bug.references.extend(references)
        if "sast" in kwargs:
            sast = kwargs.get("sast")
            if isinstance(sast, pb2.SAST):
                bug.sast.CopyFrom(sast)
        if "dast" in kwargs:
            dast = kwargs.get("dast")
            if isinstance(dast, pb2.DAST):
                bug.dast.CopyFrom(dast)
        if "network" in kwargs:
            network = kwargs.get("network")
            if isinstance(network, pb2.Network):
                bug.network.CopyFrom(network)
        if "cloud" in kwargs:
            cloud = kwargs.get("cloud")
            if isinstance(cloud, pb2.Cloud):
                bug.cloud.CopyFrom(cloud)
        if "package" in kwargs:
            package = kwargs.get("package")
            if isinstance(package, pb2.Package):
                bug.package.CopyFrom(package)
        if "container" in kwargs:
            container = kwargs.get("container")
            if isinstance(container, pb2.Container):
                bug.container.CopyFrom(container)
        if "tags" in kwargs:
            tags = kwargs.get("tags")
            if isinstance(tags, list):
                bug.tags.extend(tags)
        if "extra_info" in kwargs:
            extra_info = kwargs.get("extra_info")
            if isinstance(extra_info, dict):
                struct = Struct()
                struct.update(extra_info)
            elif isinstance(extra_info, Struct):
                struct = extra_info
            bug.extra_info.CopyFrom(struct)
        if "scan_details" in kwargs:
            scan_details = kwargs.get("scan_details")
            if isinstance(scan_details, dict):
                for key, value in scan_details.items():
                    bug.scan_details[key] = value
        if "asset" in kwargs:
            asset = kwargs.get("asset")
            if isinstance(asset, pb2.Asset):
                bug.asset.CopyFrom(asset)
        if "vulnerable_since" in kwargs:
            bug.vulnerable_since = kwargs.get("vulnerable_since")
        return bug
