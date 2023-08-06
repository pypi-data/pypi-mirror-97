"""
Main interface for secretsmanager service type definitions.

Usage::

    ```python
    from mypy_boto3_secretsmanager.type_defs import ReplicationStatusTypeTypeDef

    data: ReplicationStatusTypeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Dict, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ReplicationStatusTypeTypeDef",
    "RotationRulesTypeTypeDef",
    "SecretListEntryTypeDef",
    "SecretVersionsListEntryTypeDef",
    "TagTypeDef",
    "ValidationErrorsEntryTypeDef",
    "CancelRotateSecretResponseTypeDef",
    "CreateSecretResponseTypeDef",
    "DeleteResourcePolicyResponseTypeDef",
    "DeleteSecretResponseTypeDef",
    "DescribeSecretResponseTypeDef",
    "FilterTypeDef",
    "GetRandomPasswordResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "GetSecretValueResponseTypeDef",
    "ListSecretVersionIdsResponseTypeDef",
    "ListSecretsResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutResourcePolicyResponseTypeDef",
    "PutSecretValueResponseTypeDef",
    "RemoveRegionsFromReplicationResponseTypeDef",
    "ReplicaRegionTypeTypeDef",
    "ReplicateSecretToRegionsResponseTypeDef",
    "RestoreSecretResponseTypeDef",
    "RotateSecretResponseTypeDef",
    "StopReplicationToReplicaResponseTypeDef",
    "UpdateSecretResponseTypeDef",
    "UpdateSecretVersionStageResponseTypeDef",
    "ValidateResourcePolicyResponseTypeDef",
)

ReplicationStatusTypeTypeDef = TypedDict(
    "ReplicationStatusTypeTypeDef",
    {
        "Region": str,
        "KmsKeyId": str,
        "Status": Literal["InSync", "Failed", "InProgress"],
        "StatusMessage": str,
        "LastAccessedDate": datetime,
    },
    total=False,
)

RotationRulesTypeTypeDef = TypedDict(
    "RotationRulesTypeTypeDef", {"AutomaticallyAfterDays": int}, total=False
)

SecretListEntryTypeDef = TypedDict(
    "SecretListEntryTypeDef",
    {
        "ARN": str,
        "Name": str,
        "Description": str,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaARN": str,
        "RotationRules": "RotationRulesTypeTypeDef",
        "LastRotatedDate": datetime,
        "LastChangedDate": datetime,
        "LastAccessedDate": datetime,
        "DeletedDate": datetime,
        "Tags": List["TagTypeDef"],
        "SecretVersionsToStages": Dict[str, List[str]],
        "OwningService": str,
        "CreatedDate": datetime,
        "PrimaryRegion": str,
    },
    total=False,
)

SecretVersionsListEntryTypeDef = TypedDict(
    "SecretVersionsListEntryTypeDef",
    {
        "VersionId": str,
        "VersionStages": List[str],
        "LastAccessedDate": datetime,
        "CreatedDate": datetime,
    },
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ValidationErrorsEntryTypeDef = TypedDict(
    "ValidationErrorsEntryTypeDef", {"CheckName": str, "ErrorMessage": str}, total=False
)

CancelRotateSecretResponseTypeDef = TypedDict(
    "CancelRotateSecretResponseTypeDef", {"ARN": str, "Name": str, "VersionId": str}, total=False
)

CreateSecretResponseTypeDef = TypedDict(
    "CreateSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "ReplicationStatus": List["ReplicationStatusTypeTypeDef"],
    },
    total=False,
)

DeleteResourcePolicyResponseTypeDef = TypedDict(
    "DeleteResourcePolicyResponseTypeDef", {"ARN": str, "Name": str}, total=False
)

DeleteSecretResponseTypeDef = TypedDict(
    "DeleteSecretResponseTypeDef", {"ARN": str, "Name": str, "DeletionDate": datetime}, total=False
)

DescribeSecretResponseTypeDef = TypedDict(
    "DescribeSecretResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "Description": str,
        "KmsKeyId": str,
        "RotationEnabled": bool,
        "RotationLambdaARN": str,
        "RotationRules": "RotationRulesTypeTypeDef",
        "LastRotatedDate": datetime,
        "LastChangedDate": datetime,
        "LastAccessedDate": datetime,
        "DeletedDate": datetime,
        "Tags": List["TagTypeDef"],
        "VersionIdsToStages": Dict[str, List[str]],
        "OwningService": str,
        "CreatedDate": datetime,
        "PrimaryRegion": str,
        "ReplicationStatus": List["ReplicationStatusTypeTypeDef"],
    },
    total=False,
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Key": Literal["description", "name", "tag-key", "tag-value", "primary-region", "all"],
        "Values": List[str],
    },
    total=False,
)

GetRandomPasswordResponseTypeDef = TypedDict(
    "GetRandomPasswordResponseTypeDef", {"RandomPassword": str}, total=False
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {"ARN": str, "Name": str, "ResourcePolicy": str},
    total=False,
)

GetSecretValueResponseTypeDef = TypedDict(
    "GetSecretValueResponseTypeDef",
    {
        "ARN": str,
        "Name": str,
        "VersionId": str,
        "SecretBinary": Union[bytes, IO[bytes]],
        "SecretString": str,
        "VersionStages": List[str],
        "CreatedDate": datetime,
    },
    total=False,
)

ListSecretVersionIdsResponseTypeDef = TypedDict(
    "ListSecretVersionIdsResponseTypeDef",
    {"Versions": List["SecretVersionsListEntryTypeDef"], "NextToken": str, "ARN": str, "Name": str},
    total=False,
)

ListSecretsResponseTypeDef = TypedDict(
    "ListSecretsResponseTypeDef",
    {"SecretList": List["SecretListEntryTypeDef"], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutResourcePolicyResponseTypeDef = TypedDict(
    "PutResourcePolicyResponseTypeDef", {"ARN": str, "Name": str}, total=False
)

PutSecretValueResponseTypeDef = TypedDict(
    "PutSecretValueResponseTypeDef",
    {"ARN": str, "Name": str, "VersionId": str, "VersionStages": List[str]},
    total=False,
)

RemoveRegionsFromReplicationResponseTypeDef = TypedDict(
    "RemoveRegionsFromReplicationResponseTypeDef",
    {"ARN": str, "ReplicationStatus": List["ReplicationStatusTypeTypeDef"]},
    total=False,
)

ReplicaRegionTypeTypeDef = TypedDict(
    "ReplicaRegionTypeTypeDef", {"Region": str, "KmsKeyId": str}, total=False
)

ReplicateSecretToRegionsResponseTypeDef = TypedDict(
    "ReplicateSecretToRegionsResponseTypeDef",
    {"ARN": str, "ReplicationStatus": List["ReplicationStatusTypeTypeDef"]},
    total=False,
)

RestoreSecretResponseTypeDef = TypedDict(
    "RestoreSecretResponseTypeDef", {"ARN": str, "Name": str}, total=False
)

RotateSecretResponseTypeDef = TypedDict(
    "RotateSecretResponseTypeDef", {"ARN": str, "Name": str, "VersionId": str}, total=False
)

StopReplicationToReplicaResponseTypeDef = TypedDict(
    "StopReplicationToReplicaResponseTypeDef", {"ARN": str}, total=False
)

UpdateSecretResponseTypeDef = TypedDict(
    "UpdateSecretResponseTypeDef", {"ARN": str, "Name": str, "VersionId": str}, total=False
)

UpdateSecretVersionStageResponseTypeDef = TypedDict(
    "UpdateSecretVersionStageResponseTypeDef", {"ARN": str, "Name": str}, total=False
)

ValidateResourcePolicyResponseTypeDef = TypedDict(
    "ValidateResourcePolicyResponseTypeDef",
    {"PolicyValidationPassed": bool, "ValidationErrors": List["ValidationErrorsEntryTypeDef"]},
    total=False,
)
