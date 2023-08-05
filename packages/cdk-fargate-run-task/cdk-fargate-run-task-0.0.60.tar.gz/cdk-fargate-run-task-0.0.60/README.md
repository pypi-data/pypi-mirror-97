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
