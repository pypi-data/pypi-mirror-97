import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import IgnoreMode as _IgnoreMode_32b624fb
from ..assets import (
    FingerprintOptions as _FingerprintOptions_74cc5811,
    FollowMode as _FollowMode_e1e723bb,
    IAsset as _IAsset_1a883488,
)
from ..aws_ecr import IRepository as _IRepository_77c1519b


@jsii.implements(_IAsset_1a883488)
class DockerImageAsset(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAsset",
):
    '''(experimental) An asset that represents a Docker image.

    The image will be created in build time and uploaded to an ECR repository.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        directory: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_e1e723bb] = None,
        ignore_mode: typing.Optional[_IgnoreMode_32b624fb] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param directory: (experimental) The directory where the Dockerfile is stored.
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: (experimental) Docker target to build to. Default: - no target
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '

        :stability: experimental
        '''
        props = DockerImageAssetProps(
            directory=directory,
            build_args=build_args,
            file=file,
            repository_name=repository_name,
            target=target,
            extra_hash=extra_hash,
            exclude=exclude,
            follow=follow,
            ignore_mode=ignore_mode,
        )

        jsii.create(DockerImageAsset, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceHash")
    def source_hash(self) -> builtins.str:
        '''(experimental) A hash of the source of this asset, which is available at construction time.

        As this is a plain
        string, it can be used in construct IDs in order to enforce creation of a new resource when
        the content hash has changed.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sourceHash"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> builtins.str:
        '''(experimental) The full URI of the image (including a tag).

        Use this reference to pull
        the asset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageUri"))

    @image_uri.setter
    def image_uri(self, value: builtins.str) -> None:
        jsii.set(self, "imageUri", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="repository")
    def repository(self) -> _IRepository_77c1519b:
        '''(experimental) Repository where the image is stored.

        :stability: experimental
        '''
        return typing.cast(_IRepository_77c1519b, jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: _IRepository_77c1519b) -> None:
        jsii.set(self, "repository", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAssetOptions",
    jsii_struct_bases=[_FingerprintOptions_74cc5811],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "build_args": "buildArgs",
        "file": "file",
        "repository_name": "repositoryName",
        "target": "target",
    },
)
class DockerImageAssetOptions(_FingerprintOptions_74cc5811):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_e1e723bb] = None,
        ignore_mode: typing.Optional[_IgnoreMode_32b624fb] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for DockerImageAsset.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: (experimental) Docker target to build to. Default: - no target

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional[_FollowMode_e1e723bb]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional[_FollowMode_e1e723bb], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_IgnoreMode_32b624fb]:
        '''(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_IgnoreMode_32b624fb], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        :default: - the default ECR repository for CDK assets

        :deprecated:

        to control the location of docker image assets, please override
        ``Stack.addDockerImageAsset``. this feature will be removed in future
        releases.

        :stability: deprecated
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker target to build to.

        :default: - no target

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ecr_assets.DockerImageAssetProps",
    jsii_struct_bases=[DockerImageAssetOptions],
    name_mapping={
        "exclude": "exclude",
        "follow": "follow",
        "ignore_mode": "ignoreMode",
        "extra_hash": "extraHash",
        "build_args": "buildArgs",
        "file": "file",
        "repository_name": "repositoryName",
        "target": "target",
        "directory": "directory",
    },
)
class DockerImageAssetProps(DockerImageAssetOptions):
    def __init__(
        self,
        *,
        exclude: typing.Optional[typing.List[builtins.str]] = None,
        follow: typing.Optional[_FollowMode_e1e723bb] = None,
        ignore_mode: typing.Optional[_IgnoreMode_32b624fb] = None,
        extra_hash: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        directory: builtins.str,
    ) -> None:
        '''(experimental) Props for DockerImageAssets.

        :param exclude: (deprecated) Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: (deprecated) A strategy for how to handle symlinks. Default: Never
        :param ignore_mode: (deprecated) The ignore behavior to use for exclude patterns. Default: - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the '
        :param extra_hash: (deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs). Default: - hash is only based on source content
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Since Docker build arguments are resolved before deployment, keys and values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or ``queue.queueUrl``). Default: - no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: 'Dockerfile'
        :param repository_name: (deprecated) ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - the default ECR repository for CDK assets
        :param target: (experimental) Docker target to build to. Default: - no target
        :param directory: (experimental) The directory where the Dockerfile is stored.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "directory": directory,
        }
        if exclude is not None:
            self._values["exclude"] = exclude
        if follow is not None:
            self._values["follow"] = follow
        if ignore_mode is not None:
            self._values["ignore_mode"] = ignore_mode
        if extra_hash is not None:
            self._values["extra_hash"] = extra_hash
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Glob patterns to exclude from the copy.

        :default: nothing is excluded

        :stability: deprecated
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def follow(self) -> typing.Optional[_FollowMode_e1e723bb]:
        '''(deprecated) A strategy for how to handle symlinks.

        :default: Never

        :stability: deprecated
        '''
        result = self._values.get("follow")
        return typing.cast(typing.Optional[_FollowMode_e1e723bb], result)

    @builtins.property
    def ignore_mode(self) -> typing.Optional[_IgnoreMode_32b624fb]:
        '''(deprecated) The ignore behavior to use for exclude patterns.

        :default:

        - GLOB for file assets, DOCKER or GLOB for docker assets depending on whether the
        '

        :stability: deprecated
        :aws-cdk: /aws-ecr-assets:dockerIgnoreSupport' flag is set.
        '''
        result = self._values.get("ignore_mode")
        return typing.cast(typing.Optional[_IgnoreMode_32b624fb], result)

    @builtins.property
    def extra_hash(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Extra information to encode into the fingerprint (e.g. build instructions and other inputs).

        :default: - hash is only based on source content

        :stability: deprecated
        '''
        result = self._values.get("extra_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args to pass to the ``docker build`` command.

        Since Docker build arguments are resolved before deployment, keys and
        values cannot refer to unresolved tokens (such as ``lambda.functionArn`` or
        ``queue.queueUrl``).

        :default: - no build args are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the Dockerfile (relative to the directory).

        :default: 'Dockerfile'

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ECR repository name.

        Specify this property if you need to statically address the image, e.g.
        from a Kubernetes Pod. Note, this is only the repository name, without the
        registry and the tag parts.

        :default: - the default ECR repository for CDK assets

        :deprecated:

        to control the location of docker image assets, please override
        ``Stack.addDockerImageAsset``. this feature will be removed in future
        releases.

        :stability: deprecated
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker target to build to.

        :default: - no target

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''(experimental) The directory where the Dockerfile is stored.

        :stability: experimental
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAssetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DockerImageAsset",
    "DockerImageAssetOptions",
    "DockerImageAssetProps",
]

publication.publish()
