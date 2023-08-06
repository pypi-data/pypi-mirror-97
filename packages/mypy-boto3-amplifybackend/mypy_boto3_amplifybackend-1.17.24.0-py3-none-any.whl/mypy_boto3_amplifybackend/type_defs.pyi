"""
Main interface for amplifybackend service type definitions.

Usage::

    ```python
    from mypy_boto3_amplifybackend.type_defs import BackendAPIAppSyncAuthSettingsTypeDef

    data: BackendAPIAppSyncAuthSettingsTypeDef = {...}
    ```
"""
import sys
from typing import List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "BackendAPIAppSyncAuthSettingsTypeDef",
    "BackendAPIAuthTypeTypeDef",
    "BackendAPIConflictResolutionTypeDef",
    "BackendAPIResourceConfigTypeDef",
    "BackendAuthSocialProviderConfigTypeDef",
    "BackendJobRespObjTypeDef",
    "CreateBackendAuthForgotPasswordConfigTypeDef",
    "CreateBackendAuthIdentityPoolConfigTypeDef",
    "CreateBackendAuthMFAConfigTypeDef",
    "CreateBackendAuthOAuthConfigTypeDef",
    "CreateBackendAuthPasswordPolicyConfigTypeDef",
    "CreateBackendAuthResourceConfigTypeDef",
    "CreateBackendAuthUserPoolConfigTypeDef",
    "EmailSettingsTypeDef",
    "LoginAuthConfigReqObjTypeDef",
    "SettingsTypeDef",
    "SmsSettingsTypeDef",
    "SocialProviderSettingsTypeDef",
    "UpdateBackendAuthForgotPasswordConfigTypeDef",
    "UpdateBackendAuthIdentityPoolConfigTypeDef",
    "UpdateBackendAuthMFAConfigTypeDef",
    "UpdateBackendAuthOAuthConfigTypeDef",
    "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    "UpdateBackendAuthUserPoolConfigTypeDef",
    "CloneBackendResponseTypeDef",
    "CreateBackendAPIResponseTypeDef",
    "CreateBackendAuthResponseTypeDef",
    "CreateBackendConfigResponseTypeDef",
    "CreateBackendResponseTypeDef",
    "CreateTokenResponseTypeDef",
    "DeleteBackendAPIResponseTypeDef",
    "DeleteBackendAuthResponseTypeDef",
    "DeleteBackendResponseTypeDef",
    "DeleteTokenResponseTypeDef",
    "GenerateBackendAPIModelsResponseTypeDef",
    "GetBackendAPIModelsResponseTypeDef",
    "GetBackendAPIResponseTypeDef",
    "GetBackendAuthResponseTypeDef",
    "GetBackendJobResponseTypeDef",
    "GetBackendResponseTypeDef",
    "GetTokenResponseTypeDef",
    "ListBackendJobsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "RemoveAllBackendsResponseTypeDef",
    "RemoveBackendConfigResponseTypeDef",
    "UpdateBackendAPIResponseTypeDef",
    "UpdateBackendAuthResourceConfigTypeDef",
    "UpdateBackendAuthResponseTypeDef",
    "UpdateBackendConfigResponseTypeDef",
    "UpdateBackendJobResponseTypeDef",
)

BackendAPIAppSyncAuthSettingsTypeDef = TypedDict(
    "BackendAPIAppSyncAuthSettingsTypeDef",
    {
        "CognitoUserPoolId": str,
        "Description": str,
        "ExpirationTime": float,
        "OpenIDAuthTTL": str,
        "OpenIDClientId": str,
        "OpenIDIatTTL": str,
        "OpenIDIssueURL": str,
        "OpenIDProviderName": str,
    },
    total=False,
)

BackendAPIAuthTypeTypeDef = TypedDict(
    "BackendAPIAuthTypeTypeDef",
    {
        "Mode": Literal["API_KEY", "AWS_IAM", "AMAZON_COGNITO_USER_POOLS", "OPENID_CONNECT"],
        "Settings": "BackendAPIAppSyncAuthSettingsTypeDef",
    },
    total=False,
)

