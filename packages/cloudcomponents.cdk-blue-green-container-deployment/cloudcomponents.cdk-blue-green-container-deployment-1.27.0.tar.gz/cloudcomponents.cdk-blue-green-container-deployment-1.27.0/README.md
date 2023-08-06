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
