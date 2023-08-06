[![awscdk-jsii-template](https://img.shields.io/badge/built%20with-awscdk--jsii--template-blue)](https://github.com/pahud/awscdk-jsii-template)
[![NPM version](https://badge.fury.io/js/eks-spot-blocks.svg)](https://badge.fury.io/js/eks-spot-blocks)
[![PyPI version](https://badge.fury.io/py/eks-spot-blocks.svg)](https://badge.fury.io/py/eks-spot-blocks)
![Release](https://github.com/pahud/eks-spot-blocks/workflows/Release/badge.svg)

# cdk-eks-spotblocks

`cdk-eks-spotblocks` is a JSII construct library for AWS CDK to provison Amazon EKS cluster with `EC2 Spot Blocks` for defined workloads with the advantages of ensured availability and considerable price reduction for your kubernetes workload.

![](images/pahud_eks-spot2.svg)

## Features

* [x] support the upstream AWS CDK `aws-eks` construct libraries by extending its capabilities
* [x] `addSpotFleet()` to create your spot fleet for your cluster
* [x] define your `blockDuration`, `validFrom` and `validUntil` for fine-graned control
* [x] support any AWS commercial regions which has Amazon EKS and EC2 Spot Block support, including AWS China regions

## Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import eks_spot_blocks as eksspot
import aws_cdk.core as cdk
import aws_cdk.aws_ec2 as ec2

cluster_stack = eksspot.EksSpotCluster(stack, "Cluster",
    cluster_version=eks.KubernetesVersion.V1_16
)

cluster_stack.add_spot_fleet("FirstFleet",
    block_duration=eksspot.BlockDuration.SIX_HOURS,
    target_capacity=1,
    default_instance_type=ec2.InstanceType("p3.2xlarge"),
    valid_until=cluster_stack.add_hours(Date(), 6).to_iSOString(),
    terminate_instances_with_expiration=True
)

cluster_stack.add_spot_fleet("SecondFleet",
    block_duration=eksspot.BlockDuration.ONE_HOUR,
    target_capacity=2,
    default_instance_type=ec2.InstanceType("c5.large"),
    valid_until=cluster_stack.add_hours(Date(), 1).to_iSOString(),
    terminate_instances_with_expiration=True
)
```

check [eks-spot-blocks-demo](https://github.com/pahud/eks-spot-blocks-demo) for a full AWS CDK demo with this construct library.

## Custom AMI support

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster_stack = EksSpotCluster(stack, "Cluster",
    cluster_version=eks.KubernetesVersion.V1_16,
    custom_ami_id="ami-xxxxxx"
)
```

## FAQ

### Does `eks-spot-blocks` support existing eks clusters created by `eksctl`, `terraform` or any other tools?

No. This construct library does not support existing Amazon EKS clusters. You have to create the cluster as well as the spot fleet altogether in this construct library.

### Can I write the CDK in other languages like `Python` and `Java`?

Not at this moment. But we plan to publish this construct with `JSII` so we can install this library via `npm`, `pypi`, `maven` or `nuget`.

### How much time can I block the spotfleet?

You can block the fleet with hourly increments up to 6 hours.

### What happens after the `blockDuration`?

Spot Blocks ensure the availability of your spot instances during the `blockDuration` and avoid termination during the price disruption. After the `blockDuration`, by default, your spot instances will still be in `running` state but it doesn't ensure the availability, which means it might be terminated anytime after the `blockDuration`.

### Can I terminate the fleet immediately after the `blockDuration` to save the money?

Yes. Basically you can configure `validFrom`, `validUntil` and `terminateInstancesWithExpiration` to achieve this.

However, consider the following scenario

```
<deploy start at 1:00>|--------(one hour)-----------------------|<2:00>
                           |<fleet created at 1:05>--------(one-hour block)-------|<2:05>
```

Your fleet will be terminated at `2:00` rather at `2:05`.

### Are `tains` and `labels` supported?

Yes.

(samples TBD)

### Does it support AWS China regions?

Yes. Including **Beijing**(`cn-north-1`) and **Ningxia**(`cn-northwest-1`).

### How much can I save from the EC2 Spot Block compared to the on-demand?

According to this [document](https://aws.amazon.com/ec2/spot/pricing/?nc1=h_ls)

`Spot Instances are also available to run for a predefined duration – in hourly increments up to six hours in length – at a discount of up to 30-50% compared to On-Demand pricing.`

### Will this library become part of the upstream `aws-eks` construct library?

Probably. As it's still in the preliminary stage, we are still collecting feedbacks from the community to make `eks-spot-blocks` ready for production workloads. Eventually we will commit this feature to the upstream `aws-eks` construct library in AWS CDK through pull requests.
