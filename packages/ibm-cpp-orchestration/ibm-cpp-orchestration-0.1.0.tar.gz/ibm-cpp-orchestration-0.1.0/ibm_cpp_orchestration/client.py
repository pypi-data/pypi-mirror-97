# Copyright IBM Corp. 2020. All Rights Reserved.
import base64
import inspect
import json
import os
import warnings
from collections import abc
from typing import cast, ClassVar, Mapping, overload, Union, Optional, Any, \
    Dict, Sequence, Callable
from urllib.parse import urljoin

import requests
import responses
import attr
from attr import attrs, fields_dict, NOTHING
from ibm_cloud_sdk_core import BaseService, ApiException, DetailedResponse
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.get_authenticator import get_authenticator_from_environment
import ibm_boto3
from ibm_botocore.client import Config

from .client_errors import JsonParsingError, MissingValueError, \
    MultipleAlternativeArgumentsError, \
    UnknownOverloadError, OfCpdPathError, ScopeResponseNoFieldError, \
    NoWmlInstanceError, WmlServiceNameUnknownTypeError, \
    WmlServiceNameNoPrefixError, WmlServiceCNameNotValidError
from .cpd_paths import CpdScope
from .utils import validate_type, validate_type_from_config, \
    get_storage_config_field, get_scope_response_field, get_credentials_field


