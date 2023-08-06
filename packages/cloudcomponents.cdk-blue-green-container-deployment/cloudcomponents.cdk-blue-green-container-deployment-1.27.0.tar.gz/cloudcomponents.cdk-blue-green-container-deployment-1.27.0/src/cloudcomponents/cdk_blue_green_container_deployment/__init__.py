'''
[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-blue-green-container-deployment

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-blue-green-container-deployment)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-blue-green-container-deployment/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

> Blue green container deployment with CodeDeploy

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-blue-green-container-deployment
```

Python:

```bash
pip install cloudcomponents.cdk-blue-green-container-deployment
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import Construct, Stack, StackProps
from aws_cdk.aws_codecommit import Repository
from aws_cdk.aws_codepipeline import Pipeline, Artifact
from aws_cdk.aws_ec2 import Vpc, Port
from aws_cdk.aws_ecs import Cluster
from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer, ApplicationTargetGroup, TargetType
from aws_cdk.aws_codepipeline_actions import CodeBuildAction, CodeCommitSourceAction, CodeDeployEcsDeployAction

from cloudcomponents.cdk_container_registry import ImageRepository
from cloudcomponents.cdk_blue_green_container_deployment import EcsService, DummyTaskDefinition, EcsDeploymentGroup, PushImageProject

class BlueGreenContainerDeploymentStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        vpc = Vpc(self, "Vpc",
            max_azs=2
        )

        cluster = Cluster(self, "Cluster",
            vpc=vpc,
            cluster_name="blue-green-cluster"
        )

        load_balancer = ApplicationLoadBalancer(self, "LoadBalancer",
            vpc=vpc,
            internet_facing=True
        )

        prod_listener = load_balancer.add_listener("ProfListener",
            port=80
        )

        test_listener = load_balancer.add_listener("TestListener",
            port=8080
        )

        prod_target_group = ApplicationTargetGroup(self, "ProdTargetGroup",
            port=80,
            target_type=TargetType.IP,
            vpc=vpc
        )

        prod_listener.add_target_groups("AddProdTg",
            target_groups=[prod_target_group]
        )

        test_target_group = ApplicationTargetGroup(self, "TestTargetGroup",
            port=8080,
            target_type=TargetType.IP,
            vpc=vpc
        )

        test_listener.add_target_groups("AddTestTg",
            target_groups=[test_target_group]
        )

        # Will be replaced by CodeDeploy in CodePipeline
        task_definition = DummyTaskDefinition(self, "DummyTaskDefinition",
            image="nginx",
            family="blue-green"
        )

        ecs_service = EcsService(self, "EcsService",
            cluster=cluster,
            service_name="blue-green-service",
            desired_count=2,
            task_definition=task_definition,
            prod_target_group=prod_target_group
        )

        ecs_service.connections.allow_from(load_balancer, Port.tcp(80))
        ecs_service.connections.allow_from(load_balancer, Port.tcp(8080))

        deployment_group = EcsDeploymentGroup(self, "DeploymentGroup",
            application_name="blue-green-application",
            deployment_group_name="blue-green-deployment-group",
            ecs_services=[ecs_service],
            target_group_names=[prod_target_group.target_group_name, test_target_group.target_group_name
            ],
            prod_traffic_listener=prod_listener,
            test_traffic_listener=test_listener,
            termination_wait_time_in_minutes=100
        )

        # @see https://github.com/cloudcomponents/cdk-constructs/tree/master/examples/blue-green-container-deployment-example/blue-green-repository
        repository = Repository(self, "CodeRepository",
            repository_name="blue-green-repository"
        )

        image_repository = ImageRepository(self, "ImageRepository", {
            "force_delete": True
        })

        source_artifact = Artifact()

        source_action = CodeCommitSourceAction(
            action_name="CodeCommit",
            repository=repository,
            output=source_artifact
        )

        image_artifact = Artifact("ImageArtifact")
        manifest_artifact = Artifact("ManifestArtifact")

        push_image_project = PushImageProject(self, "PushImageProject",
            image_repository=image_repository,
            task_definition=task_definition
        )

        build_action = CodeBuildAction(
            action_name="PushImage",
            project=push_image_project,
            input=source_artifact,
            outputs=[image_artifact, manifest_artifact]
        )

        deploy_action = CodeDeployEcsDeployAction(
            action_name="CodeDeploy",
            task_definition_template_input=manifest_artifact,
            app_spec_template_input=manifest_artifact,
            container_image_inputs=[CodeDeployEcsContainerImageInput(
                input=image_artifact,
                task_definition_placeholder="IMAGE1_NAME"
            )
            ],
            deployment_group=deployment_group
        )

        Pipeline(self, "Pipeline",
            pipeline_name="blue-green-pipeline",
            stages=[StageProps(
                stage_name="Source",
                actions=[source_action]
            ), StageProps(
                stage_name="Build",
                actions=[build_action]
            ), StageProps(
                stage_name="Deploy",
                actions=[deploy_action]
            )
            ]
        )
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-blue-green-container-deployment/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-blue-green-container-deployment//LICENSE)
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

import aws_cdk.aws_codebuild
import aws_cdk.aws_codedeploy
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.core


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.DummyTaskDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "container_port": "containerPort",
        "family": "family",
    },
)
class DummyTaskDefinitionProps:
    def __init__(
        self,
        *,
        image: builtins.str,
        container_port: typing.Optional[jsii.Number] = None,
        family: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: -
        :param container_port: -
        :param family: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
        }
        if container_port is not None:
            self._values["container_port"] = container_port
        if family is not None:
            self._values["family"] = family

    @builtins.property
    def image(self) -> builtins.str:
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def family(self) -> typing.Optional[builtins.str]:
        result = self._values.get("family")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DummyTaskDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_codedeploy.IEcsDeploymentGroup)
class EcsDeploymentGroup(
    aws_cdk.core.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.EcsDeploymentGroup",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        deployment_group_name: builtins.str,
        ecs_services: typing.List["IEcsService"],
        prod_traffic_listener: "TrafficListener",
        target_group_names: typing.List[builtins.str],
        test_traffic_listener: "TrafficListener",
        application_name: typing.Optional[builtins.str] = None,
        auto_rollback_on_events: typing.Optional[typing.List["RollbackEvent"]] = None,
        deployment_config: typing.Optional[aws_cdk.aws_codedeploy.IEcsDeploymentConfig] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param deployment_group_name: -
        :param ecs_services: -
        :param prod_traffic_listener: -
        :param target_group_names: -
        :param test_traffic_listener: -
        :param application_name: -
        :param auto_rollback_on_events: The event type or types that trigger a rollback.
        :param deployment_config: -
        :param termination_wait_time_in_minutes: the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set. The maximum setting is 2880 minutes (2 days). Default: 60
        '''
        props = EcsDeploymentGroupProps(
            deployment_group_name=deployment_group_name,
            ecs_services=ecs_services,
            prod_traffic_listener=prod_traffic_listener,
            target_group_names=target_group_names,
            test_traffic_listener=test_traffic_listener,
            application_name=application_name,
            auto_rollback_on_events=auto_rollback_on_events,
            deployment_config=deployment_config,
            termination_wait_time_in_minutes=termination_wait_time_in_minutes,
        )

        jsii.create(EcsDeploymentGroup, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="application")
    def application(self) -> aws_cdk.aws_codedeploy.IEcsApplication:
        '''The reference to the CodeDeploy ECS Application that this Deployment Group belongs to.'''
        return typing.cast(aws_cdk.aws_codedeploy.IEcsApplication, jsii.get(self, "application"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentConfig")
    def deployment_config(self) -> aws_cdk.aws_codedeploy.IEcsDeploymentConfig:
        '''The Deployment Configuration this Group uses.'''
        return typing.cast(aws_cdk.aws_codedeploy.IEcsDeploymentConfig, jsii.get(self, "deploymentConfig"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupArn")
    def deployment_group_arn(self) -> builtins.str:
        '''The ARN of this Deployment Group.'''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deploymentGroupName")
    def deployment_group_name(self) -> builtins.str:
        '''The physical name of the CodeDeploy Deployment Group.'''
        return typing.cast(builtins.str, jsii.get(self, "deploymentGroupName"))


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.EcsDeploymentGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_group_name": "deploymentGroupName",
        "ecs_services": "ecsServices",
        "prod_traffic_listener": "prodTrafficListener",
        "target_group_names": "targetGroupNames",
        "test_traffic_listener": "testTrafficListener",
        "application_name": "applicationName",
        "auto_rollback_on_events": "autoRollbackOnEvents",
        "deployment_config": "deploymentConfig",
        "termination_wait_time_in_minutes": "terminationWaitTimeInMinutes",
    },
)
class EcsDeploymentGroupProps:
    def __init__(
        self,
        *,
        deployment_group_name: builtins.str,
        ecs_services: typing.List["IEcsService"],
        prod_traffic_listener: "TrafficListener",
        target_group_names: typing.List[builtins.str],
        test_traffic_listener: "TrafficListener",
        application_name: typing.Optional[builtins.str] = None,
        auto_rollback_on_events: typing.Optional[typing.List["RollbackEvent"]] = None,
        deployment_config: typing.Optional[aws_cdk.aws_codedeploy.IEcsDeploymentConfig] = None,
        termination_wait_time_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param deployment_group_name: -
        :param ecs_services: -
        :param prod_traffic_listener: -
        :param target_group_names: -
        :param test_traffic_listener: -
        :param application_name: -
        :param auto_rollback_on_events: The event type or types that trigger a rollback.
        :param deployment_config: -
        :param termination_wait_time_in_minutes: the number of minutes before deleting the original (blue) task set. During an Amazon ECS deployment, CodeDeploy shifts traffic from the original (blue) task set to a replacement (green) task set. The maximum setting is 2880 minutes (2 days). Default: 60
        '''
        if isinstance(prod_traffic_listener, dict):
            prod_traffic_listener = TrafficListener(**prod_traffic_listener)
        if isinstance(test_traffic_listener, dict):
            test_traffic_listener = TrafficListener(**test_traffic_listener)
        self._values: typing.Dict[str, typing.Any] = {
            "deployment_group_name": deployment_group_name,
            "ecs_services": ecs_services,
            "prod_traffic_listener": prod_traffic_listener,
            "target_group_names": target_group_names,
            "test_traffic_listener": test_traffic_listener,
        }
        if application_name is not None:
            self._values["application_name"] = application_name
        if auto_rollback_on_events is not None:
            self._values["auto_rollback_on_events"] = auto_rollback_on_events
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if termination_wait_time_in_minutes is not None:
            self._values["termination_wait_time_in_minutes"] = termination_wait_time_in_minutes

    @builtins.property
    def deployment_group_name(self) -> builtins.str:
        result = self._values.get("deployment_group_name")
        assert result is not None, "Required property 'deployment_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ecs_services(self) -> typing.List["IEcsService"]:
        result = self._values.get("ecs_services")
        assert result is not None, "Required property 'ecs_services' is missing"
        return typing.cast(typing.List["IEcsService"], result)

    @builtins.property
    def prod_traffic_listener(self) -> "TrafficListener":
        result = self._values.get("prod_traffic_listener")
        assert result is not None, "Required property 'prod_traffic_listener' is missing"
        return typing.cast("TrafficListener", result)

    @builtins.property
    def target_group_names(self) -> typing.List[builtins.str]:
        result = self._values.get("target_group_names")
        assert result is not None, "Required property 'target_group_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def test_traffic_listener(self) -> "TrafficListener":
        result = self._values.get("test_traffic_listener")
        assert result is not None, "Required property 'test_traffic_listener' is missing"
        return typing.cast("TrafficListener", result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_rollback_on_events(self) -> typing.Optional[typing.List["RollbackEvent"]]:
        '''The event type or types that trigger a rollback.'''
        result = self._values.get("auto_rollback_on_events")
        return typing.cast(typing.Optional[typing.List["RollbackEvent"]], result)

    @builtins.property
    def deployment_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_codedeploy.IEcsDeploymentConfig]:
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[aws_cdk.aws_codedeploy.IEcsDeploymentConfig], result)

    @builtins.property
    def termination_wait_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''the number of minutes before deleting the original (blue) task set.

        During an Amazon ECS deployment, CodeDeploy shifts traffic from the
        original (blue) task set to a replacement (green) task set.

        The maximum setting is 2880 minutes (2 days).

        :default: 60
        '''
        result = self._values.get("termination_wait_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsDeploymentGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.EcsServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "prod_target_group": "prodTargetGroup",
        "service_name": "serviceName",
        "task_definition": "taskDefinition",
        "container_port": "containerPort",
        "desired_count": "desiredCount",
        "launch_type": "launchType",
        "platform_version": "platformVersion",
        "security_groups": "securityGroups",
    },
)
class EcsServiceProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        prod_target_group: aws_cdk.aws_elasticloadbalancingv2.ITargetGroup,
        service_name: builtins.str,
        task_definition: "DummyTaskDefinition",
        container_port: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        launch_type: typing.Optional[aws_cdk.aws_ecs.LaunchType] = None,
        platform_version: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.SecurityGroup]] = None,
    ) -> None:
        '''
        :param cluster: -
        :param prod_target_group: -
        :param service_name: -
        :param task_definition: -
        :param container_port: -
        :param desired_count: -
        :param launch_type: -
        :param platform_version: -
        :param security_groups: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "prod_target_group": prod_target_group,
            "service_name": service_name,
            "task_definition": task_definition,
        }
        if container_port is not None:
            self._values["container_port"] = container_port
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if launch_type is not None:
            self._values["launch_type"] = launch_type
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_ecs.ICluster, result)

    @builtins.property
    def prod_target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.ITargetGroup:
        result = self._values.get("prod_target_group")
        assert result is not None, "Required property 'prod_target_group' is missing"
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.ITargetGroup, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_definition(self) -> "DummyTaskDefinition":
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast("DummyTaskDefinition", result)

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("container_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def launch_type(self) -> typing.Optional[aws_cdk.aws_ecs.LaunchType]:
        result = self._values.get("launch_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.LaunchType], result)

    @builtins.property
    def platform_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.SecurityGroup]]:
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.SecurityGroup]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.IDummyTaskDefinition"
)
class IDummyTaskDefinition(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IDummyTaskDefinitionProxy"]:
        return _IDummyTaskDefinitionProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> aws_cdk.aws_iam.IRole:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        ...


class _IDummyTaskDefinitionProxy:
    __jsii_type__: typing.ClassVar[str] = "@cloudcomponents/cdk-blue-green-container-deployment.IDummyTaskDefinition"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "executionRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskDefinitionArn"))


@jsii.interface(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.IEcsService"
)
class IEcsService(typing_extensions.Protocol):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_IEcsServiceProxy"]:
        return _IEcsServiceProxy

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        ...


class _IEcsServiceProxy:
    __jsii_type__: typing.ClassVar[str] = "@cloudcomponents/cdk-blue-green-container-deployment.IEcsService"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))


class PushImageProject(
    aws_cdk.aws_codebuild.PipelineProject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.PushImageProject",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image_repository: aws_cdk.aws_ecr.IRepository,
        task_definition: IDummyTaskDefinition,
        build_spec: typing.Optional[aws_cdk.aws_codebuild.BuildSpec] = None,
        cache: typing.Optional[aws_cdk.aws_codebuild.Cache] = None,
        compute_type: typing.Optional[aws_cdk.aws_codebuild.ComputeType] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_repository: -
        :param task_definition: -
        :param build_spec: -
        :param cache: -
        :param compute_type: -
        :param environment_variables: -
        :param project_name: -
        '''
        props = PushImageProjectProps(
            image_repository=image_repository,
            task_definition=task_definition,
            build_spec=build_spec,
            cache=cache,
            compute_type=compute_type,
            environment_variables=environment_variables,
            project_name=project_name,
        )

        jsii.create(PushImageProject, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.PushImageProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_repository": "imageRepository",
        "task_definition": "taskDefinition",
        "build_spec": "buildSpec",
        "cache": "cache",
        "compute_type": "computeType",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
    },
)
class PushImageProjectProps:
    def __init__(
        self,
        *,
        image_repository: aws_cdk.aws_ecr.IRepository,
        task_definition: IDummyTaskDefinition,
        build_spec: typing.Optional[aws_cdk.aws_codebuild.BuildSpec] = None,
        cache: typing.Optional[aws_cdk.aws_codebuild.Cache] = None,
        compute_type: typing.Optional[aws_cdk.aws_codebuild.ComputeType] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_repository: -
        :param task_definition: -
        :param build_spec: -
        :param cache: -
        :param compute_type: -
        :param environment_variables: -
        :param project_name: -
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image_repository": image_repository,
            "task_definition": task_definition,
        }
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cache is not None:
            self._values["cache"] = cache
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def image_repository(self) -> aws_cdk.aws_ecr.IRepository:
        result = self._values.get("image_repository")
        assert result is not None, "Required property 'image_repository' is missing"
        return typing.cast(aws_cdk.aws_ecr.IRepository, result)

    @builtins.property
    def task_definition(self) -> IDummyTaskDefinition:
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(IDummyTaskDefinition, result)

    @builtins.property
    def build_spec(self) -> typing.Optional[aws_cdk.aws_codebuild.BuildSpec]:
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[aws_cdk.aws_codebuild.BuildSpec], result)

    @builtins.property
    def cache(self) -> typing.Optional[aws_cdk.aws_codebuild.Cache]:
        result = self._values.get("cache")
        return typing.cast(typing.Optional[aws_cdk.aws_codebuild.Cache], result)

    @builtins.property
    def compute_type(self) -> typing.Optional[aws_cdk.aws_codebuild.ComputeType]:
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[aws_cdk.aws_codebuild.ComputeType], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]]:
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_codebuild.BuildEnvironmentVariable]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushImageProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.RollbackEvent"
)
class RollbackEvent(enum.Enum):
    DEPLOYMENT_FAILURE = "DEPLOYMENT_FAILURE"
    DEPLOYMENT_STOP_ON_ALARM = "DEPLOYMENT_STOP_ON_ALARM"
    DEPLOYMENT_STOP_ON_REQUEST = "DEPLOYMENT_STOP_ON_REQUEST"


