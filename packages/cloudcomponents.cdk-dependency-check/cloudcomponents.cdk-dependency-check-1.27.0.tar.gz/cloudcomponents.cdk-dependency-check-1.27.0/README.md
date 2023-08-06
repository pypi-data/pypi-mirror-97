[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-dependency-check

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-dependency-check)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-dependency-check/)

> [OWASP dependency-check](https://owasp.org/www-project-dependency-check/) for codecommit repositories

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-dependency-check
```

Python:

```bash
pip install cloudcomponents.cdk-dependency-check
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_events import Schedule
from aws_cdk.aws_events_targets import SnsTopic
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from cloudcomponents.cdk_dependency_check import CodeCommitDependencyCheck

class DependencyCheckStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository.from_repository_name(self, "Repository", process.env.REPOSITORY_NAME)

        reports_bucket = Bucket(self, "Bucket")

        # The following example runs a task every day at 4am
        check = CodeCommitDependencyCheck(self, "CodeCommitDependencyCheck",
            repository=repository,
            reports_bucket=reports_bucket,
            pre_check_command="npm i",
            schedule=Schedule.cron(
                minute="0",
                hour="4"
            )
        )

        check_topic = Topic(self, "CheckTopic")

        check_topic.add_subscription(
            EmailSubscription(process.env.DEVSECOPS_TEAM_EMAIL))

        check.on_check_started("started",
            target=SnsTopic(check_topic)
        )

        check.on_check_succeeded("succeeded",
            target=SnsTopic(check_topic)
        )

        check.on_check_failed("failed",
            target=SnsTopic(check_topic)
        )
```

## Upload HTML Reports

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
reports_bucket = Bucket(self, "Bucket")

# The following example runs a task every day at 4am
check = CodeCommitDependencyCheck(self, "CodeCommitDependencyCheck",
    repository=repository,
    reports_bucket=reports_bucket,
    pre_check_command="npm i",
    schedule=Schedule.cron(
        minute="0",
        hour="4"
    )
)
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dependency-check/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-dependency-check/LICENSE)