BackendAPIConflictResolutionTypeDef = TypedDict(
    "BackendAPIConflictResolutionTypeDef",
    {"ResolutionStrategy": Literal["OPTIMISTIC_CONCURRENCY", "LAMBDA", "AUTOMERGE", "NONE"]},
    total=False,
)

BackendAPIResourceConfigTypeDef = TypedDict(
    "BackendAPIResourceConfigTypeDef",
    {
        "AdditionalAuthTypes": List["BackendAPIAuthTypeTypeDef"],
        "ApiName": str,
        "ConflictResolution": "BackendAPIConflictResolutionTypeDef",
        "DefaultAuthType": "BackendAPIAuthTypeTypeDef",
        "Service": str,
        "TransformSchema": str,
    },
    total=False,
)

BackendAuthSocialProviderConfigTypeDef = TypedDict(
    "BackendAuthSocialProviderConfigTypeDef", {"ClientId": str, "ClientSecret": str}, total=False
)

_RequiredBackendJobRespObjTypeDef = TypedDict(
    "_RequiredBackendJobRespObjTypeDef", {"AppId": str, "BackendEnvironmentName": str}
)
_OptionalBackendJobRespObjTypeDef = TypedDict(
    "_OptionalBackendJobRespObjTypeDef",
    {
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
    },
    total=False,
)

class BackendJobRespObjTypeDef(
    _RequiredBackendJobRespObjTypeDef, _OptionalBackendJobRespObjTypeDef
):
    pass

_RequiredCreateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthForgotPasswordConfigTypeDef",
    {"DeliveryMethod": Literal["EMAIL", "SMS"]},
)
_OptionalCreateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthForgotPasswordConfigTypeDef",
    {"EmailSettings": "EmailSettingsTypeDef", "SmsSettings": "SmsSettingsTypeDef"},
    total=False,
)

class CreateBackendAuthForgotPasswordConfigTypeDef(
    _RequiredCreateBackendAuthForgotPasswordConfigTypeDef,
    _OptionalCreateBackendAuthForgotPasswordConfigTypeDef,
):
    pass

CreateBackendAuthIdentityPoolConfigTypeDef = TypedDict(
    "CreateBackendAuthIdentityPoolConfigTypeDef",
    {"IdentityPoolName": str, "UnauthenticatedLogin": bool},
)

_RequiredCreateBackendAuthMFAConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthMFAConfigTypeDef", {"MFAMode": Literal["ON", "OFF", "OPTIONAL"]}
)
_OptionalCreateBackendAuthMFAConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthMFAConfigTypeDef", {"Settings": "SettingsTypeDef"}, total=False
)

class CreateBackendAuthMFAConfigTypeDef(
    _RequiredCreateBackendAuthMFAConfigTypeDef, _OptionalCreateBackendAuthMFAConfigTypeDef
):
    pass

_RequiredCreateBackendAuthOAuthConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthOAuthConfigTypeDef",
    {
        "OAuthGrantType": Literal["CODE", "IMPLICIT"],
        "OAuthScopes": List[
            Literal["PHONE", "EMAIL", "OPENID", "PROFILE", "AWS_COGNITO_SIGNIN_USER_ADMIN"]
        ],
        "RedirectSignInURIs": List[str],
        "RedirectSignOutURIs": List[str],
    },
)
_OptionalCreateBackendAuthOAuthConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthOAuthConfigTypeDef",
    {"DomainPrefix": str, "SocialProviderSettings": "SocialProviderSettingsTypeDef"},
    total=False,
)

class CreateBackendAuthOAuthConfigTypeDef(
    _RequiredCreateBackendAuthOAuthConfigTypeDef, _OptionalCreateBackendAuthOAuthConfigTypeDef
):
    pass

_RequiredCreateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthPasswordPolicyConfigTypeDef", {"MinimumLength": float}
)
_OptionalCreateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthPasswordPolicyConfigTypeDef",
    {
        "AdditionalConstraints": List[
            Literal["REQUIRE_DIGIT", "REQUIRE_LOWERCASE", "REQUIRE_SYMBOL", "REQUIRE_UPPERCASE"]
        ]
    },
    total=False,
)

class CreateBackendAuthPasswordPolicyConfigTypeDef(
    _RequiredCreateBackendAuthPasswordPolicyConfigTypeDef,
    _OptionalCreateBackendAuthPasswordPolicyConfigTypeDef,
):
    pass

_RequiredCreateBackendAuthResourceConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthResourceConfigTypeDef",
    {
        "AuthResources": Literal["USER_POOL_ONLY", "IDENTITY_POOL_AND_USER_POOL"],
        "Service": Literal["COGNITO"],
        "UserPoolConfigs": "CreateBackendAuthUserPoolConfigTypeDef",
    },
)
_OptionalCreateBackendAuthResourceConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthResourceConfigTypeDef",
    {"IdentityPoolConfigs": "CreateBackendAuthIdentityPoolConfigTypeDef"},
    total=False,
)

class CreateBackendAuthResourceConfigTypeDef(
    _RequiredCreateBackendAuthResourceConfigTypeDef, _OptionalCreateBackendAuthResourceConfigTypeDef
):
    pass

_RequiredCreateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "_RequiredCreateBackendAuthUserPoolConfigTypeDef",
    {
        "RequiredSignUpAttributes": List[
            Literal[
                "ADDRESS",
                "BIRTHDATE",
                "EMAIL",
                "FAMILY_NAME",
                "GENDER",
                "GIVEN_NAME",
                "LOCALE",
                "MIDDLE_NAME",
                "NAME",
                "NICKNAME",
                "PHONE_NUMBER",
                "PICTURE",
                "PREFERRED_USERNAME",
                "PROFILE",
                "UPDATED_AT",
                "WEBSITE",
                "ZONE_INFO",
            ]
        ],
        "SignInMethod": Literal["EMAIL", "EMAIL_AND_PHONE_NUMBER", "PHONE_NUMBER", "USERNAME"],
        "UserPoolName": str,
    },
)
_OptionalCreateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "_OptionalCreateBackendAuthUserPoolConfigTypeDef",
    {
        "ForgotPassword": "CreateBackendAuthForgotPasswordConfigTypeDef",
        "Mfa": "CreateBackendAuthMFAConfigTypeDef",
        "OAuth": "CreateBackendAuthOAuthConfigTypeDef",
        "PasswordPolicy": "CreateBackendAuthPasswordPolicyConfigTypeDef",
    },
    total=False,
)

class CreateBackendAuthUserPoolConfigTypeDef(
    _RequiredCreateBackendAuthUserPoolConfigTypeDef, _OptionalCreateBackendAuthUserPoolConfigTypeDef
):
    pass

EmailSettingsTypeDef = TypedDict(
    "EmailSettingsTypeDef", {"EmailMessage": str, "EmailSubject": str}, total=False
)

LoginAuthConfigReqObjTypeDef = TypedDict(
    "LoginAuthConfigReqObjTypeDef",
    {
        "AwsCognitoIdentityPoolId": str,
        "AwsCognitoRegion": str,
        "AwsUserPoolsId": str,
        "AwsUserPoolsWebClientId": str,
    },
    total=False,
)

SettingsTypeDef = TypedDict(
    "SettingsTypeDef", {"MfaTypes": List[Literal["SMS", "TOTP"]], "SmsMessage": str}, total=False
)

SmsSettingsTypeDef = TypedDict("SmsSettingsTypeDef", {"SmsMessage": str}, total=False)