@jsii.enum(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.SchedulingStrategy"
)
class SchedulingStrategy(enum.Enum):
    REPLICA = "REPLICA"
    DAEMON = "DAEMON"


@jsii.data_type(
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.TrafficListener",
    jsii_struct_bases=[],
    name_mapping={"listener_arn": "listenerArn"},
)
class TrafficListener:
    def __init__(self, *, listener_arn: builtins.str) -> None:
        '''
        :param listener_arn: ARN of the listener.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "listener_arn": listener_arn,
        }

    @builtins.property
    def listener_arn(self) -> builtins.str:
        '''ARN of the listener.

        :attribute: true
        '''
        result = self._values.get("listener_arn")
        assert result is not None, "Required property 'listener_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrafficListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDummyTaskDefinition)
class DummyTaskDefinition(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.DummyTaskDefinition",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        image: builtins.str,
        container_port: typing.Optional[jsii.Number] = None,
        family: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image: -
        :param container_port: -
        :param family: -
        '''
        props = DummyTaskDefinitionProps(
            image=image, container_port=container_port, family=family
        )

        jsii.create(DummyTaskDefinition, self, [scope, id, props])

    @jsii.member(jsii_name="addToExecutionRolePolicy")
    def add_to_execution_role_policy(
        self,
        statement: aws_cdk.aws_iam.PolicyStatement,
    ) -> None:
        '''Adds a policy statement to the task execution IAM role.

        :param statement: -
        '''
        return typing.cast(None, jsii.invoke(self, "addToExecutionRolePolicy", [statement]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="containerPort")
    def container_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "containerPort"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> aws_cdk.aws_iam.IRole:
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "executionRole"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="family")
    def family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "family"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="taskDefinitionArn")
    def task_definition_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "taskDefinitionArn"))