class CPDOrchestration(BaseService):
    DEFAULT_SERVICE_URL = "https://api.dataplatform.cloud.ibm.com"
    DEFAULT_SERVICE_NAME = 'cpd-orchestration'

    DEFAULT_CPD_API_URL = "https://api.dataplatform.cloud.ibm.com"

    @classmethod
    def new_instance(cls, *, service_name: str = None, url: str = None) -> 'CPDOrchestration':
        """
        Return a new client for the CPD Orchestration for default settings.
        """
        return cls(service_name=service_name, url=url)

    @classmethod
    def from_apikey(cls, apikey: str = None, *, service_name: str = None, url: str = None) -> 'CPDOrchestration':
        """
        Return a new client for the CPD Orchestration using the specified API key.
        """
        if apikey is None:
            apikey = os.environ.get('APIKEY', None)
        return cls(apikey=apikey, service_name=service_name, url=url)

    def __init__(
        self,
        apikey: str = None,
        *,
        service_name: str = None,
        url: str = None,
    ):
        """
        Construct a new client for the CPD Orchestration.

        :param Authenticator authenticator: The authenticator specifies the authentication mechanism.
               Get up to date information from https://github.com/IBM/python-sdk-core/blob/master/README.md
               about initializing the authenticator of your choice.
        :param str apikey: API key the authenticator should be constructed from.
        """
        url = self._get_cpd_api_url(url)
        validate_type(url, "url", str)

        if apikey is None:
            apikey = os.environ.get('APIKEY', None)
            if apikey is None:
                raise MissingValueError('APIKEY')
        validate_type(apikey, "apikey", str)

        authenticator = self._get_authenticator(apikey, url)

        if service_name is None:
            service_name = self.DEFAULT_SERVICE_NAME

        super().__init__(
            service_url=url,
            authenticator=authenticator
        )
        self.authenticator = authenticator
        self.apikey = apikey
        self.configure_service(service_name)

    def _get_iam_url(self, url: str) -> str:
        validate_type(url, "url", str)
        if not url.startswith("https://"):
            warnings.warn("'url' doesn't start with https")

        url_to_iam_url = {
            "https://api.dataplatform.dev.cloud.ibm.com": "https://iam.test.cloud.ibm.com/identity/token",
            "https://api.dataplatform.test.cloud.ibm.com": "https://iam.cloud.ibm.com/identity/token",
            "https://api.dataplatform.cloud.ibm.com": "https://iam.cloud.ibm.com/identity/token"
        }
        return url_to_iam_url.get(url, "https://iam.cloud.ibm.com/identity/token")

    def _get_authenticator(self, apikey: str, url: str) -> IAMAuthenticator:
        validate_type(apikey, "api_key", str)
        iam_url = self._get_iam_url(url)
        return IAMAuthenticator(apikey, url = iam_url)

    @classmethod
    def get_output_artifact_map(cls) -> Mapping[str, str]:
        """Given the name-value outputs map, generates name-key map."""
        output_artifacts = os.environ.get('OF_OUTPUT_ARTIFACTS', None)
        if output_artifacts is None:
            raise MissingValueError("OF_OUTPUT_ARTIFACTS")

        try:
            output_artifacts = json.loads(output_artifacts)
        except json.decoder.JSONDecodeError as ex:
            # could it be base64?
            try:
                pad_base64 = lambda s: s + '=' * (-len(s) % 4)
                output_artifacts = base64.b64decode(pad_base64(output_artifacts))
                output_artifacts = json.loads(output_artifacts)
            except:
                # if it has been decoded, show the decoded value
                raise JsonParsingError(output_artifacts, ex)

        validate_type(output_artifacts, "OF_OUTPUT_ARTIFACTS", abc.Mapping)
        for output_name, output_artifact in output_artifacts.items():
            validate_type(output_artifact, f"OF_OUTPUT_ARTIFACTS[{output_name}]", str)
        output_artifacts = cast(Mapping[str, str], output_artifacts)
        return output_artifacts

    def get_project(self, scope_id: str) -> dict:
        uri = urljoin("/v2/projects/", scope_id)
        scope = self._get_scope_from_uri(uri)
        return scope

    def get_space(self, scope_id: str) -> dict:
        uri = urljoin("/v2/spaces/", scope_id)
        scope = self._get_scope_from_uri(uri)
        return scope

    def _get_scope_from_uri(self, uri: str):
        headers = {
            "Accept": "application/json",
        }

        scope_request = self.prepare_request('GET', uri, headers = headers)
        # BaseService has some type signature problems here
        scope_request = cast(requests.Request, scope_request)

        scope_response = self.send(scope_request)

        if isinstance(scope_response.result, dict):
            scope = scope_response.result
        else:
            try:
                scope = json.loads(scope_response.result.content)
            except json.decoder.JSONDecodeError as ex:
                if hasattr(scope_response.result, 'content'):
                    raise JsonParsingError(scope_response.result.content, ex)
                else:
                    raise JsonParsingError(scope_response.result, ex)
        return scope

    def _get_cpd_api_url(self, url: str = None) -> str:
        if url is not None:
            return url

        url = os.environ.get('OF_CPD_API_URL', None)
        if url is not None:
            validate_type(url, "OF_CPD_API_URL", str)
            return url

        url = self.DEFAULT_CPD_API_URL
        validate_type(url, "DEFAULT_CPD_API_URL", str)
        return url

    def get_scope(
        self,
        cpd_scope: Optional[Union[str, CpdScope]] = None
    ) -> dict:
        cpd_scope = self._get_as_scope(cpd_scope)

        scope_type_map: Mapping[str, Callable[[str], dict]] = {
            'projects': self.get_project,
            'spaces': self.get_space,
        }

        scope_getter = scope_type_map.get(cpd_scope.scope_type, None)
        if scope_getter is None:
            li = ', '.join(scope_type_map.keys())
            msg = "Handling scopes other than {} is not supported yet!".format(li)
            raise NotImplementedError(msg)
        scope = scope_getter(cpd_scope.scope_id)
        return scope

    def get_storage_properties(
        self,
        scope_response: dict
    ) -> dict:
        props = get_scope_response_field(scope_response, 'entity.storage.properties', dict)
        return props

    def get_wml_credentials(
        self,
        cpd_scope: Optional[Union[str, CpdScope]] = None
    ) -> dict:
        cpd_scope = self._get_as_scope(cpd_scope)

        scope_response = self.get_scope(cpd_scope)

        wml_credentials = self._extract_wml_creds_from_scope_response(
            cpd_scope,
            scope_response
        )
        return wml_credentials.to_dict()

    def _extract_wml_creds_from_scope_response(
        self,
        cpd_scope: CpdScope,
        scope_response: dict
    ) -> 'WmlCredentials':
        computed = get_scope_response_field(
            scope_response, "entity.compute", list, mandatory=False
        )

        data = None
        for el in computed or []:
            if 'type' in el and el['type'] == 'machine_learning':
                data = el
                break

        if data is None:
            raise NoWmlInstanceError(cpd_scope)

        return self._extract_wml_creds_from_computed(data)

    def _extract_wml_creds_from_computed(
        self,
        computed: dict
    ) -> 'WmlCredentials':
        guid = get_credentials_field(computed, "guid", str)
        name = get_credentials_field(computed, "name", str)
        crn = get_credentials_field(computed, "crn", str)
        url = self._get_wml_url_from_wml_crn(crn)
        return WmlCredentials(
            guid = guid,
            name = name,
            url = url,
            apikey = self.apikey,
        )

    def _get_wml_url_from_wml_crn(self, crn: str) -> str:
        wml_prod = 'https://{}.ml.cloud.ibm.com'
        wml_qa = 'https://yp-qa.ml.cloud.ibm.com'
        wml_staging = 'https://{}.ml.test.cloud.ibm.com'
        wml_service_name = 'pm-20'
        wml_service_name_devops = 'pm-20-devops'
        platform_qa_url_host = 'api.dataplatform.test.cloud.ibm.com'

        parts = crn.split(':')

        cname = parts[2]
        service_name = parts[4]
        location = parts[5]

        if not service_name.startswith(wml_service_name):
            raise WmlServiceNameNoPrefixError(crn, service_name, wml_service_name)

        if cname == 'bluemix':
            if platform_qa_url_host in self.service_url:
                return wml_qa
            else:
                return wml_prod.format(location)
        elif cname == 'staging':
            if service_name == wml_service_name:
                return wml_staging.format('us-south')
            elif service_name == wml_service_name_devops:
                return wml_staging.format('wml-fvt')
            else:
                raise WmlServiceNameUnknownTypeError(crn, service_name)
        else:
            raise WmlServiceCNameNotValidError(crn, cname, ['bluemix', 'staging'])

    def get_storage_credentials(
        self,
        cpd_scope: Optional[Union[str, CpdScope]] = None
    ) -> dict:
        cpd_scope = self._get_as_scope(cpd_scope)

        scope_response = self.get_scope(cpd_scope)
        props = self.get_storage_properties(scope_response)

        cos_credentials = StorageCredentialsFull.from_storage_properties(props)
        return cos_credentials.to_dict()


    def _get_as_scope(
            self,
            cpd_scope: Optional[Union[str, CpdScope]]
    ) -> CpdScope:
        # if cpd_scope is None --- get it from env-var
        if cpd_scope is None:
            cpd_scope = os.environ.get('OF_CPD_SCOPE', None)
            if cpd_scope is None:
                raise MissingValueError("OF_CPD_SCOPE")

        # if cpd_scope is str --- parse it
        if isinstance(cpd_scope, str):
            try:
                cpd_scope = CpdScope.from_string(cpd_scope)
            except Exception as ex:
                raise OfCpdPathError(cpd_scope, reason = ex)

        # now it should be CpdScope
        validate_type(cpd_scope, "OF_CPD_SCOPE", CpdScope)
        return cpd_scope


    def store_results(
        self,
        outputs: Mapping[str, Any] # output name -> path value
    ) -> DetailedResponse:
        validate_type(outputs, "outputs", abc.Mapping)
        for key, value in outputs.items():
            validate_type(key, f"outputs[...]", str)

        cpd_scope = os.environ.get('OF_CPD_SCOPE', None)
        if cpd_scope is None:
            raise MissingValueError("OF_CPD_SCOPE")
        try:
            cpd_scope = CpdScope.from_string(cpd_scope)
        except Exception as ex:
            raise OfCpdPathError(cpd_scope, reason = ex)
        validate_type(cpd_scope, "OF_CPD_SCOPE", CpdScope)

        scope = self.get_scope(cpd_scope)
        props = self.get_storage_properties(scope)

        cos_config = StorageConfig.from_storage_properties(props)
        cos_client = CosClient(self, cos_config)

        output_artifacts = self.get_output_artifact_map()

        response = None
        for output_name, output_value in outputs.items():
            result_key = output_artifacts[output_name]
            response = cos_client.store_result(result_key, output_value)
            if response.status not in range(200, 300):
                raise ApiException(response.status, http_response=response)

        if response is not None:
            response.url = urljoin(cos_config.endpoint, cos_config.bucket_name)
            response.headers = {}
            response = DetailedResponse(response = response)
        else:
            response = DetailedResponse(
                response=responses.Response(
                    'PUT',
                    url = urljoin(cos_config.endpoint, cos_config.bucket_name),
                    status = 200
                ),
                status_code = 200
            )
        return response


