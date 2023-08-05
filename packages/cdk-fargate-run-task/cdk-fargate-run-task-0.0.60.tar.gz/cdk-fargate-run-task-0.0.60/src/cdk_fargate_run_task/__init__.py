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
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        '''
        props = RunTaskProps(
            task=task,
            cluster=cluster,
            log_retention=log_retention,
            run_at_once=run_at_once,
            schedule=schedule,
            vpc=vpc,
        )

        jsii.create(RunTask, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        return typing.cast(aws_cdk.aws_ecs.ICluster, jsii.get(self, "cluster"))

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
        "log_retention": "logRetention",
        "run_at_once": "runAtOnce",
        "schedule": "schedule",
        "vpc": "vpc",
    },
)
class RunTaskProps:
    def __init__(
        self,
        *,
        task: aws_cdk.aws_ecs.FargateTaskDefinition,
        cluster: typing.Optional[aws_cdk.aws_ecs.ICluster] = None,
        log_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "task": task,
        }
        if cluster is not None:
            self._values["cluster"] = cluster
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if run_at_once is not None:
            self._values["run_at_once"] = run_at_once
        if schedule is not None:
            self._values["schedule"] = schedule
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
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        '''run the task with defined schedule.

        :default: - no shedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

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
    "RunTask",
    "RunTaskProps",
]

publication.publish()