@jsii.implements(aws_cdk.aws_ec2.IConnectable, IEcsService)
class EcsService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cloudcomponents/cdk-blue-green-container-deployment.EcsService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_ecs.ICluster,
        prod_target_group: aws_cdk.aws_elasticloadbalancingv2.ITargetGroup,
        service_name: builtins.str,
        task_definition: DummyTaskDefinition,
        container_port: typing.Optional[jsii.Number] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        launch_type: typing.Optional[aws_cdk.aws_ecs.LaunchType] = None,
        platform_version: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.List[aws_cdk.aws_ec2.SecurityGroup]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: -
        :param prod_target_group: -
        :param service_name: -
        :param task_definition: -
        :param container_port: -
        :param desired_count: -
        :param launch_type: -
        :param platform_version: -
        :param security_groups: -
        '''
        props = EcsServiceProps(
            cluster=cluster,
            prod_target_group=prod_target_group,
            service_name=service_name,
            task_definition=task_definition,
            container_port=container_port,
            desired_count=desired_count,
            launch_type=launch_type,
            platform_version=platform_version,
            security_groups=security_groups,
        )

        jsii.create(EcsService, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))


__all__ = [
    "DummyTaskDefinition",
    "DummyTaskDefinitionProps",
    "EcsDeploymentGroup",
    "EcsDeploymentGroupProps",
    "EcsService",
    "EcsServiceProps",
    "IDummyTaskDefinition",
    "IEcsService",
    "PushImageProject",
    "PushImageProjectProps",
    "RollbackEvent",
    "SchedulingStrategy",
    "TrafficListener",
]

publication.publish()
