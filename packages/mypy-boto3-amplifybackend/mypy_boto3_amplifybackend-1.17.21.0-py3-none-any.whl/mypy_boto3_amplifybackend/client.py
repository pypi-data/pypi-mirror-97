"""
Main interface for amplifybackend service client

Usage::

    ```python
    import boto3
    from mypy_boto3_amplifybackend import AmplifyBackendClient

    client: AmplifyBackendClient = boto3.client("amplifybackend")
    ```
"""
import sys
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from mypy_boto3_amplifybackend.paginator import ListBackendJobsPaginator
from mypy_boto3_amplifybackend.type_defs import (
    BackendAPIResourceConfigTypeDef,
    CloneBackendResponseTypeDef,
    CreateBackendAPIResponseTypeDef,
    CreateBackendAuthResourceConfigTypeDef,
    CreateBackendAuthResponseTypeDef,
    CreateBackendConfigResponseTypeDef,
    CreateBackendResponseTypeDef,
    CreateTokenResponseTypeDef,
    DeleteBackendAPIResponseTypeDef,
    DeleteBackendAuthResponseTypeDef,
    DeleteBackendResponseTypeDef,
    DeleteTokenResponseTypeDef,
    GenerateBackendAPIModelsResponseTypeDef,
    GetBackendAPIModelsResponseTypeDef,
    GetBackendAPIResponseTypeDef,
    GetBackendAuthResponseTypeDef,
    GetBackendJobResponseTypeDef,
    GetBackendResponseTypeDef,
    GetTokenResponseTypeDef,
    ListBackendJobsResponseTypeDef,
    LoginAuthConfigReqObjTypeDef,
    RemoveAllBackendsResponseTypeDef,
    RemoveBackendConfigResponseTypeDef,
    UpdateBackendAPIResponseTypeDef,
    UpdateBackendAuthResourceConfigTypeDef,
    UpdateBackendAuthResponseTypeDef,
    UpdateBackendConfigResponseTypeDef,
    UpdateBackendJobResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AmplifyBackendClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class AmplifyBackendClient:
    """
    [AmplifyBackend.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.can_paginate)
        """

    def clone_backend(
        self, AppId: str, BackendEnvironmentName: str, TargetEnvironmentName: str
    ) -> CloneBackendResponseTypeDef:
        """
        [Client.clone_backend documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.clone_backend)
        """

    def create_backend(
        self,
        AppId: str,
        AppName: str,
        BackendEnvironmentName: str,
        ResourceConfig: Dict[str, Any] = None,
        ResourceName: str = None,
    ) -> CreateBackendResponseTypeDef:
        """
        [Client.create_backend documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend)
        """

    def create_backend_api(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef",
        ResourceName: str,
    ) -> CreateBackendAPIResponseTypeDef:
        """
        [Client.create_backend_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_api)
        """

    def create_backend_auth(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: "CreateBackendAuthResourceConfigTypeDef",
        ResourceName: str,
    ) -> CreateBackendAuthResponseTypeDef:
        """
        [Client.create_backend_auth documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_auth)
        """

    def create_backend_config(
        self, AppId: str, BackendManagerAppId: str = None
    ) -> CreateBackendConfigResponseTypeDef:
        """
        [Client.create_backend_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.create_backend_config)
        """

    def create_token(self, AppId: str) -> CreateTokenResponseTypeDef:
        """
        [Client.create_token documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.create_token)
        """

    def delete_backend(
        self, AppId: str, BackendEnvironmentName: str
    ) -> DeleteBackendResponseTypeDef:
        """
        [Client.delete_backend documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend)
        """

    def delete_backend_api(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = None,
    ) -> DeleteBackendAPIResponseTypeDef:
        """
        [Client.delete_backend_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend_api)
        """

    def delete_backend_auth(
        self, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> DeleteBackendAuthResponseTypeDef:
        """
        [Client.delete_backend_auth documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_backend_auth)
        """

    def delete_token(self, AppId: str, SessionId: str) -> DeleteTokenResponseTypeDef:
        """
        [Client.delete_token documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.delete_token)
        """

    def generate_backend_api_models(
        self, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GenerateBackendAPIModelsResponseTypeDef:
        """
        [Client.generate_backend_api_models documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.generate_backend_api_models)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.generate_presigned_url)
        """

    def get_backend(
        self, AppId: str, BackendEnvironmentName: str = None
    ) -> GetBackendResponseTypeDef:
        """
        [Client.get_backend documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend)
        """

    def get_backend_api(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = None,
    ) -> GetBackendAPIResponseTypeDef:
        """
        [Client.get_backend_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_api)
        """

    def get_backend_api_models(
        self, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GetBackendAPIModelsResponseTypeDef:
        """
        [Client.get_backend_api_models documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_api_models)
        """

    def get_backend_auth(
        self, AppId: str, BackendEnvironmentName: str, ResourceName: str
    ) -> GetBackendAuthResponseTypeDef:
        """
        [Client.get_backend_auth documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_auth)
        """

    def get_backend_job(
        self, AppId: str, BackendEnvironmentName: str, JobId: str
    ) -> GetBackendJobResponseTypeDef:
        """
        [Client.get_backend_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_backend_job)
        """

    def get_token(self, AppId: str, SessionId: str) -> GetTokenResponseTypeDef:
        """
        [Client.get_token documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.get_token)
        """

    def list_backend_jobs(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str = None,
        MaxResults: int = None,
        NextToken: str = None,
        Operation: str = None,
        Status: str = None,
    ) -> ListBackendJobsResponseTypeDef:
        """
        [Client.list_backend_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.list_backend_jobs)
        """

    def remove_all_backends(
        self, AppId: str, CleanAmplifyApp: bool = None
    ) -> RemoveAllBackendsResponseTypeDef:
        """
        [Client.remove_all_backends documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.remove_all_backends)
        """

    def remove_backend_config(self, AppId: str) -> RemoveBackendConfigResponseTypeDef:
        """
        [Client.remove_backend_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.remove_backend_config)
        """

    def update_backend_api(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceName: str,
        ResourceConfig: "BackendAPIResourceConfigTypeDef" = None,
    ) -> UpdateBackendAPIResponseTypeDef:
        """
        [Client.update_backend_api documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_api)
        """

    def update_backend_auth(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        ResourceConfig: UpdateBackendAuthResourceConfigTypeDef,
        ResourceName: str,
    ) -> UpdateBackendAuthResponseTypeDef:
        """
        [Client.update_backend_auth documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_auth)
        """

    def update_backend_config(
        self, AppId: str, LoginAuthConfig: "LoginAuthConfigReqObjTypeDef" = None
    ) -> UpdateBackendConfigResponseTypeDef:
        """
        [Client.update_backend_config documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_config)
        """

    def update_backend_job(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str,
        Operation: str = None,
        Status: str = None,
    ) -> UpdateBackendJobResponseTypeDef:
        """
        [Client.update_backend_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Client.update_backend_job)
        """

    def get_paginator(
        self, operation_name: Literal["list_backend_jobs"]
    ) -> ListBackendJobsPaginator:
        """
        [Paginator.ListBackendJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs)
        """