SocialProviderSettingsTypeDef = TypedDict(
    "SocialProviderSettingsTypeDef",
    {
        "Facebook": "BackendAuthSocialProviderConfigTypeDef",
        "Google": "BackendAuthSocialProviderConfigTypeDef",
        "LoginWithAmazon": "BackendAuthSocialProviderConfigTypeDef",
    },
    total=False,
)

UpdateBackendAuthForgotPasswordConfigTypeDef = TypedDict(
    "UpdateBackendAuthForgotPasswordConfigTypeDef",
    {
        "DeliveryMethod": Literal["EMAIL", "SMS"],
        "EmailSettings": "EmailSettingsTypeDef",
        "SmsSettings": "SmsSettingsTypeDef",
    },
    total=False,
)

UpdateBackendAuthIdentityPoolConfigTypeDef = TypedDict(
    "UpdateBackendAuthIdentityPoolConfigTypeDef", {"UnauthenticatedLogin": bool}, total=False
)

UpdateBackendAuthMFAConfigTypeDef = TypedDict(
    "UpdateBackendAuthMFAConfigTypeDef",
    {"MFAMode": Literal["ON", "OFF", "OPTIONAL"], "Settings": "SettingsTypeDef"},
    total=False,
)

UpdateBackendAuthOAuthConfigTypeDef = TypedDict(
    "UpdateBackendAuthOAuthConfigTypeDef",
    {
        "DomainPrefix": str,
        "OAuthGrantType": Literal["CODE", "IMPLICIT"],
        "OAuthScopes": List[
            Literal["PHONE", "EMAIL", "OPENID", "PROFILE", "AWS_COGNITO_SIGNIN_USER_ADMIN"]
        ],
        "RedirectSignInURIs": List[str],
        "RedirectSignOutURIs": List[str],
        "SocialProviderSettings": "SocialProviderSettingsTypeDef",
    },
    total=False,
)

UpdateBackendAuthPasswordPolicyConfigTypeDef = TypedDict(
    "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    {
        "AdditionalConstraints": List[
            Literal["REQUIRE_DIGIT", "REQUIRE_LOWERCASE", "REQUIRE_SYMBOL", "REQUIRE_UPPERCASE"]
        ],
        "MinimumLength": float,
    },
    total=False,
)

UpdateBackendAuthUserPoolConfigTypeDef = TypedDict(
    "UpdateBackendAuthUserPoolConfigTypeDef",
    {
        "ForgotPassword": "UpdateBackendAuthForgotPasswordConfigTypeDef",
        "Mfa": "UpdateBackendAuthMFAConfigTypeDef",
        "OAuth": "UpdateBackendAuthOAuthConfigTypeDef",
        "PasswordPolicy": "UpdateBackendAuthPasswordPolicyConfigTypeDef",
    },
    total=False,
)

