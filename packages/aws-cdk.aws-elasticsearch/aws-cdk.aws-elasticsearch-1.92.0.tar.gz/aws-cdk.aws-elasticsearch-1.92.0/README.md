# Amazon Elasticsearch Service Construct Library

<!--BEGIN STABILITY BANNER-->---


Features                           | Stability
-----------------------------------|----------------------------------------------------------------
CFN Resources                      | ![Stable](https://img.shields.io/badge/stable-success.svg?style=for-the-badge)
Higher level constructs for Domain | ![Experimental](https://img.shields.io/badge/experimental-important.svg?style=for-the-badge)

> **CFN Resources:** All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always
> stable and safe to use.

<!-- -->

> **Experimental:** Higher level constructs in this module that are marked as experimental are
> under active development. They are subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and
> breaking changes will be announced in the release notes. This means that while you may use them,
> you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Quick start

Create a development cluster by simply specifying the version:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticsearch as es

dev_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1
)
```

To perform version upgrades without replacing the entire domain, specify the `enableVersionUpgrade` property.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_elasticsearch as es

dev_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_9,
    enable_version_upgrade=True
)
```

Create a production grade cluster by also specifying things like capacity and az distribution

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
prod_domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    capacity={
        "master_nodes": 5,
        "data_nodes": 20
    },
    ebs={
        "volume_size": 20
    },
    zone_awareness={
        "availability_zone_count": 3
    },
    logging={
        "slow_search_log_enabled": True,
        "app_log_enabled": True,
        "slow_index_log_enabled": True
    }
)
```

This creates an Elasticsearch cluster and automatically sets up log groups for
logging the domain logs and slow search logs.

## Importing existing domains

To import an existing domain into your CDK application, use the `Domain.fromDomainEndpoint` factory method.
This method accepts a domain endpoint of an already existing domain:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain_endpoint = "https://my-domain-jcjotrt6f7otem4sqcwbch3c4u.us-east-1.es.amazonaws.com"
domain = Domain.from_domain_endpoint(self, "ImportedDomain", domain_endpoint)
```

## Permissions

### IAM

Helper methods also exist for managing access to the domain.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
lambda_ = lambda_.Function(self, "Lambda")

# Grant write access to the app-search index
domain.grant_index_write("app-search", lambda_)

# Grant read access to the 'app-search/_search' path
domain.grant_path_read("app-search/_search", lambda_)
```

## Encryption

The domain can also be created with encryption enabled:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_4,
    ebs={
        "volume_size": 100,
        "volume_type": EbsDeviceVolumeType.GENERAL_PURPOSE_SSD
    },
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    }
)
```

This sets up the domain with node to node encryption and encryption at
rest. You can also choose to supply your own KMS key to use for encryption at
rest.

## Metrics

Helper methods exist to access common domain metrics for example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
free_storage_space = domain.metric_free_storage_space()
master_sys_memory_utilization = domain.metric("MasterSysMemoryUtilization")
```

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Fine grained access control

The domain can also be created with a master user configured. The password can
be supplied or dynamically created if not supplied.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    },
    fine_grained_access_control={
        "master_user_name": "master-user"
    }
)

master_user_password = domain.master_user_password
```

## Using unsigned basic auth

For convenience, the domain can be configured to allow unsigned HTTP requests
that use basic auth. Unless the domain is configured to be part of a VPC this
means anyone can access the domain using the configured master username and
password.

To enable unsigned basic auth access the domain is configured with an access
policy that allows anyonmous requests, HTTPS required, node to node encryption,
encryption at rest and fine grained access control.

If the above settings are not set they will be configured as part of enabling
unsigned basic auth. If they are set with conflicting values, an error will be
thrown.

If no master user is configured a default master user is created with the
username `admin`.

If no password is configured a default master user password is created and
stored in the AWS Secrets Manager as secret. The secret has the prefix
`<domain id>MasterUser`.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    use_unsigned_basic_auth=True
)

master_user_password = domain.master_user_password
```

## Audit logs

Audit logs can be enabled for a domain, but only when fine grained access control is enabled.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_1,
    enforce_https=True,
    node_to_node_encryption=True,
    encryption_at_rest={
        "enabled": True
    },
    fine_grained_access_control={
        "master_user_name": "master-user"
    },
    logging={
        "audit_log_enabled": True,
        "slow_search_log_enabled": True,
        "app_log_enabled": True,
        "slow_index_log_enabled": True
    }
)
```

## UltraWarm

UltraWarm nodes can be enabled to provide a cost-effective way to store large amounts of read-only data.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
domain = es.Domain(self, "Domain",
    version=es.ElasticsearchVersion.V7_9,
    capacity={
        "master_nodes": 2,
        "warm_nodes": 2,
        "warm_instance_type": "ultrawarm1.medium.elasticsearch"
    }
)
```

## Custom endpoint

Custom endpoints can be configured to reach the ES domain under a custom domain name.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Domain(stack, "Domain",
    version=ElasticsearchVersion.V7_7,
    custom_endpoint={
        "domain_name": "search.example.com"
    }
)
```

It is also possible to specify a custom certificate instead of the auto-generated one.

Additionally, an automatic CNAME-Record is created if a hosted zone is provided for the custom endpoint
