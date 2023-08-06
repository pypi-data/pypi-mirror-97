[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-pull-request-approval-rule

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-pull-request-approval-rule)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-pull-request-approval-rule/)

> CodeCommit pull request approval rules to enforcing your pull request workflow

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-pull-request-approval-rule
```

Python:

```bash
pip install cloudcomponents.cdk-pull-request-approval-rule
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codebuild import BuildSpec
from cloudcomponents.cdk_pull_request_check import PullRequestCheck
from cloudcomponents.cdk_pull_request_approval_rule import ApprovalRuleTemplate, ApprovalRuleTemplateRepositoryAssociation

class PullRequestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="pr-check-repository"
        )

        { approvalRuleTemplateName } = ApprovalRuleTemplate(self, "ApprovalRuleTemplate",
            approval_rule_template_name="template-name",
            template=Template(
                approvers=Approvers(
                    number_of_approvals_needed=1
                )
            )
        )

        ApprovalRuleTemplateRepositoryAssociation(self, "ApprovalRuleTemplateRepositoryAssociation",
            approval_rule_template_name=approval_rule_template_name,
            repository=repository
        )

        PullRequestCheck(self, "PullRequestCheck",
            repository=repository,
            build_spec=BuildSpec.from_source_filename("prcheck.yml")
        )
```

## ApprovalRuleOverridden notification

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codebuild import BuildSpec
from cloudcomponents.cdk_pull_request_check import PullRequestCheck
from cloudcomponents.cdk_pull_request_approval_rule import ApprovalRuleTemplate, ApprovalRuleTemplateRepositoryAssociation

class PullRequestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        repository = Repository(self, "Repository",
            repository_name="pr-check-repository"
        )

        { approvalRuleTemplateName } = ApprovalRuleTemplate(self, "ApprovalRuleTemplate",
            approval_rule_template_name="template-name",
            template=Template(
                approvers=Approvers(
                    number_of_approvals_needed=1
                )
            )
        )

        rule_asscociation = ApprovalRuleTemplateRepositoryAssociation(stack, "ApprovalRuleTemplateRepositoryAssociation",
            approval_rule_template_name=approval_rule_template_name,
            repository=repository
        )

        topic = Topic(stack, "Topic")

        rule_asscociation.on_overridden("overridden",
            target=SnsTopic(topic)
        )

        # Approves the pull request
        PullRequestCheck(self, "PullRequestCheck",
            repository=repository,
            build_spec=BuildSpec.from_source_filename("prcheck.yml")
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-pull-request-approval-rule/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-pull-request-approval-rule/LICENSE)
