"""
Main interface for events service type definitions.

Usage::

    ```python
    from mypy_boto3_events.type_defs import ApiDestinationTypeDef

    data: ApiDestinationTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ApiDestinationTypeDef",
    "ArchiveTypeDef",
    "AwsVpcConfigurationTypeDef",
    "BatchArrayPropertiesTypeDef",
    "BatchParametersTypeDef",
    "BatchRetryStrategyTypeDef",
    "ConnectionApiKeyAuthResponseParametersTypeDef",
    "ConnectionAuthResponseParametersTypeDef",
    "ConnectionBasicAuthResponseParametersTypeDef",
    "ConnectionBodyParameterTypeDef",
    "ConnectionHeaderParameterTypeDef",
    "ConnectionHttpParametersTypeDef",
    "ConnectionOAuthClientResponseParametersTypeDef",
    "ConnectionOAuthResponseParametersTypeDef",
    "ConnectionQueryStringParameterTypeDef",
    "ConnectionTypeDef",
    "CreateConnectionApiKeyAuthRequestParametersTypeDef",
    "CreateConnectionBasicAuthRequestParametersTypeDef",
    "CreateConnectionOAuthClientRequestParametersTypeDef",
    "CreateConnectionOAuthRequestParametersTypeDef",
    "DeadLetterConfigTypeDef",
    "EcsParametersTypeDef",
    "EventBusTypeDef",
    "EventSourceTypeDef",
    "HttpParametersTypeDef",
    "InputTransformerTypeDef",
    "KinesisParametersTypeDef",
    "NetworkConfigurationTypeDef",
    "PartnerEventSourceAccountTypeDef",
    "PartnerEventSourceTypeDef",
    "PutEventsResultEntryTypeDef",
    "PutPartnerEventsResultEntryTypeDef",
    "PutTargetsResultEntryTypeDef",
    "RedshiftDataParametersTypeDef",
    "RemoveTargetsResultEntryTypeDef",
    "ReplayDestinationTypeDef",
    "ReplayTypeDef",
    "RetryPolicyTypeDef",
    "RuleTypeDef",
    "RunCommandParametersTypeDef",
    "RunCommandTargetTypeDef",
    "SqsParametersTypeDef",
    "TagTypeDef",
    "TargetTypeDef",
    "UpdateConnectionApiKeyAuthRequestParametersTypeDef",
    "UpdateConnectionBasicAuthRequestParametersTypeDef",
    "UpdateConnectionOAuthClientRequestParametersTypeDef",
    "UpdateConnectionOAuthRequestParametersTypeDef",
    "CancelReplayResponseTypeDef",
    "ConditionTypeDef",
    "CreateApiDestinationResponseTypeDef",
    "CreateArchiveResponseTypeDef",
    "CreateConnectionAuthRequestParametersTypeDef",
    "CreateConnectionResponseTypeDef",
    "CreateEventBusResponseTypeDef",
    "CreatePartnerEventSourceResponseTypeDef",
    "DeauthorizeConnectionResponseTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DescribeApiDestinationResponseTypeDef",
    "DescribeArchiveResponseTypeDef",
    "DescribeConnectionResponseTypeDef",
    "DescribeEventBusResponseTypeDef",
    "DescribeEventSourceResponseTypeDef",
    "DescribePartnerEventSourceResponseTypeDef",
    "DescribeReplayResponseTypeDef",
    "DescribeRuleResponseTypeDef",
    "ListApiDestinationsResponseTypeDef",
    "ListArchivesResponseTypeDef",
    "ListConnectionsResponseTypeDef",
    "ListEventBusesResponseTypeDef",
    "ListEventSourcesResponseTypeDef",
    "ListPartnerEventSourceAccountsResponseTypeDef",
    "ListPartnerEventSourcesResponseTypeDef",
    "ListReplaysResponseTypeDef",
    "ListRuleNamesByTargetResponseTypeDef",
    "ListRulesResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTargetsByRuleResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutEventsRequestEntryTypeDef",
    "PutEventsResponseTypeDef",
    "PutPartnerEventsRequestEntryTypeDef",
    "PutPartnerEventsResponseTypeDef",
    "PutRuleResponseTypeDef",
    "PutTargetsResponseTypeDef",
    "RemoveTargetsResponseTypeDef",
    "StartReplayResponseTypeDef",
    "TestEventPatternResponseTypeDef",
    "UpdateApiDestinationResponseTypeDef",
    "UpdateArchiveResponseTypeDef",
    "UpdateConnectionAuthRequestParametersTypeDef",
    "UpdateConnectionResponseTypeDef",
)

ApiDestinationTypeDef = TypedDict(
    "ApiDestinationTypeDef",
    {
        "ApiDestinationArn": str,
        "Name": str,
        "ApiDestinationState": Literal["ACTIVE", "INACTIVE"],
        "ConnectionArn": str,
        "InvocationEndpoint": str,
        "HttpMethod": Literal["POST", "GET", "HEAD", "OPTIONS", "PUT", "PATCH", "DELETE"],
        "InvocationRateLimitPerSecond": int,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

ArchiveTypeDef = TypedDict(
    "ArchiveTypeDef",
    {
        "ArchiveName": str,
        "EventSourceArn": str,
        "State": Literal[
            "ENABLED", "DISABLED", "CREATING", "UPDATING", "CREATE_FAILED", "UPDATE_FAILED"
        ],
        "StateReason": str,
        "RetentionDays": int,
        "SizeBytes": int,
        "EventCount": int,
        "CreationTime": datetime,
    },
    total=False,
)

_RequiredAwsVpcConfigurationTypeDef = TypedDict(
    "_RequiredAwsVpcConfigurationTypeDef", {"Subnets": List[str]}
)
_OptionalAwsVpcConfigurationTypeDef = TypedDict(
    "_OptionalAwsVpcConfigurationTypeDef",
    {"SecurityGroups": List[str], "AssignPublicIp": Literal["ENABLED", "DISABLED"]},
    total=False,
)

class AwsVpcConfigurationTypeDef(
    _RequiredAwsVpcConfigurationTypeDef, _OptionalAwsVpcConfigurationTypeDef
):
    pass

BatchArrayPropertiesTypeDef = TypedDict("BatchArrayPropertiesTypeDef", {"Size": int}, total=False)

_RequiredBatchParametersTypeDef = TypedDict(
    "_RequiredBatchParametersTypeDef", {"JobDefinition": str, "JobName": str}
)
_OptionalBatchParametersTypeDef = TypedDict(
    "_OptionalBatchParametersTypeDef",
    {
        "ArrayProperties": "BatchArrayPropertiesTypeDef",
        "RetryStrategy": "BatchRetryStrategyTypeDef",
    },
    total=False,
)

class BatchParametersTypeDef(_RequiredBatchParametersTypeDef, _OptionalBatchParametersTypeDef):
    pass

BatchRetryStrategyTypeDef = TypedDict("BatchRetryStrategyTypeDef", {"Attempts": int}, total=False)

ConnectionApiKeyAuthResponseParametersTypeDef = TypedDict(
    "ConnectionApiKeyAuthResponseParametersTypeDef", {"ApiKeyName": str}, total=False
)

ConnectionAuthResponseParametersTypeDef = TypedDict(
    "ConnectionAuthResponseParametersTypeDef",
    {
        "BasicAuthParameters": "ConnectionBasicAuthResponseParametersTypeDef",
        "OAuthParameters": "ConnectionOAuthResponseParametersTypeDef",
        "ApiKeyAuthParameters": "ConnectionApiKeyAuthResponseParametersTypeDef",
        "InvocationHttpParameters": "ConnectionHttpParametersTypeDef",
    },
    total=False,
)

ConnectionBasicAuthResponseParametersTypeDef = TypedDict(
    "ConnectionBasicAuthResponseParametersTypeDef", {"Username": str}, total=False
)

ConnectionBodyParameterTypeDef = TypedDict(
    "ConnectionBodyParameterTypeDef", {"Key": str, "Value": str, "IsValueSecret": bool}, total=False
)

ConnectionHeaderParameterTypeDef = TypedDict(
    "ConnectionHeaderParameterTypeDef",
    {"Key": str, "Value": str, "IsValueSecret": bool},
    total=False,
)

ConnectionHttpParametersTypeDef = TypedDict(
    "ConnectionHttpParametersTypeDef",
    {
        "HeaderParameters": List["ConnectionHeaderParameterTypeDef"],
        "QueryStringParameters": List["ConnectionQueryStringParameterTypeDef"],
        "BodyParameters": List["ConnectionBodyParameterTypeDef"],
    },
    total=False,
)

ConnectionOAuthClientResponseParametersTypeDef = TypedDict(
    "ConnectionOAuthClientResponseParametersTypeDef", {"ClientID": str}, total=False
)

ConnectionOAuthResponseParametersTypeDef = TypedDict(
    "ConnectionOAuthResponseParametersTypeDef",
    {
        "ClientParameters": "ConnectionOAuthClientResponseParametersTypeDef",
        "AuthorizationEndpoint": str,
        "HttpMethod": Literal["GET", "POST", "PUT"],
        "OAuthHttpParameters": "ConnectionHttpParametersTypeDef",
    },
    total=False,
)

ConnectionQueryStringParameterTypeDef = TypedDict(
    "ConnectionQueryStringParameterTypeDef",
    {"Key": str, "Value": str, "IsValueSecret": bool},
    total=False,
)

ConnectionTypeDef = TypedDict(
    "ConnectionTypeDef",
    {
        "ConnectionArn": str,
        "Name": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "StateReason": str,
        "AuthorizationType": Literal["BASIC", "OAUTH_CLIENT_CREDENTIALS", "API_KEY"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastAuthorizedTime": datetime,
    },
    total=False,
)

CreateConnectionApiKeyAuthRequestParametersTypeDef = TypedDict(
    "CreateConnectionApiKeyAuthRequestParametersTypeDef", {"ApiKeyName": str, "ApiKeyValue": str}
)

CreateConnectionBasicAuthRequestParametersTypeDef = TypedDict(
    "CreateConnectionBasicAuthRequestParametersTypeDef", {"Username": str, "Password": str}
)

CreateConnectionOAuthClientRequestParametersTypeDef = TypedDict(
    "CreateConnectionOAuthClientRequestParametersTypeDef", {"ClientID": str, "ClientSecret": str}
)

_RequiredCreateConnectionOAuthRequestParametersTypeDef = TypedDict(
    "_RequiredCreateConnectionOAuthRequestParametersTypeDef",
    {
        "ClientParameters": "CreateConnectionOAuthClientRequestParametersTypeDef",
        "AuthorizationEndpoint": str,
        "HttpMethod": Literal["GET", "POST", "PUT"],
    },
)
_OptionalCreateConnectionOAuthRequestParametersTypeDef = TypedDict(
    "_OptionalCreateConnectionOAuthRequestParametersTypeDef",
    {"OAuthHttpParameters": "ConnectionHttpParametersTypeDef"},
    total=False,
)

class CreateConnectionOAuthRequestParametersTypeDef(
    _RequiredCreateConnectionOAuthRequestParametersTypeDef,
    _OptionalCreateConnectionOAuthRequestParametersTypeDef,
):
    pass

DeadLetterConfigTypeDef = TypedDict("DeadLetterConfigTypeDef", {"Arn": str}, total=False)

_RequiredEcsParametersTypeDef = TypedDict(
    "_RequiredEcsParametersTypeDef", {"TaskDefinitionArn": str}
)
_OptionalEcsParametersTypeDef = TypedDict(
    "_OptionalEcsParametersTypeDef",
    {
        "TaskCount": int,
        "LaunchType": Literal["EC2", "FARGATE"],
        "NetworkConfiguration": "NetworkConfigurationTypeDef",
        "PlatformVersion": str,
        "Group": str,
    },
    total=False,
)

class EcsParametersTypeDef(_RequiredEcsParametersTypeDef, _OptionalEcsParametersTypeDef):
    pass

EventBusTypeDef = TypedDict(
    "EventBusTypeDef", {"Name": str, "Arn": str, "Policy": str}, total=False
)

EventSourceTypeDef = TypedDict(
    "EventSourceTypeDef",
    {
        "Arn": str,
        "CreatedBy": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "Name": str,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

HttpParametersTypeDef = TypedDict(
    "HttpParametersTypeDef",
    {
        "PathParameterValues": List[str],
        "HeaderParameters": Dict[str, str],
        "QueryStringParameters": Dict[str, str],
    },
    total=False,
)

_RequiredInputTransformerTypeDef = TypedDict(
    "_RequiredInputTransformerTypeDef", {"InputTemplate": str}
)
_OptionalInputTransformerTypeDef = TypedDict(
    "_OptionalInputTransformerTypeDef", {"InputPathsMap": Dict[str, str]}, total=False
)

class InputTransformerTypeDef(_RequiredInputTransformerTypeDef, _OptionalInputTransformerTypeDef):
    pass

KinesisParametersTypeDef = TypedDict("KinesisParametersTypeDef", {"PartitionKeyPath": str})

NetworkConfigurationTypeDef = TypedDict(
    "NetworkConfigurationTypeDef",
    {"awsvpcConfiguration": "AwsVpcConfigurationTypeDef"},
    total=False,
)

PartnerEventSourceAccountTypeDef = TypedDict(
    "PartnerEventSourceAccountTypeDef",
    {
        "Account": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

PartnerEventSourceTypeDef = TypedDict(
    "PartnerEventSourceTypeDef", {"Arn": str, "Name": str}, total=False
)

PutEventsResultEntryTypeDef = TypedDict(
    "PutEventsResultEntryTypeDef",
    {"EventId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

PutPartnerEventsResultEntryTypeDef = TypedDict(
    "PutPartnerEventsResultEntryTypeDef",
    {"EventId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

PutTargetsResultEntryTypeDef = TypedDict(
    "PutTargetsResultEntryTypeDef",
    {"TargetId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

_RequiredRedshiftDataParametersTypeDef = TypedDict(
    "_RequiredRedshiftDataParametersTypeDef", {"Database": str, "Sql": str}
)
_OptionalRedshiftDataParametersTypeDef = TypedDict(
    "_OptionalRedshiftDataParametersTypeDef",
    {"SecretManagerArn": str, "DbUser": str, "StatementName": str, "WithEvent": bool},
    total=False,
)

class RedshiftDataParametersTypeDef(
    _RequiredRedshiftDataParametersTypeDef, _OptionalRedshiftDataParametersTypeDef
):
    pass

RemoveTargetsResultEntryTypeDef = TypedDict(
    "RemoveTargetsResultEntryTypeDef",
    {"TargetId": str, "ErrorCode": str, "ErrorMessage": str},
    total=False,
)

_RequiredReplayDestinationTypeDef = TypedDict("_RequiredReplayDestinationTypeDef", {"Arn": str})
_OptionalReplayDestinationTypeDef = TypedDict(
    "_OptionalReplayDestinationTypeDef", {"FilterArns": List[str]}, total=False
)

class ReplayDestinationTypeDef(
    _RequiredReplayDestinationTypeDef, _OptionalReplayDestinationTypeDef
):
    pass

ReplayTypeDef = TypedDict(
    "ReplayTypeDef",
    {
        "ReplayName": str,
        "EventSourceArn": str,
        "State": Literal["STARTING", "RUNNING", "CANCELLING", "COMPLETED", "CANCELLED", "FAILED"],
        "StateReason": str,
        "EventStartTime": datetime,
        "EventEndTime": datetime,
        "EventLastReplayedTime": datetime,
        "ReplayStartTime": datetime,
        "ReplayEndTime": datetime,
    },
    total=False,
)

RetryPolicyTypeDef = TypedDict(
    "RetryPolicyTypeDef",
    {"MaximumRetryAttempts": int, "MaximumEventAgeInSeconds": int},
    total=False,
)

RuleTypeDef = TypedDict(
    "RuleTypeDef",
    {
        "Name": str,
        "Arn": str,
        "EventPattern": str,
        "State": Literal["ENABLED", "DISABLED"],
        "Description": str,
        "ScheduleExpression": str,
        "RoleArn": str,
        "ManagedBy": str,
        "EventBusName": str,
    },
    total=False,
)

RunCommandParametersTypeDef = TypedDict(
    "RunCommandParametersTypeDef", {"RunCommandTargets": List["RunCommandTargetTypeDef"]}
)

RunCommandTargetTypeDef = TypedDict("RunCommandTargetTypeDef", {"Key": str, "Values": List[str]})

SqsParametersTypeDef = TypedDict("SqsParametersTypeDef", {"MessageGroupId": str}, total=False)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str})

_RequiredTargetTypeDef = TypedDict("_RequiredTargetTypeDef", {"Id": str, "Arn": str})
_OptionalTargetTypeDef = TypedDict(
    "_OptionalTargetTypeDef",
    {
        "RoleArn": str,
        "Input": str,
        "InputPath": str,
        "InputTransformer": "InputTransformerTypeDef",
        "KinesisParameters": "KinesisParametersTypeDef",
        "RunCommandParameters": "RunCommandParametersTypeDef",
        "EcsParameters": "EcsParametersTypeDef",
        "BatchParameters": "BatchParametersTypeDef",
        "SqsParameters": "SqsParametersTypeDef",
        "HttpParameters": "HttpParametersTypeDef",
        "RedshiftDataParameters": "RedshiftDataParametersTypeDef",
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "RetryPolicy": "RetryPolicyTypeDef",
    },
    total=False,
)

class TargetTypeDef(_RequiredTargetTypeDef, _OptionalTargetTypeDef):
    pass

UpdateConnectionApiKeyAuthRequestParametersTypeDef = TypedDict(
    "UpdateConnectionApiKeyAuthRequestParametersTypeDef",
    {"ApiKeyName": str, "ApiKeyValue": str},
    total=False,
)

UpdateConnectionBasicAuthRequestParametersTypeDef = TypedDict(
    "UpdateConnectionBasicAuthRequestParametersTypeDef",
    {"Username": str, "Password": str},
    total=False,
)

UpdateConnectionOAuthClientRequestParametersTypeDef = TypedDict(
    "UpdateConnectionOAuthClientRequestParametersTypeDef",
    {"ClientID": str, "ClientSecret": str},
    total=False,
)

UpdateConnectionOAuthRequestParametersTypeDef = TypedDict(
    "UpdateConnectionOAuthRequestParametersTypeDef",
    {
        "ClientParameters": "UpdateConnectionOAuthClientRequestParametersTypeDef",
        "AuthorizationEndpoint": str,
        "HttpMethod": Literal["GET", "POST", "PUT"],
        "OAuthHttpParameters": "ConnectionHttpParametersTypeDef",
    },
    total=False,
)

CancelReplayResponseTypeDef = TypedDict(
    "CancelReplayResponseTypeDef",
    {
        "ReplayArn": str,
        "State": Literal["STARTING", "RUNNING", "CANCELLING", "COMPLETED", "CANCELLED", "FAILED"],
        "StateReason": str,
    },
    total=False,
)

ConditionTypeDef = TypedDict("ConditionTypeDef", {"Type": str, "Key": str, "Value": str})

CreateApiDestinationResponseTypeDef = TypedDict(
    "CreateApiDestinationResponseTypeDef",
    {
        "ApiDestinationArn": str,
        "ApiDestinationState": Literal["ACTIVE", "INACTIVE"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

CreateArchiveResponseTypeDef = TypedDict(
    "CreateArchiveResponseTypeDef",
    {
        "ArchiveArn": str,
        "State": Literal[
            "ENABLED", "DISABLED", "CREATING", "UPDATING", "CREATE_FAILED", "UPDATE_FAILED"
        ],
        "StateReason": str,
        "CreationTime": datetime,
    },
    total=False,
)

CreateConnectionAuthRequestParametersTypeDef = TypedDict(
    "CreateConnectionAuthRequestParametersTypeDef",
    {
        "BasicAuthParameters": "CreateConnectionBasicAuthRequestParametersTypeDef",
        "OAuthParameters": "CreateConnectionOAuthRequestParametersTypeDef",
        "ApiKeyAuthParameters": "CreateConnectionApiKeyAuthRequestParametersTypeDef",
        "InvocationHttpParameters": "ConnectionHttpParametersTypeDef",
    },
    total=False,
)

CreateConnectionResponseTypeDef = TypedDict(
    "CreateConnectionResponseTypeDef",
    {
        "ConnectionArn": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

CreateEventBusResponseTypeDef = TypedDict(
    "CreateEventBusResponseTypeDef", {"EventBusArn": str}, total=False
)

CreatePartnerEventSourceResponseTypeDef = TypedDict(
    "CreatePartnerEventSourceResponseTypeDef", {"EventSourceArn": str}, total=False
)

DeauthorizeConnectionResponseTypeDef = TypedDict(
    "DeauthorizeConnectionResponseTypeDef",
    {
        "ConnectionArn": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastAuthorizedTime": datetime,
    },
    total=False,
)

DeleteConnectionResponseTypeDef = TypedDict(
    "DeleteConnectionResponseTypeDef",
    {
        "ConnectionArn": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastAuthorizedTime": datetime,
    },
    total=False,
)

DescribeApiDestinationResponseTypeDef = TypedDict(
    "DescribeApiDestinationResponseTypeDef",
    {
        "ApiDestinationArn": str,
        "Name": str,
        "Description": str,
        "ApiDestinationState": Literal["ACTIVE", "INACTIVE"],
        "ConnectionArn": str,
        "InvocationEndpoint": str,
        "HttpMethod": Literal["POST", "GET", "HEAD", "OPTIONS", "PUT", "PATCH", "DELETE"],
        "InvocationRateLimitPerSecond": int,
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

DescribeArchiveResponseTypeDef = TypedDict(
    "DescribeArchiveResponseTypeDef",
    {
        "ArchiveArn": str,
        "ArchiveName": str,
        "EventSourceArn": str,
        "Description": str,
        "EventPattern": str,
        "State": Literal[
            "ENABLED", "DISABLED", "CREATING", "UPDATING", "CREATE_FAILED", "UPDATE_FAILED"
        ],
        "StateReason": str,
        "RetentionDays": int,
        "SizeBytes": int,
        "EventCount": int,
        "CreationTime": datetime,
    },
    total=False,
)

DescribeConnectionResponseTypeDef = TypedDict(
    "DescribeConnectionResponseTypeDef",
    {
        "ConnectionArn": str,
        "Name": str,
        "Description": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "StateReason": str,
        "AuthorizationType": Literal["BASIC", "OAUTH_CLIENT_CREDENTIALS", "API_KEY"],
        "SecretArn": str,
        "AuthParameters": "ConnectionAuthResponseParametersTypeDef",
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastAuthorizedTime": datetime,
    },
    total=False,
)

DescribeEventBusResponseTypeDef = TypedDict(
    "DescribeEventBusResponseTypeDef", {"Name": str, "Arn": str, "Policy": str}, total=False
)

DescribeEventSourceResponseTypeDef = TypedDict(
    "DescribeEventSourceResponseTypeDef",
    {
        "Arn": str,
        "CreatedBy": str,
        "CreationTime": datetime,
        "ExpirationTime": datetime,
        "Name": str,
        "State": Literal["PENDING", "ACTIVE", "DELETED"],
    },
    total=False,
)

DescribePartnerEventSourceResponseTypeDef = TypedDict(
    "DescribePartnerEventSourceResponseTypeDef", {"Arn": str, "Name": str}, total=False
)

DescribeReplayResponseTypeDef = TypedDict(
    "DescribeReplayResponseTypeDef",
    {
        "ReplayName": str,
        "ReplayArn": str,
        "Description": str,
        "State": Literal["STARTING", "RUNNING", "CANCELLING", "COMPLETED", "CANCELLED", "FAILED"],
        "StateReason": str,
        "EventSourceArn": str,
        "Destination": "ReplayDestinationTypeDef",
        "EventStartTime": datetime,
        "EventEndTime": datetime,
        "EventLastReplayedTime": datetime,
        "ReplayStartTime": datetime,
        "ReplayEndTime": datetime,
    },
    total=False,
)

DescribeRuleResponseTypeDef = TypedDict(
    "DescribeRuleResponseTypeDef",
    {
        "Name": str,
        "Arn": str,
        "EventPattern": str,
        "ScheduleExpression": str,
        "State": Literal["ENABLED", "DISABLED"],
        "Description": str,
        "RoleArn": str,
        "ManagedBy": str,
        "EventBusName": str,
        "CreatedBy": str,
    },
    total=False,
)

ListApiDestinationsResponseTypeDef = TypedDict(
    "ListApiDestinationsResponseTypeDef",
    {"ApiDestinations": List["ApiDestinationTypeDef"], "NextToken": str},
    total=False,
)

ListArchivesResponseTypeDef = TypedDict(
    "ListArchivesResponseTypeDef",
    {"Archives": List["ArchiveTypeDef"], "NextToken": str},
    total=False,
)

ListConnectionsResponseTypeDef = TypedDict(
    "ListConnectionsResponseTypeDef",
    {"Connections": List["ConnectionTypeDef"], "NextToken": str},
    total=False,
)

ListEventBusesResponseTypeDef = TypedDict(
    "ListEventBusesResponseTypeDef",
    {"EventBuses": List["EventBusTypeDef"], "NextToken": str},
    total=False,
)

ListEventSourcesResponseTypeDef = TypedDict(
    "ListEventSourcesResponseTypeDef",
    {"EventSources": List["EventSourceTypeDef"], "NextToken": str},
    total=False,
)

ListPartnerEventSourceAccountsResponseTypeDef = TypedDict(
    "ListPartnerEventSourceAccountsResponseTypeDef",
    {"PartnerEventSourceAccounts": List["PartnerEventSourceAccountTypeDef"], "NextToken": str},
    total=False,
)

ListPartnerEventSourcesResponseTypeDef = TypedDict(
    "ListPartnerEventSourcesResponseTypeDef",
    {"PartnerEventSources": List["PartnerEventSourceTypeDef"], "NextToken": str},
    total=False,
)

ListReplaysResponseTypeDef = TypedDict(
    "ListReplaysResponseTypeDef", {"Replays": List["ReplayTypeDef"], "NextToken": str}, total=False
)

ListRuleNamesByTargetResponseTypeDef = TypedDict(
    "ListRuleNamesByTargetResponseTypeDef", {"RuleNames": List[str], "NextToken": str}, total=False
)

ListRulesResponseTypeDef = TypedDict(
    "ListRulesResponseTypeDef", {"Rules": List["RuleTypeDef"], "NextToken": str}, total=False
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"Tags": List["TagTypeDef"]}, total=False
)

ListTargetsByRuleResponseTypeDef = TypedDict(
    "ListTargetsByRuleResponseTypeDef",
    {"Targets": List["TargetTypeDef"], "NextToken": str},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutEventsRequestEntryTypeDef = TypedDict(
    "PutEventsRequestEntryTypeDef",
    {
        "Time": datetime,
        "Source": str,
        "Resources": List[str],
        "DetailType": str,
        "Detail": str,
        "EventBusName": str,
        "TraceHeader": str,
    },
    total=False,
)

PutEventsResponseTypeDef = TypedDict(
    "PutEventsResponseTypeDef",
    {"FailedEntryCount": int, "Entries": List["PutEventsResultEntryTypeDef"]},
    total=False,
)

PutPartnerEventsRequestEntryTypeDef = TypedDict(
    "PutPartnerEventsRequestEntryTypeDef",
    {"Time": datetime, "Source": str, "Resources": List[str], "DetailType": str, "Detail": str},
    total=False,
)

PutPartnerEventsResponseTypeDef = TypedDict(
    "PutPartnerEventsResponseTypeDef",
    {"FailedEntryCount": int, "Entries": List["PutPartnerEventsResultEntryTypeDef"]},
    total=False,
)

PutRuleResponseTypeDef = TypedDict("PutRuleResponseTypeDef", {"RuleArn": str}, total=False)

PutTargetsResponseTypeDef = TypedDict(
    "PutTargetsResponseTypeDef",
    {"FailedEntryCount": int, "FailedEntries": List["PutTargetsResultEntryTypeDef"]},
    total=False,
)

RemoveTargetsResponseTypeDef = TypedDict(
    "RemoveTargetsResponseTypeDef",
    {"FailedEntryCount": int, "FailedEntries": List["RemoveTargetsResultEntryTypeDef"]},
    total=False,
)

StartReplayResponseTypeDef = TypedDict(
    "StartReplayResponseTypeDef",
    {
        "ReplayArn": str,
        "State": Literal["STARTING", "RUNNING", "CANCELLING", "COMPLETED", "CANCELLED", "FAILED"],
        "StateReason": str,
        "ReplayStartTime": datetime,
    },
    total=False,
)

TestEventPatternResponseTypeDef = TypedDict(
    "TestEventPatternResponseTypeDef", {"Result": bool}, total=False
)

UpdateApiDestinationResponseTypeDef = TypedDict(
    "UpdateApiDestinationResponseTypeDef",
    {
        "ApiDestinationArn": str,
        "ApiDestinationState": Literal["ACTIVE", "INACTIVE"],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
    },
    total=False,
)

UpdateArchiveResponseTypeDef = TypedDict(
    "UpdateArchiveResponseTypeDef",
    {
        "ArchiveArn": str,
        "State": Literal[
            "ENABLED", "DISABLED", "CREATING", "UPDATING", "CREATE_FAILED", "UPDATE_FAILED"
        ],
        "StateReason": str,
        "CreationTime": datetime,
    },
    total=False,
)

UpdateConnectionAuthRequestParametersTypeDef = TypedDict(
    "UpdateConnectionAuthRequestParametersTypeDef",
    {
        "BasicAuthParameters": "UpdateConnectionBasicAuthRequestParametersTypeDef",
        "OAuthParameters": "UpdateConnectionOAuthRequestParametersTypeDef",
        "ApiKeyAuthParameters": "UpdateConnectionApiKeyAuthRequestParametersTypeDef",
        "InvocationHttpParameters": "ConnectionHttpParametersTypeDef",
    },
    total=False,
)

UpdateConnectionResponseTypeDef = TypedDict(
    "UpdateConnectionResponseTypeDef",
    {
        "ConnectionArn": str,
        "ConnectionState": Literal[
            "CREATING",
            "UPDATING",
            "DELETING",
            "AUTHORIZED",
            "DEAUTHORIZED",
            "AUTHORIZING",
            "DEAUTHORIZING",
        ],
        "CreationTime": datetime,
        "LastModifiedTime": datetime,
        "LastAuthorizedTime": datetime,
    },
    total=False,
)
