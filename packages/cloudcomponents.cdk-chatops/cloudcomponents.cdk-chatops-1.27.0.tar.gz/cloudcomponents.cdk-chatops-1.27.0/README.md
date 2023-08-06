[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-chatops

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-chatops)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-chatops/)

> Constructs for chattool integration: #slack / msteams

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-chatops
```

Python:

```bash
pip install cloudcomponents.cdk-chatops
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Pipeline, Artifact
from aws_cdk.aws_codepipeline_actions import CodeCommitSourceAction, ManualApprovalAction
from cloudcomponents.cdk_developer_tools_notifications import RepositoryNotificationRule, PipelineNotificationRule, RepositoryEvent, PipelineEvent, SlackChannel, MSTeamsIncomingWebhook
from cloudcomponents.cdk_chatops import SlackChannelConfiguration, MSTeamsIncomingWebhookConfiguration, AccountLabelMode

class NotificationsStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="notifications-repository"
        )

        slack_channel = SlackChannelConfiguration(self, "SlackChannel",
            slack_workspace_id=process.env.SLACK_WORKSPACE_ID,
            configuration_name="notifications",
            slack_channel_id=process.env.SLACK_CHANNEL_ID
        )

        webhook = MSTeamsIncomingWebhookConfiguration(self, "MSTeamsWebhook",
            url=process.env.INCOMING_WEBHOOK_URL,
            account_label_mode=AccountLabelMode.ID_AND_ALIAS,
            theme_color="#FF0000"
        )

        RepositoryNotificationRule(self, "RepoNotifications",
            name="notifications-repository",
            repository=repository,
            events=[RepositoryEvent.COMMENTS_ON_COMMITS, RepositoryEvent.PULL_REQUEST_CREATED, RepositoryEvent.PULL_REQUEST_MERGED
            ],
            targets=[
                SlackChannel(slack_channel),
                MSTeamsIncomingWebhook(webhook)
            ]
        )

        source_artifact = Artifact()

        source_action = CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_artifact
        )

        approval_action = ManualApprovalAction(
            action_name="Approval"
        )

        pipeline = Pipeline(self, "Pipeline",
            pipeline_name="notifications-pipeline",
            stages=[StageProps(
                stage_name="Source",
                actions=[source_action]
            ), StageProps(
                stage_name="Approval",
                actions=[approval_action]
            )
            ]
        )

        PipelineNotificationRule(self, "PipelineNotificationRule",
            name="pipeline-notification",
            pipeline=pipeline,
            events=[PipelineEvent.PIPELINE_EXECUTION_STARTED, PipelineEvent.PIPELINE_EXECUTION_FAILED, PipelineEvent.PIPELINE_EXECUTION_SUCCEEDED, PipelineEvent.MANUAL_APPROVAL_NEEDED, PipelineEvent.MANUAL_APPROVAL_SUCCEEDED
            ],
            targets=[
                SlackChannel(slack_channel),
                MSTeamsIncomingWebhook(webhook)
            ]
        )
```

## MSTeams

[Add incoming webhook](https://docs.microsoft.com/de-de/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook):

1. Navigate to the channel where you want to add the webhook and select (•••) More Options from the top navigation bar.
2. Choose Connectors from the drop-down menu and search for Incoming Webhook.
3. Select the Configure button, provide a name, and, optionally, upload an image avatar for your webhook.
4. The dialog window will present a unique URL that will map to the channel. Make sure that you copy and save the URL—you will need to provide it to the outside service.
5. Select the Done button. The webhook will be available in the team channel.

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-chatops/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-chatops/LICENSE)
