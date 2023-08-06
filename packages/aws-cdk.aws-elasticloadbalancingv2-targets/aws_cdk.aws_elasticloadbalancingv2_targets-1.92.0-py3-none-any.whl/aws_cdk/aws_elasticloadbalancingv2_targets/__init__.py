'''
# Targets for AWS Elastic Load Balancing V2

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This package contains targets for ELBv2. See the README of the `@aws-cdk/aws-elasticloadbalancingv2` library.
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
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_lambda


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class InstanceIdTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceIdTarget",
):
    '''(experimental) An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    :stability: experimental
    '''

    def __init__(
        self,
        instance_id: builtins.str,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        :stability: experimental
        '''
        jsii.create(InstanceIdTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


class InstanceTarget(
    InstanceIdTarget,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceTarget",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        instance: aws_cdk.aws_ec2.Instance,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Create a new Instance target.

        :param instance: Instance to register to.
        :param port: Override the default port for the target group.

        :stability: experimental
        '''
        jsii.create(InstanceTarget, self, [instance, port])


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class IpTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.IpTarget",
):
    '''(experimental) An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    :stability: experimental
    '''

    def __init__(
        self,
        ip_address: builtins.str,
        port: typing.Optional[jsii.Number] = None,
        availability_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        :stability: experimental
        '''
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget)
class LambdaTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.LambdaTarget",
):
    '''
    :stability: experimental
    '''

    def __init__(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        '''(experimental) Create a new Lambda target.

        :param fn: -

        :stability: experimental
        '''
        jsii.create(LambdaTarget, self, [fn])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToApplicationTargetGroup", [target_group]))

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(
        self,
        target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup,
    ) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        '''(experimental) Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        :stability: experimental
        '''
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps, jsii.invoke(self, "attachToNetworkTargetGroup", [target_group]))


__all__ = [
    "InstanceIdTarget",
    "InstanceTarget",
    "IpTarget",
    "LambdaTarget",
]

publication.publish()
