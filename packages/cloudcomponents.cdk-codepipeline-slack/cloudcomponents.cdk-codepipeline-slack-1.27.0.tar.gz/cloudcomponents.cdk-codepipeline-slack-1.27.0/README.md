[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codepipeline-slack

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codepipeline-slack)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codepipeline-slack/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> Cdk component that provisions a #slack approval workflow and notification messages on codepipeline state changes

![Approval Workflow](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/approval_workflow.png)

![Review Dialog](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/review_dialog.png)

## Install

TypeScript/JavaScript:

```bash
npm install --save @cloudcomponents/cdk-codepipeline-slack
```

Python:

```bash
pip install cloudcomponents.cdk-codepipeline-slack
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Pipeline, Artifact
from aws_cdk.aws_codepipeline_actions import CodeCommitSourceAction, CodeBuildAction
from aws_cdk.aws_codebuild import PipelineProject

from cloudcomponents.cdk_codepipeline_slack import SlackApprovalAction, SlackNotifier

class CodePipelineSlackApprovalStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="MyRepositoryName"
        )

        source_artifact = Artifact()

        source_action = CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_artifact
        )

        project = PipelineProject(self, "MyProject")

        build_action = CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_artifact
        )

        slack_bot_token = process.env.SLACK_BOT_TOKEN
        slack_signing_secret = process.env.SLACK_SIGNING_SECRET
        slack_channel = process.env.SLACK_CHANNEL_NAME

        approval_action = SlackApprovalAction(
            action_name="SlackApproval",
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            slack_channel=slack_channel,
            external_entity_link="http://cloudcomponents.org",
            additional_information="Would you like to promote the build to production?"
        )

        pipeline = Pipeline(self, "MyPipeline",
            pipeline_name="MyPipeline",
            stages=[StageProps(
                stage_name="Source",
                actions=[source_action]
            ), StageProps(
                stage_name="Build",
                actions=[build_action]
            ), StageProps(
                stage_name="Approval",
                actions=[approval_action]
            )
            ]
        )

        SlackNotifier(self, "SlackNotifier",
            pipeline=pipeline,
            slack_bot_token=slack_bot_token,
            slack_signing_secret=slack_signing_secret,
            slack_channel=slack_channel
        )
```

## Slack App Settings

Create an app that’s just for your workspace

### OAuth & Permissions

Grant the `channels::history`-Scope to the Bot in your app and Add the Bot to the configured Slack-Channel

Select Permission Scopes:

![OAuth Scopes](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/oauth_scope.png)

### Interactive Components

Enter the url of your api from the AWS Api Gateway and append `/slack/actions`:

![Interactive Components](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/packages/cdk-codepipeline-slack/assets/interactive_components.png)

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-slack/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-slack/LICENSE)
