[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codecommit-backup

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codecommit-backup)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codecommit-backup/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> Backup CodeCommit repositories to S3

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-codecommit-backup
```

Python:

```bash
pip install cloudcomponents.cdk-codecommit-backup
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps, Duration
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_events import Schedule
from aws_cdk.aws_events_targets import SnsTopic
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from cloudcomponents.cdk_codecommit_backup import BackupBucket, S3CodeCommitBackup

class CodeCommitBackupStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository.from_repository_name(self, "Repository", process.env.REPOSITORY_NAME)

        backup_bucket = BackupBucket(self, "BackupBuckt",
            retention_period=Duration.days(90)
        )

        # The following example runs a task every day at 4am
        backup = S3CodeCommitBackup(self, "S3CodeCommitBackup",
            backup_bucket=backup_bucket,
            repository=repository,
            schedule=Schedule.cron(
                minute="0",
                hour="4"
            )
        )

        backup_topic = Topic(self, "BackupTopic")

        backup_topic.add_subscription(
            EmailSubscription(process.env.DEVSECOPS_TEAM_EMAIL))

        backup.on_backup_started("started",
            target=SnsTopic(backup_topic)
        )

        backup.on_backup_succeeded("succeeded",
            target=SnsTopic(backup_topic)
        )

        backup.on_backup_failed("failed",
            target=SnsTopic(backup_topic)
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codecommit-backup/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codecommit-backup/LICENSE)
