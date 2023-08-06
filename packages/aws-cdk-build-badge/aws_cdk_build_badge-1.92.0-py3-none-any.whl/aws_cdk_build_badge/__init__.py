'''
[![NPM version](https://badge.fury.io/js/aws-cdk-build-badge.svg)](https://badge.fury.io/js/aws-cdk-build-badge)
[![PyPI version](https://badge.fury.io/py/aws-cdk-build-badge.svg)](https://badge.fury.io/py/aws-cdk-build-badge)
[![.NET version](https://img.shields.io/nuget/v/com.github.mmuller88.awsCdkBuildBadge.svg?style=flat-square)](https://www.nuget.org/packages/com.github.mmuller88.awsCdkBuildBadge/)
![Release](https://github.com/mmuller88/aws-cdk-build-badge/workflows/Release/badge.svg)

# aws-cdk-build-badge

This an AWS CDK custom construct for get the status of a CodeBuild Project with has CodePipeline as source. That is currently not possible:

* https://github.com/aws/aws-cdk/issues/1749

How the native badges are working you find in the AWS docs:

* https://docs.aws.amazon.com/codebuild/latest/userguide/sample-build-badges.html

After you created the build badge construct you can use the api gateway url to get the badge picture. Additionally you can retrieve the url to to the CodeBuild build with adding ?url=true to the query parameter. See the example.

# Example

Build succeeded: [![CodeBuild test build](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=PipelineCustomStageprodTest-Fdei5bm2ulR6)](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=PipelineCustomStageprodTest-Fdei5bm2ulR6&url=true)

Build failed: [![CodeBuild test build](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=PipelineCustomStagedevTestC-UnzKxyLsGYZw)](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=PipelineCustomStageprodTest-Fdei5bm2ulR6&url=true)

Build not found: [![CodeBuild test build](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=123)](https://fktijpwdng.execute-api.eu-central-1.amazonaws.com/prod/?projectName=123&url=true)

There are more badges (see ./badges/) but I don't have build in that state atm.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

stack = cdk.Stack(app, "my-build-badge-demo-stack")

# without exposing the account id in the url when using ?url=true
BuildBadge(stack, "BuildBadge")

# with exposing the account id in the url when using ?url=true
BuildBadge(stack, "BuildBadge2", hide_account_iD="no")

# partly exposing the account id in the url when using ?url=true
BuildBadge(stack, "BuildBadge3", hide_account_iD="XX123356")
```

# Thanks To

* The CDK Community cdk-dev.slack.com
* [Projen](https://github.com/projen/projen) project and the community around it
* https://github.com/btorun/aws-codebuild-badges
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.core


class BuildBadge(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-build-badge.BuildBadge",
):
    def __init__(
        self,
        parent: aws_cdk.core.Stack,
        id: builtins.str,
        *,
        default_project_name: typing.Optional[builtins.str] = None,
        hide_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parent: -
        :param id: -
        :param default_project_name: Specify a default project name. Than you don't need to add it in the url. If you do so anyway the default here will be ignored. Default: - not set
        :param hide_account_id: Thats a little safety feature. Set it to 'no' for allowing to see your account id when retrieving the CodeBuild URL. You can as well use a pattern which hides part of your account id like XX1237193288 Default: - not set and account id will be shown as 123
        '''
        props = BuildBadgeProps(
            default_project_name=default_project_name, hide_account_id=hide_account_id
        )

        jsii.create(BuildBadge, self, [parent, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="badgeUrl")
    def badge_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "badgeUrl"))


@jsii.data_type(
    jsii_type="aws-cdk-build-badge.BuildBadgeProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_project_name": "defaultProjectName",
        "hide_account_id": "hideAccountID",
    },
)
class BuildBadgeProps:
    def __init__(
        self,
        *,
        default_project_name: typing.Optional[builtins.str] = None,
        hide_account_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_project_name: Specify a default project name. Than you don't need to add it in the url. If you do so anyway the default here will be ignored. Default: - not set
        :param hide_account_id: Thats a little safety feature. Set it to 'no' for allowing to see your account id when retrieving the CodeBuild URL. You can as well use a pattern which hides part of your account id like XX1237193288 Default: - not set and account id will be shown as 123
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if default_project_name is not None:
            self._values["default_project_name"] = default_project_name
        if hide_account_id is not None:
            self._values["hide_account_id"] = hide_account_id

    @builtins.property
    def default_project_name(self) -> typing.Optional[builtins.str]:
        '''Specify a default project name.

        Than you don't need to add it in the url. If you do so anyway the default here will be ignored.

        :default: - not set
        '''
        result = self._values.get("default_project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hide_account_id(self) -> typing.Optional[builtins.str]:
        '''Thats a little safety feature.

        Set it to 'no' for allowing to see your account id when retrieving the CodeBuild URL.
        You can as well use a pattern which hides part of your account id like XX1237193288

        :default: - not set and account id will be shown as 123
        '''
        result = self._values.get("hide_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildBadgeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BuildBadge",
    "BuildBadgeProps",
]

publication.publish()
