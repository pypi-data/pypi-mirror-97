'''
[![NPM version](https://badge.fury.io/js/cdk-fargate-run-task.svg)](https://badge.fury.io/js/cdk-fargate-run-task)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-run-task.svg)](https://badge.fury.io/py/cdk-fargate-run-task)
![Release](https://github.com/pahud/cdk-fargate-run-task/workflows/Release/badge.svg?branch=main)

# cdk-fargate-run-task

Define and run container tasks on AWS Fargate at once or by schedule.

# sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
app = cdk.App()

env = {
    "account": process.env.CDK_DEFAULT_ACCOUNT,
    "region": process.env.CDK_DEFAULT_REGION
}

stack = cdk.Stack(app, "run-task-demo-stack", env=env)

# define your task
task = ecs.FargateTaskDefinition(stack, "Task", cpu=256, memory_limit_mi_b=512)

# add contianer into the task
task.add_container("Ping",
    image=ecs.ContainerImage.from_registry("busybox"),
    command=["sh", "-c", "ping -c 3 google.com"
    ],
    logging=ecs.AwsLogDriver(
        stream_prefix="Ping",
        log_group=LogGroup(stack, "LogGroup",
            log_group_name=f"{stack.stackName}LogGroup",
            retention=RetentionDays.ONE_DAY
        )
    )
)

# deploy and run this task once
run_task_at_once = RunTask(stack, "RunDemoTaskOnce", task=task)

# or run it with schedule(every hour 0min)
RunTask(stack, "RunDemoTaskEveryHour",
    task=task,
    cluster=run_task_at_once.cluster,
    run_once=False,
    schedule=Schedule.cron(minute="0")
)
```
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

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_logs
import aws_cdk.core


@jsii.enum(jsii_type="cdk-fargate-run-task.PlatformVersion")
class PlatformVersion(enum.Enum):
    '''Fargate platform version.'''

    V1_3_0 = "V1_3_0"
    V1_4_0 = "V1_4_0"
    LATEST = "LATEST"


class RunTask(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fargate-run-task.RunTask",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        task: aws_cdk.aws_ecs.FargateTaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        fargate_platform_version: typing.Optional[PlatformVersion] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        run_on_resource_update: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param fargate_platform_version: Fargate platform version. Default: LATEST
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param run_on_resource_update: run the task again on the custom resource update. Default: false
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param security_group: fargate security group. Default: - create a default security group
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        '''
        props = RunTaskProps(
            task=task,
            cluster=cluster,
            fargate_platform_version=fargate_platform_version,
            log_retention=log_retention,
            run_at_once=run_at_once,
            run_on_resource_update=run_on_resource_update,
            schedule=schedule,
            security_group=security_group,
            vpc=vpc,
        )

        jsii.create(RunTask, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        return typing.cast(aws_cdk.aws_ecs.ICluster, jsii.get(self, "cluster"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> aws_cdk.aws_ec2.ISecurityGroup:
        '''fargate task security group.'''
        return typing.cast(aws_cdk.aws_ec2.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-fargate-run-task.RunTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task": "task",
        "cluster": "cluster",
        "fargate_platform_version": "fargatePlatformVersion",
        "log_retention": "logRetention",
        "run_at_once": "runAtOnce",
        "run_on_resource_update": "runOnResourceUpdate",
        "schedule": "schedule",
        "security_group": "securityGroup",
        "vpc": "vpc",
    },
)
class RunTaskProps:
    def __init__(
        self,
        *,
        task: aws_cdk.aws_ecs.FargateTaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        fargate_platform_version: typing.Optional[PlatformVersion] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        run_on_resource_update: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param fargate_platform_version: Fargate platform version. Default: LATEST
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param run_on_resource_update: run the task again on the custom resource update. Default: false
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param security_group: fargate security group. Default: - create a default security group
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "task": task,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if fargate_platform_version is not None:
            self._values["fargate_platform_version"] = fargate_platform_version
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if run_at_once is not None:
            self._values["run_at_once"] = run_at_once
        if run_on_resource_update is not None:
            self._values["run_on_resource_update"] = run_on_resource_update
        if schedule is not None:
            self._values["schedule"] = schedule
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def task(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        '''The Amazon ECS Task definition for AWS Fargate.'''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(aws_cdk.aws_ecs.FargateTaskDefinition, result)

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        '''The Amazon ECS Cluster.

        :default: - create a new cluster
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[aws_cdk.aws_ecs.ICluster], result)

    @builtins.property
    def fargate_platform_version(self) -> typing.Optional[PlatformVersion]:
        '''Fargate platform version.

        :default: LATEST
        '''
        result = self._values.get("fargate_platform_version")
        return typing.cast(typing.Optional[PlatformVersion], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        '''Log retention days.

        :default: - one week
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def run_at_once(self) -> typing.Optional[builtins.bool]:
        '''run it at once(immediately after deployment).

        :default: true
        '''
        result = self._values.get("run_at_once")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def run_on_resource_update(self) -> typing.Optional[builtins.bool]:
        '''run the task again on the custom resource update.

        :default: false
        '''
        result = self._values.get("run_on_resource_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''run the task with defined schedule.

        :default: - no shedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    @builtins.property
    def security_group(self) -> typing.Optional[aws_cdk.aws_ec2.ISecurityGroup]:
        '''fargate security group.

        :default: - create a default security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        '''The VPC for the Amazon ECS task.

        :default: - create a new VPC or use existing one
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PlatformVersion",
    "RunTask",
    "RunTaskProps",
]

publication.publish()