CloneBackendResponseTypeDef = TypedDict(
    "CloneBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

CreateBackendAPIResponseTypeDef = TypedDict(
    "CreateBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

CreateBackendAuthResponseTypeDef = TypedDict(
    "CreateBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

CreateBackendConfigResponseTypeDef = TypedDict(
    "CreateBackendConfigResponseTypeDef",
    {"AppId": str, "BackendEnvironmentName": str, "JobId": str, "Status": str},
    total=False,
)

CreateBackendResponseTypeDef = TypedDict(
    "CreateBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

CreateTokenResponseTypeDef = TypedDict(
    "CreateTokenResponseTypeDef",
    {"AppId": str, "ChallengeCode": str, "SessionId": str, "Ttl": str},
    total=False,
)

DeleteBackendAPIResponseTypeDef = TypedDict(
    "DeleteBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

DeleteBackendAuthResponseTypeDef = TypedDict(
    "DeleteBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

DeleteBackendResponseTypeDef = TypedDict(
    "DeleteBackendResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

DeleteTokenResponseTypeDef = TypedDict(
    "DeleteTokenResponseTypeDef", {"IsSuccess": bool}, total=False
)

GenerateBackendAPIModelsResponseTypeDef = TypedDict(
    "GenerateBackendAPIModelsResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

GetBackendAPIModelsResponseTypeDef = TypedDict(
    "GetBackendAPIModelsResponseTypeDef",
    {"Models": str, "Status": Literal["LATEST", "STALE"]},
    total=False,
)

GetBackendAPIResponseTypeDef = TypedDict(
    "GetBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "ResourceConfig": "BackendAPIResourceConfigTypeDef",
        "ResourceName": str,
    },
    total=False,
)

GetBackendAuthResponseTypeDef = TypedDict(
    "GetBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "ResourceConfig": "CreateBackendAuthResourceConfigTypeDef",
        "ResourceName": str,
    },
    total=False,
)

GetBackendJobResponseTypeDef = TypedDict(
    "GetBackendJobResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
    },
    total=False,
)

GetBackendResponseTypeDef = TypedDict(
    "GetBackendResponseTypeDef",
    {
        "AmplifyMetaConfig": str,
        "AppId": str,
        "AppName": str,
        "BackendEnvironmentList": List[str],
        "BackendEnvironmentName": str,
        "Error": str,
    },
    total=False,
)

GetTokenResponseTypeDef = TypedDict(
    "GetTokenResponseTypeDef",
    {"AppId": str, "ChallengeCode": str, "SessionId": str, "Ttl": str},
    total=False,
)

ListBackendJobsResponseTypeDef = TypedDict(
    "ListBackendJobsResponseTypeDef",
    {"Jobs": List["BackendJobRespObjTypeDef"], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

RemoveAllBackendsResponseTypeDef = TypedDict(
    "RemoveAllBackendsResponseTypeDef",
    {"AppId": str, "Error": str, "JobId": str, "Operation": str, "Status": str},
    total=False,
)

RemoveBackendConfigResponseTypeDef = TypedDict(
    "RemoveBackendConfigResponseTypeDef", {"Error": str}, total=False
)

UpdateBackendAPIResponseTypeDef = TypedDict(
    "UpdateBackendAPIResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

_RequiredUpdateBackendAuthResourceConfigTypeDef = TypedDict(
    "_RequiredUpdateBackendAuthResourceConfigTypeDef",
    {
        "AuthResources": Literal["USER_POOL_ONLY", "IDENTITY_POOL_AND_USER_POOL"],
        "Service": Literal["COGNITO"],
        "UserPoolConfigs": "UpdateBackendAuthUserPoolConfigTypeDef",
    },
)
_OptionalUpdateBackendAuthResourceConfigTypeDef = TypedDict(
    "_OptionalUpdateBackendAuthResourceConfigTypeDef",
    {"IdentityPoolConfigs": "UpdateBackendAuthIdentityPoolConfigTypeDef"},
    total=False,
)

class UpdateBackendAuthResourceConfigTypeDef(
    _RequiredUpdateBackendAuthResourceConfigTypeDef, _OptionalUpdateBackendAuthResourceConfigTypeDef
):
    pass

UpdateBackendAuthResponseTypeDef = TypedDict(
    "UpdateBackendAuthResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
    },
    total=False,
)

UpdateBackendConfigResponseTypeDef = TypedDict(
    "UpdateBackendConfigResponseTypeDef",
    {
        "AppId": str,
        "BackendManagerAppId": str,
        "Error": str,
        "LoginAuthConfig": "LoginAuthConfigReqObjTypeDef",
    },
    total=False,
)

UpdateBackendJobResponseTypeDef = TypedDict(
    "UpdateBackendJobResponseTypeDef",
    {
        "AppId": str,
        "BackendEnvironmentName": str,
        "CreateTime": str,
        "Error": str,
        "JobId": str,
        "Operation": str,
        "Status": str,
        "UpdateTime": str,
    },
    total=False,
)
