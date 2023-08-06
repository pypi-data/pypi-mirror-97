[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-codepipeline-dockerfile-linter-action

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-codepipeline-dockerfile-linter-action)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-codepipeline-dockerfile-linter-action/)

> CodePipeline action to lint dockerfiles with [hadolint](https://github.com/hadolint/hadolint)

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-codepipeline-dockerfile-linter-action
```

Python:

```bash
pip install cloudcomponents.cdk-codepipeline-dockerfile-linter-action
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Pipeline, Artifact
from aws_cdk.aws_codepipeline_actions import CodeCommitSourceAction
from cloudcomponents.cdk_codepipeline_dockerfile_linter_action import CodePipelineDockerfileLinterAction
from cloudcomponents.cdk_codepipeline_anchore_inline_scan_action import CodePipelineAnchoreInlineScanAction
class ContainerAuditStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="container-audit-repository"
        )

        source_artifact = Artifact()

        source_action = CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_artifact,
            branch="master"
        )

        linter_action = CodePipelineDockerfileLinterAction(
            action_name="Linter",
            input=source_artifact
        )

        vuln_scan_action = CodePipelineAnchoreInlineScanAction(
            action_name="VulnScan",
            input=source_artifact
        )

        Pipeline(self, "Pipeline",
            pipeline_name="container-audit-pipeline",
            stages=[StageProps(
                stage_name="Source",
                actions=[source_action]
            ), StageProps(
                stage_name="Audit",
                actions=[linter_action, vuln_scan_action]
            )
            ]
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-dockerfile-linter-action/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-codepipeline-dockerfile-linter-action/LICENSE)