@attrs(auto_attribs=True, kw_only=True, frozen=True)
class WmlCredentials:
    guid: str
    name: str
    url: str
    apikey: str

    def to_dict(self) -> dict:
        return attr.asdict(self)


@attrs(auto_attribs=True, kw_only=True, frozen=True)
class StorageCredentials:
    api_key: str
    service_id: str
    access_key_id: Optional[str] = None
    secret_access_key: Optional[str] = None
    resource_key_crn: Optional[str] = None

    def to_dict(self) -> dict:
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'StorageCredentials':
        fields = dict()
        for field_name, field in fields_dict(cls).items():
            field_required = field.default is NOTHING
            value = get_credentials_field(data, field_name, str, mandatory=field_required)
            if value is not None:
                fields[field_name] = value

        return cls(
            api_key = fields["api_key"],
            service_id = fields["service_id"],
            access_key_id = fields.get("access_key_id", None),
            secret_access_key = fields.get("secret_access_key", None),
            resource_key_crn = fields.get("resource_key_crn", None)
        )

@attrs(auto_attribs=True, kw_only=True, frozen=True)
class StorageCredentialsFull:
    admin: Optional[StorageCredentials] = None
    editor: Optional[StorageCredentials] = None
    viewer: StorageCredentials

    def to_dict(self) -> dict:
        return attr.asdict(self)

    @classmethod
    def from_storage_properties(cls, props: dict) -> 'StorageCredentialsFull':
        fields = dict()
        for field_name, field in fields_dict(cls).items():
            field_required = field.default is NOTHING
            path = "credentials." + field_name
            value = get_storage_config_field(props, path, dict, mandatory=field_required)
            if value is not None:
                fields[field_name] = StorageCredentials.from_dict(value)

        return cls(
            admin = fields.get("admin", None),
            editor = fields.get("editor", None),
            viewer = fields["viewer"],
        )

