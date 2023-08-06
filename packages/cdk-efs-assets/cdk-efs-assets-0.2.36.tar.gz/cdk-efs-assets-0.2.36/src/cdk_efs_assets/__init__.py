'''
[![NPM version](https://badge.fury.io/js/cdk-efs-assets.svg)](https://badge.fury.io/js/cdk-efs-assets)
[![PyPI version](https://badge.fury.io/py/cdk-efs-assets.svg)](https://badge.fury.io/py/cdk-efs-assets)
![Release](https://github.com/pahud/cdk-efs-assets/workflows/Release/badge.svg)

# cdk-efs-assets

CDK construct library to populate Amazon EFS assets from Github or S3. If the source is S3, the construct also optionally supports updating the contents in EFS if a new zip file is uploaded to S3.

## Install

TypeScript/JavaScript:

```bash
npm i cdk-efs-assets
```

## SyncedAccessPoint

The main construct that is used to provide this EFS sync functionality is `SyncedAccessPoint`. This extends the standard EFS `AccessPoint` construct, and takes an additional `SyncSource` constructor property which defines the source to sync assets from. The `SyncedAccessPoint` instance can be used anywhere an `AccessPoint` can be used. For example, to specify a volume in a Task Definition:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
task_definition = ecs.FargateTaskDefinition(self, "TaskDefinition",
    (SpreadAssignment ...
      volumes
      volumes), {
        "name": "efs-storage",
        "efs_volume_configuration": {
            "file_system_id": shared_file_system.file_system_id,
            "transit_encryption": "ENABLED",
            "authorization_config": {
                "access_point_id": synced_access_point.access_point_id
            }
        }
    } , =
)
```

## SyncSource

Use the `SyncSource` static functions to create a `SyncSource` instance that can then be passed as a `SyncedAccessPoint` constructor property to define the source of the sync. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SyncedAccessPoint(stack, "EfsAccessPoint",
    (SpreadAssignment ...
      syncSource
      sync_source), SyncSource=SyncSource, =.github(
        vpc=vpc,
        repository="https://github.com/pahud/cdk-efs-assets.git"
    )
)
```

### syncDirectoryPath

By default, the synced EFS assets are placed into a directory corresponding to the type of the sync source. For example, the default behavior of the GitHub source is to place the copied files into a directory named the same as the repository name (for a repository specified as 'https://github.com/pahud/cdk-efs-assets.git', the directory name would be 'cdk-efs-assets'), while the default behavior of the S3 archive source is to place the copied files into a directory named the same as the zip file (for a zip file name of 'assets.zip', the directory name would be 'assets').

If you wish to override this default behavior, specify a value for the `syncDirectoryPath` property that is passed into the `SyncSource` call.

If you are using the `AccessPoint` in an ECS/Fargate Task Definition, you probably will want to override the value of `syncDirectoryPath` to '/'. This will place the file contents in the root directory of the Access Point. The reason for this is that when you create a volume that is referencing an EFS Access Point, you are not allowed to specify any path other than the root directory in the task definition configuration.

## How to use SyncedAccessPoint initialized with files provisioned from GitHub repository

This will sync assets from a GitHub repository to a directory (by default, the output directory is named after the repository name) in the EFS AccessPoint:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import SyncSource, SyncedAccessPoint

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

efs_access_point = SyncedAccessPoint(stack, "GithubAccessPoint",
    file_system=fs,
    path="/demo-github",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    },
    sync_source=SyncSource.github(
        vpc=vpc,
        repository="https://github.com/pahud/cdk-efs-assets.git"
    )
)
```

### Github private repository support

To clone a github private repository, you need to generate your github **PAT(Personal Access Token)** and store the token in **AWS Secrets Manager** secret.

For example, if your PAT is stored in the AWS Secret manager with the secret ID `github` and the key `oauth_token`, you can specify the `secret` property as the sample below. Under the covers the lambda function will format the full github repository uri with your **PAT** and successfully git clone the private repository to the efs filesystem.

Store your PAT into the AWS Secrets Manager with AWS CLI:

```sh
aws secretsmanager create-secret \
--name github \
--secret-string '{"oauth_token":"MYOAUTHTOKEN"}'
```

Configure the `secret` property to allow lambda to retrieve the **PAT** from the secret:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
SyncSource.github(
    vpc=vpc,
    repository="https://github.com/username/repo.git",
    secret={
        "id": "github",
        "key": "oauth_token"
    }
)
```

## How to use SyncedAccessPoint initialized with files provisioned from zip file stored in S3

This will sync assets from a zip file stored in an S3 bucket to a directory (by default, the output directory is named after the zip file name) in the EFS AccessPoint:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_efs_assets import S3ArchiveSync

app = App()

env = {
    "region": process.env.CDK_DEFAULT_REGION ?? AWS_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = Stack(app, "testing-stack", env=env)

vpc = ec2.Vpc.from_lookup(stack, "Vpc", is_default=True)

fs = efs.FileSystem(stack, "Filesystem",
    vpc=vpc,
    removal_policy=RemovalPolicy.DESTROY
)

bucket = Bucket.from_bucket_name(self, "Bucket", "demo-bucket")

efs_access_point = SyncedAccessPoint(stack, "EfsAccessPoint",
    file_system=fs,
    path="/demo-s3",
    create_acl={
        "owner_gid": "1001",
        "owner_uid": "1001",
        "permissions": "0755"
    },
    posix_user={
        "uid": "1001",
        "gid": "1001"
    },
    sync_source=SyncSource.s3_archive(
        vpc=vpc,
        bucket=bucket,
        zip_file_path="folder/foo.zip"
    )
)
```

### syncOnUpdate

If the `syncOnUpdate` property is set to `true` (defaults to `true`), then the specified zip file path will be monitored, and if a new object is uploaded to the path, then it will resync the data to EFS. Note that to use this functionality, you must have a CloudTrail Trail in your account that captures the desired S3 write data event.

*WARNING*: The contents of the extraction directory in the access point will be destroyed before extracting the zip file.
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
import aws_cdk.aws_efs
import aws_cdk.aws_s3
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-efs-assets.GithubSecret",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "key": "key"},
)
class GithubSecret:
    def __init__(self, *, id: builtins.str, key: builtins.str) -> None:
        '''
        :param id: The secret ID from AWS Secrets Manager.
        :param key: The key of the secret.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "key": key,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The secret ID from AWS Secrets Manager.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The key of the secret.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubSecret(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyncSource(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-efs-assets.SyncSource",
):
    @builtins.staticmethod
    def __jsii_proxy_class__() -> typing.Type["_SyncSourceProxy"]:
        return _SyncSourceProxy

    def __init__(self) -> None:
        jsii.create(SyncSource, self, [])

    @jsii.member(jsii_name="github") # type: ignore[misc]
    @builtins.classmethod
    def github(
        cls,
        *,
        repository: builtins.str,
        secret: typing.Optional[GithubSecret] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        sync_directory_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "SyncSource":
        '''
        :param repository: The github repository HTTP URI.
        :param secret: The github secret for the private repository.
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param sync_directory_path: The (absolute) directory path inside the EFS AccessPoint to sync files to. Specify '/' to restore synced files to the root directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default behavior is to restore to a directory matching the name of the repository)
        :param timeout: Timeout duration for sync Lambda function. (optional, default: Duration.minutes(3))
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        '''
        props = GithubSourceProps(
            repository=repository,
            secret=secret,
            vpc=vpc,
            sync_directory_path=sync_directory_path,
            timeout=timeout,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("SyncSource", jsii.sinvoke(cls, "github", [props]))

    @jsii.member(jsii_name="s3Archive") # type: ignore[misc]
    @builtins.classmethod
    def s3_archive(
        cls,
        *,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_file_path: builtins.str,
        sync_on_update: typing.Optional[builtins.bool] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        sync_directory_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> "SyncSource":
        '''
        :param bucket: The S3 bucket containing the archive file.
        :param zip_file_path: The path of the zip file to extract in the S3 bucket.
        :param sync_on_update: If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered. Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3 event. (optional, default: true)
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param sync_directory_path: The (absolute) directory path inside the EFS AccessPoint to sync files to. Specify '/' to restore synced files to the root directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default behavior is to restore to a directory matching the name of the repository)
        :param timeout: Timeout duration for sync Lambda function. (optional, default: Duration.minutes(3))
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        '''
        props = S3ArchiveSourceProps(
            bucket=bucket,
            zip_file_path=zip_file_path,
            sync_on_update=sync_on_update,
            vpc=vpc,
            sync_directory_path=sync_directory_path,
            timeout=timeout,
            vpc_subnets=vpc_subnets,
        )

        return typing.cast("SyncSource", jsii.sinvoke(cls, "s3Archive", [props]))


class _SyncSourceProxy(SyncSource):
    pass


@jsii.data_type(
    jsii_type="cdk-efs-assets.SyncSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "sync_directory_path": "syncDirectoryPath",
        "timeout": "timeout",
        "vpc_subnets": "vpcSubnets",
    },
)
class SyncSourceProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        sync_directory_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param sync_directory_path: The (absolute) directory path inside the EFS AccessPoint to sync files to. Specify '/' to restore synced files to the root directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default behavior is to restore to a directory matching the name of the repository)
        :param timeout: Timeout duration for sync Lambda function. (optional, default: Duration.minutes(3))
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if sync_directory_path is not None:
            self._values["sync_directory_path"] = sync_directory_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The VPC of the Amazon EFS Filesystem.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def sync_directory_path(self) -> typing.Optional[builtins.str]:
        '''The (absolute) directory path inside the EFS AccessPoint to sync files to.

        Specify '/' to restore synced files to the root
        directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default
        behavior is to restore to a directory matching the name of the repository)
        '''
        result = self._values.get("sync_directory_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''Timeout duration for sync Lambda function.

        (optional, default: Duration.minutes(3))
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.'''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyncSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_efs.IAccessPoint)
class SyncedAccessPoint(
    aws_cdk.aws_efs.AccessPoint,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-efs-assets.SyncedAccessPoint",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        sync_source: SyncSource,
        file_system: aws_cdk.aws_efs.IFileSystem,
        create_acl: typing.Optional[aws_cdk.aws_efs.Acl] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[aws_cdk.aws_efs.PosixUser] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sync_source: 
        :param file_system: (experimental) The efs filesystem.
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced
        '''
        props = SyncedAccessPointProps(
            sync_source=sync_source,
            file_system=file_system,
            create_acl=create_acl,
            path=path,
            posix_user=posix_user,
        )

        jsii.create(SyncedAccessPoint, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-efs-assets.SyncedAccessPointProps",
    jsii_struct_bases=[aws_cdk.aws_efs.AccessPointProps],
    name_mapping={
        "create_acl": "createAcl",
        "path": "path",
        "posix_user": "posixUser",
        "file_system": "fileSystem",
        "sync_source": "syncSource",
    },
)
class SyncedAccessPointProps(aws_cdk.aws_efs.AccessPointProps):
    def __init__(
        self,
        *,
        create_acl: typing.Optional[aws_cdk.aws_efs.Acl] = None,
        path: typing.Optional[builtins.str] = None,
        posix_user: typing.Optional[aws_cdk.aws_efs.PosixUser] = None,
        file_system: aws_cdk.aws_efs.IFileSystem,
        sync_source: SyncSource,
    ) -> None:
        '''
        :param create_acl: (experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory. If the root directory specified by ``path`` does not exist, EFS creates the root directory and applies the permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``. Default: - None. The directory specified by ``path`` must exist.
        :param path: (experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system. Default: '/'
        :param posix_user: (experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point. Specify this to enforce a user identity using an access point. Default: - user identity not enforced
        :param file_system: (experimental) The efs filesystem.
        :param sync_source: 
        '''
        if isinstance(create_acl, dict):
            create_acl = aws_cdk.aws_efs.Acl(**create_acl)
        if isinstance(posix_user, dict):
            posix_user = aws_cdk.aws_efs.PosixUser(**posix_user)
        self._values: typing.Dict[str, typing.Any] = {
            "file_system": file_system,
            "sync_source": sync_source,
        }
        if create_acl is not None:
            self._values["create_acl"] = create_acl
        if path is not None:
            self._values["path"] = path
        if posix_user is not None:
            self._values["posix_user"] = posix_user

    @builtins.property
    def create_acl(self) -> typing.Optional[aws_cdk.aws_efs.Acl]:
        '''(experimental) Specifies the POSIX IDs and permissions to apply when creating the access point's root directory.

        If the
        root directory specified by ``path`` does not exist, EFS creates the root directory and applies the
        permissions specified here. If the specified ``path`` does not exist, you must specify ``createAcl``.

        :default: - None. The directory specified by ``path`` must exist.

        :stability: experimental
        '''
        result = self._values.get("create_acl")
        return typing.cast(typing.Optional[aws_cdk.aws_efs.Acl], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the path on the EFS file system to expose as the root directory to NFS clients using the access point to access the EFS file system.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_user(self) -> typing.Optional[aws_cdk.aws_efs.PosixUser]:
        '''(experimental) The full POSIX identity, including the user ID, group ID, and any secondary group IDs, on the access point that is used for all file system operations performed by NFS clients using the access point.

        Specify this to enforce a user identity using an access point.

        :default: - user identity not enforced

        :see: - `Enforcing a User Identity Using an Access Point <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_
        :stability: experimental
        '''
        result = self._values.get("posix_user")
        return typing.cast(typing.Optional[aws_cdk.aws_efs.PosixUser], result)

    @builtins.property
    def file_system(self) -> aws_cdk.aws_efs.IFileSystem:
        '''(experimental) The efs filesystem.

        :stability: experimental
        '''
        result = self._values.get("file_system")
        assert result is not None, "Required property 'file_system' is missing"
        return typing.cast(aws_cdk.aws_efs.IFileSystem, result)

    @builtins.property
    def sync_source(self) -> SyncSource:
        result = self._values.get("sync_source")
        assert result is not None, "Required property 'sync_source' is missing"
        return typing.cast(SyncSource, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyncedAccessPointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-efs-assets.GithubSourceProps",
    jsii_struct_bases=[SyncSourceProps],
    name_mapping={
        "vpc": "vpc",
        "sync_directory_path": "syncDirectoryPath",
        "timeout": "timeout",
        "vpc_subnets": "vpcSubnets",
        "repository": "repository",
        "secret": "secret",
    },
)
class GithubSourceProps(SyncSourceProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        sync_directory_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        repository: builtins.str,
        secret: typing.Optional[GithubSecret] = None,
    ) -> None:
        '''
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param sync_directory_path: The (absolute) directory path inside the EFS AccessPoint to sync files to. Specify '/' to restore synced files to the root directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default behavior is to restore to a directory matching the name of the repository)
        :param timeout: Timeout duration for sync Lambda function. (optional, default: Duration.minutes(3))
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        :param repository: The github repository HTTP URI.
        :param secret: The github secret for the private repository.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        if isinstance(secret, dict):
            secret = GithubSecret(**secret)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "repository": repository,
        }
        if sync_directory_path is not None:
            self._values["sync_directory_path"] = sync_directory_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The VPC of the Amazon EFS Filesystem.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def sync_directory_path(self) -> typing.Optional[builtins.str]:
        '''The (absolute) directory path inside the EFS AccessPoint to sync files to.

        Specify '/' to restore synced files to the root
        directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default
        behavior is to restore to a directory matching the name of the repository)
        '''
        result = self._values.get("sync_directory_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''Timeout duration for sync Lambda function.

        (optional, default: Duration.minutes(3))
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.'''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The github repository HTTP URI.'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> typing.Optional[GithubSecret]:
        '''The github secret for the private repository.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[GithubSecret], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GithubSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-efs-assets.S3ArchiveSourceProps",
    jsii_struct_bases=[SyncSourceProps],
    name_mapping={
        "vpc": "vpc",
        "sync_directory_path": "syncDirectoryPath",
        "timeout": "timeout",
        "vpc_subnets": "vpcSubnets",
        "bucket": "bucket",
        "zip_file_path": "zipFilePath",
        "sync_on_update": "syncOnUpdate",
    },
)
class S3ArchiveSourceProps(SyncSourceProps):
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        sync_directory_path: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        bucket: aws_cdk.aws_s3.IBucket,
        zip_file_path: builtins.str,
        sync_on_update: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param vpc: The VPC of the Amazon EFS Filesystem.
        :param sync_directory_path: The (absolute) directory path inside the EFS AccessPoint to sync files to. Specify '/' to restore synced files to the root directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default behavior is to restore to a directory matching the name of the repository)
        :param timeout: Timeout duration for sync Lambda function. (optional, default: Duration.minutes(3))
        :param vpc_subnets: Where to place the network interfaces within the VPC.
        :param bucket: The S3 bucket containing the archive file.
        :param zip_file_path: The path of the zip file to extract in the S3 bucket.
        :param sync_on_update: If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered. Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3 event. (optional, default: true)
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
            "bucket": bucket,
            "zip_file_path": zip_file_path,
        }
        if sync_directory_path is not None:
            self._values["sync_directory_path"] = sync_directory_path
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if sync_on_update is not None:
            self._values["sync_on_update"] = sync_on_update

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        '''The VPC of the Amazon EFS Filesystem.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def sync_directory_path(self) -> typing.Optional[builtins.str]:
        '''The (absolute) directory path inside the EFS AccessPoint to sync files to.

        Specify '/' to restore synced files to the root
        directory. (optional, default: a source-specific directory path. For example, for the GitHub source, the default
        behavior is to restore to a directory matching the name of the repository)
        '''
        result = self._values.get("sync_directory_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''Timeout duration for sync Lambda function.

        (optional, default: Duration.minutes(3))
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.'''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        '''The S3 bucket containing the archive file.'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def zip_file_path(self) -> builtins.str:
        '''The path of the zip file to extract in the S3 bucket.'''
        result = self._values.get("zip_file_path")
        assert result is not None, "Required property 'zip_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sync_on_update(self) -> typing.Optional[builtins.bool]:
        '''If this is set to true, then whenever a new object is uploaded to the specified path, an EFS sync will be triggered.

        Currently, this functionality depends on at least one CloudTrail Trail existing in your account that captures the S3
        event.

        (optional, default: true)
        '''
        result = self._values.get("sync_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ArchiveSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GithubSecret",
    "GithubSourceProps",
    "S3ArchiveSourceProps",
    "SyncSource",
    "SyncSourceProps",
    "SyncedAccessPoint",
    "SyncedAccessPointProps",
]

publication.publish()
