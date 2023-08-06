[![NPM version](https://badge.fury.io/js/cdk-gitlab.svg)](https://badge.fury.io/js/cdk-gitlab)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab.svg)](https://badge.fury.io/py/cdk-gitlab)
![Release](https://github.com/pahud/cdk-gitlab/workflows/Release/badge.svg)

# cdk-gitlab

High level CDK construct to provision GitLab integrations with AWS

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab import Provider, FargateJobExecutor, FargateRunner, JobExecutorImage

provider = Provider(stack, "GitlabProvider", vpc=vpc)

# create a Amazon EKS cluster
provider.create_fargate_eks_cluster(stack, "GitlabEksCluster",
    cluster_options={
        "vpc": vpc,
        "version": eks.KubernetesVersion.V1_19
    }
)

# create a default fargate runner with its job executor
provider.create_fargate_runner()

# alternatively, create the runner and the executor indivicually.
# first, create the executor
executor = FargateJobExecutor(stack, "JobExecutor",
    image=JobExecutorImage.DEBIAN
)

# second, create the runner with the task definition of the executor
FargateRunner(stack, "FargateRunner",
    vpc=vpc,
    executor=executor
)

# TBD - create Amazon EC2 runner for the GitLab
provider.create_ec2_runner(...)
```

# Fargate Runner with Aamzon ECS

On deployment with `createFargateRunner()`, the **Fargate Runner** will be provisioned in Amazon ECS with AWS Fargate and [Amazon ECS Capacity Providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-capacity-providers.html). By default, the `FARGATE` and `FARGATE_SPOT` capacity providers are available for the Amazon ECS cluster and the runner and job executor will run on `FARGATE_SPOT`. You can specify your custom `clusterDefaultCapacityProviderStrategy` and `serviceDefaultCapacityProviderStrategy` properties from the `FargateRunner` construct for different capacity provider strategies.

# Deploy

```sh
cdk deploy -c GITLAB_REGISTRATION_TOKEN=<TOKEN>
```