@attrs(auto_attribs=True, kw_only=True, frozen=True)
class StorageConfig:
    DEFAULT_COS_AUTH_ENDPOINT: ClassVar[str] = 'https://iam.cloud.ibm.com/identity/token'

    endpoint: str
    api_key_id: str
    instance_crn: str
    auth_endpoint: str
    bucket_name: str

    @classmethod
    def from_storage_properties(cls, props: dict) -> 'StorageConfig':
        fields_to_paths = {
            "endpoint": "endpoint_url",
            "bucket_name": "bucket_name",
            "api_key_id": "credentials.editor.api_key",
            "instance_crn": "credentials.editor.resource_key_crn",
        }
        fields = dict()
        for field_name, field_path in fields_to_paths.items():
            fields[field_name] = get_storage_config_field(props, field_path, str)
        fields["auth_endpoint"] = cls._get_auth_endpoint_from_instance_crn(fields["instance_crn"])

        return cls(
            endpoint = fields["endpoint"],
            api_key_id = fields["api_key_id"],
            instance_crn = fields["instance_crn"],
            auth_endpoint = fields["auth_endpoint"],
            bucket_name = fields["bucket_name"]
        )

    @classmethod
    def _get_auth_endpoint_from_instance_crn(cls, instance_crn: str) -> str:
        parts = instance_crn.split(":")
        cname = parts[2]
        cname_to_auth_endpoint = {
            'bluemix': 'https://iam.cloud.ibm.com/identity/token',
            'prod': 'https://iam.cloud.ibm.com/identity/token',
            'staging': 'https://iam.test.cloud.ibm.com/identity/token',
            'dev': 'https://iam.test.cloud.ibm.com/identity/token',
        }
        auth_endpoint = cname_to_auth_endpoint.get(cname, cls.DEFAULT_COS_AUTH_ENDPOINT)
        validate_type(auth_endpoint, "auth_endpoint", str)
        return auth_endpoint


class CosClient:
    def __init__(
        self,
        cpd_orchestration: CPDOrchestration,
        config: StorageConfig
    ):
        validate_type(cpd_orchestration, "cpd_orchestration", CPDOrchestration)
        validate_type(config, "config", StorageConfig)

        self.cpd_orchestration = cpd_orchestration
        self.config = config
        self.cos = ibm_boto3.resource(
            "s3",
            ibm_api_key_id=config.api_key_id,
            ibm_service_instance_id=config.instance_crn,
            ibm_auth_endpoint=config.auth_endpoint,
            config=Config(signature_version="oauth"),
            endpoint_url=config.endpoint
        )

    def store_result(self, output_key: str, value: Any) -> responses.Response:
        validate_type(output_key, "output_key", str)
        response = self.cos.Object(self.config.bucket_name, output_key).put(
            Body=str(value)
        )
        return responses.Response(
            method = 'PUT',
            url = urljoin(urljoin(self.config.endpoint, self.config.bucket_name), output_key),
            status = response['ResponseMetadata']['HTTPStatusCode'],
            headers = response['ResponseMetadata']['HTTPHeaders']
        )
