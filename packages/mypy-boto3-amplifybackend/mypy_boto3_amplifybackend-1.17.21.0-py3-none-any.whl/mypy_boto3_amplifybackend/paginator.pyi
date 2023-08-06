"""
Main interface for amplifybackend service client paginators.

Usage::

    ```python
    import boto3

    from mypy_boto3_amplifybackend import AmplifyBackendClient
    from mypy_boto3_amplifybackend.paginator import (
        ListBackendJobsPaginator,
    )

    client: AmplifyBackendClient = boto3.client("amplifybackend")

    list_backend_jobs_paginator: ListBackendJobsPaginator = client.get_paginator("list_backend_jobs")
    ```
"""
from typing import Iterator

from botocore.paginate import Paginator as Boto3Paginator

from mypy_boto3_amplifybackend.type_defs import (
    ListBackendJobsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListBackendJobsPaginator",)

class ListBackendJobsPaginator(Boto3Paginator):
    """
    [Paginator.ListBackendJobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs)
    """

    def paginate(
        self,
        AppId: str,
        BackendEnvironmentName: str,
        JobId: str = None,
        Operation: str = None,
        Status: str = None,
        PaginationConfig: PaginatorConfigTypeDef = None,
    ) -> Iterator[ListBackendJobsResponseTypeDef]:
        """
        [ListBackendJobs.paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.21/reference/services/amplifybackend.html#AmplifyBackend.Paginator.ListBackendJobs.paginate)
        """
