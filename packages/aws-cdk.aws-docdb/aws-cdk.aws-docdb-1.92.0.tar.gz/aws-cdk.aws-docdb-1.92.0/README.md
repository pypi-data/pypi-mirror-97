# Amazon DocumentDB Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Starting a Clustered Database

To set up a clustered DocumentDB database, define a `DatabaseCluster`. You must
always launch a database in a VPC. Use the `vpcSubnets` attribute to control whether
your instances will be launched privately or publicly:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster = DatabaseCluster(self, "Database",
    master_user={
        "username": "myuser"
    },
    instance_props={
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
        "vpc_subnets": {
            "subnet_type": ec2.SubnetType.PUBLIC
        },
        "vpc": vpc
    }
)
```

By default, the master password will be generated and stored in AWS Secrets Manager with auto-generated description.

Your cluster will be empty by default.

## Connecting

To control who can access the cluster, use the `.connections` attribute. DocumentDB databases have a default port, so
you don't need to specify the port:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster.connections.allow_default_port_from_any_ipv4("Open to the world")
```

The endpoints to access your database cluster will be available as the `.clusterEndpoint` and `.clusterReadEndpoint`
attributes:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
write_address = cluster.cluster_endpoint.socket_address
```

## Rotating credentials

When the master password is generated and stored in AWS Secrets Manager, it can be rotated automatically:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_single_user()
```

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
cluster = docdb.DatabaseCluster(stack, "Database",
    master_user=Login(
        username="docdb"
    ),
    instance_props={
        "instance_type": ec2.InstanceType.of(ec2.InstanceClass.R5, ec2.InstanceSize.LARGE),
        "vpc": vpc
    },
    removal_policy=cdk.RemovalPolicy.DESTROY
)

cluster.add_rotation_single_user()
```

The multi user rotation scheme is also available:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
cluster.add_rotation_multi_user("MyUser",
    secret=my_imported_secret
)
```

It's also possible to create user credentials together with the cluster and add rotation:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_user_secret = docdb.DatabaseSecret(self, "MyUserSecret",
    username="myuser",
    master_secret=cluster.secret
)
my_user_secret_attached = my_user_secret.attach(cluster)# Adds DB connections information in the secret

cluster.add_rotation_multi_user("MyUser", # Add rotation using the multi user scheme
    secret=my_user_secret_attached)
```

**Note**: This user must be created manually in the database using the master credentials.
The rotation will start as soon as this user exists.

See also [@aws-cdk/aws-secretsmanager](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-secretsmanager/README.md) for credentials rotation of existing clusters.
