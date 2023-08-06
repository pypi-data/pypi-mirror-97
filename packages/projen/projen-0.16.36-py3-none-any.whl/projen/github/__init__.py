import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from .. import (
    Component as _Component_2b0ad27f,
    Project as _Project_57d89203,
    TextFile as _TextFile_4a74808c,
    YamlFile as _YamlFile_909731b0,
)


class AutoMerge(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.AutoMerge",
):
    '''(experimental) Sets up mergify to merging approved pull requests.

    If ``buildJob`` is specified, the specified GitHub workflow job ID is required
    to succeed in order for the PR to be merged.

    ``approvedReviews`` specified the number of code review approvals required for
    the PR to be merged.

    :stability: experimental
    '''

    def __init__(
        self,
        project: _Project_57d89203,
        *,
        approved_reviews: typing.Optional[jsii.Number] = None,
        auto_merge_label: typing.Optional[builtins.str] = None,
        build_job: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param project: -
        :param approved_reviews: (experimental) Number of approved code reviews. Default: 1
        :param auto_merge_label: (experimental) Automatically merge PRs that build successfully and have this label. To disable, set this value to an empty string. Default: "auto-merge"
        :param build_job: (experimental) The GitHub job ID of the build workflow.

        :stability: experimental
        '''
        options = AutoMergeOptions(
            approved_reviews=approved_reviews,
            auto_merge_label=auto_merge_label,
            build_job=build_job,
        )

        jsii.create(AutoMerge, self, [project, options])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="autoMergeLabel")
    def auto_merge_label(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "autoMergeLabel"))


@jsii.data_type(
    jsii_type="projen.github.AutoMergeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "approved_reviews": "approvedReviews",
        "auto_merge_label": "autoMergeLabel",
        "build_job": "buildJob",
    },
)
class AutoMergeOptions:
    def __init__(
        self,
        *,
        approved_reviews: typing.Optional[jsii.Number] = None,
        auto_merge_label: typing.Optional[builtins.str] = None,
        build_job: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param approved_reviews: (experimental) Number of approved code reviews. Default: 1
        :param auto_merge_label: (experimental) Automatically merge PRs that build successfully and have this label. To disable, set this value to an empty string. Default: "auto-merge"
        :param build_job: (experimental) The GitHub job ID of the build workflow.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if approved_reviews is not None:
            self._values["approved_reviews"] = approved_reviews
        if auto_merge_label is not None:
            self._values["auto_merge_label"] = auto_merge_label
        if build_job is not None:
            self._values["build_job"] = build_job

    @builtins.property
    def approved_reviews(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of approved code reviews.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("approved_reviews")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_merge_label(self) -> typing.Optional[builtins.str]:
        '''(experimental) Automatically merge PRs that build successfully and have this label.

        To disable, set this value to an empty string.

        :default: "auto-merge"

        :stability: experimental
        '''
        result = self._values.get("auto_merge_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_job(self) -> typing.Optional[builtins.str]:
        '''(experimental) The GitHub job ID of the build workflow.

        :stability: experimental
        '''
        result = self._values.get("build_job")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoMergeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Dependabot(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.Dependabot",
):
    '''(experimental) Defines dependabot configuration for node projects.

    Since module versions are managed in projen, the versioning strategy will be
    configured to "lockfile-only" which means that only updates that can be done
    on the lockfile itself will be proposed.

    :stability: experimental
    '''

    def __init__(
        self,
        github: "GitHub",
        *,
        auto_merge: typing.Optional[builtins.bool] = None,
        ignore: typing.Optional[typing.List["DependabotIgnore"]] = None,
        ignore_projen: typing.Optional[builtins.bool] = None,
        schedule_interval: typing.Optional["DependabotScheduleInterval"] = None,
        versioning_strategy: typing.Optional["VersioningStrategy"] = None,
    ) -> None:
        '''
        :param github: -
        :param auto_merge: (experimental) Automatically merge dependabot PRs if build CI build passes. Default: true
        :param ignore: (experimental) You can use the ``ignore`` option to customize which dependencies are updated. The ignore option supports the following options. Default: []
        :param ignore_projen: (experimental) Ignores updates to ``projen``. This is required since projen updates may cause changes in committed files and anti-tamper checks will fail. Projen upgrades are covered through the ``ProjenUpgrade`` class. Default: true
        :param schedule_interval: (experimental) How often to check for new versions and raise pull requests. Default: ScheduleInterval.DAILY
        :param versioning_strategy: (experimental) The strategy to use when edits manifest and lock files. Default: VersioningStrategy.LOCKFILE_ONLY The default is to only update the lock file because package.json is controlled by projen and any outside updates will fail the build.

        :stability: experimental
        '''
        options = DependabotOptions(
            auto_merge=auto_merge,
            ignore=ignore,
            ignore_projen=ignore_projen,
            schedule_interval=schedule_interval,
            versioning_strategy=versioning_strategy,
        )

        jsii.create(Dependabot, self, [github, options])

    @jsii.member(jsii_name="addIgnore")
    def add_ignore(
        self,
        dependency_name: builtins.str,
        *versions: builtins.str,
    ) -> None:
        '''(experimental) Ignores a dependency from automatic updates.

        :param dependency_name: Use to ignore updates for dependencies with matching names, optionally using ``*`` to match zero or more characters.
        :param versions: Use to ignore specific versions or ranges of versions. If you want to define a range, use the standard pattern for the package manager (for example: ``^1.0.0`` for npm, or ``~> 2.0`` for Bundler).

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addIgnore", [dependency_name, *versions]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        '''(experimental) The raw dependabot configuration.

        :see: https://docs.github.com/en/github/administering-a-repository/configuration-options-for-dependency-updates
        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "config"))


@jsii.data_type(
    jsii_type="projen.github.DependabotIgnore",
    jsii_struct_bases=[],
    name_mapping={"dependency_name": "dependencyName", "versions": "versions"},
)
class DependabotIgnore:
    def __init__(
        self,
        *,
        dependency_name: builtins.str,
        versions: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) You can use the ``ignore`` option to customize which dependencies are updated.

        The ignore option supports the following options.

        :param dependency_name: (experimental) Use to ignore updates for dependencies with matching names, optionally using ``*`` to match zero or more characters. For Java dependencies, the format of the dependency-name attribute is: ``groupId:artifactId``, for example: ``org.kohsuke:github-api``.
        :param versions: (experimental) Use to ignore specific versions or ranges of versions. If you want to define a range, use the standard pattern for the package manager (for example: ``^1.0.0`` for npm, or ``~> 2.0`` for Bundler).

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "dependency_name": dependency_name,
        }
        if versions is not None:
            self._values["versions"] = versions

    @builtins.property
    def dependency_name(self) -> builtins.str:
        '''(experimental) Use to ignore updates for dependencies with matching names, optionally using ``*`` to match zero or more characters.

        For Java dependencies, the format of the dependency-name attribute is:
        ``groupId:artifactId``, for example: ``org.kohsuke:github-api``.

        :stability: experimental
        '''
        result = self._values.get("dependency_name")
        assert result is not None, "Required property 'dependency_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def versions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Use to ignore specific versions or ranges of versions.

        If you want to
        define a range, use the standard pattern for the package manager (for
        example: ``^1.0.0`` for npm, or ``~> 2.0`` for Bundler).

        :stability: experimental
        '''
        result = self._values.get("versions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DependabotIgnore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.DependabotOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auto_merge": "autoMerge",
        "ignore": "ignore",
        "ignore_projen": "ignoreProjen",
        "schedule_interval": "scheduleInterval",
        "versioning_strategy": "versioningStrategy",
    },
)
class DependabotOptions:
    def __init__(
        self,
        *,
        auto_merge: typing.Optional[builtins.bool] = None,
        ignore: typing.Optional[typing.List[DependabotIgnore]] = None,
        ignore_projen: typing.Optional[builtins.bool] = None,
        schedule_interval: typing.Optional["DependabotScheduleInterval"] = None,
        versioning_strategy: typing.Optional["VersioningStrategy"] = None,
    ) -> None:
        '''
        :param auto_merge: (experimental) Automatically merge dependabot PRs if build CI build passes. Default: true
        :param ignore: (experimental) You can use the ``ignore`` option to customize which dependencies are updated. The ignore option supports the following options. Default: []
        :param ignore_projen: (experimental) Ignores updates to ``projen``. This is required since projen updates may cause changes in committed files and anti-tamper checks will fail. Projen upgrades are covered through the ``ProjenUpgrade`` class. Default: true
        :param schedule_interval: (experimental) How often to check for new versions and raise pull requests. Default: ScheduleInterval.DAILY
        :param versioning_strategy: (experimental) The strategy to use when edits manifest and lock files. Default: VersioningStrategy.LOCKFILE_ONLY The default is to only update the lock file because package.json is controlled by projen and any outside updates will fail the build.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if auto_merge is not None:
            self._values["auto_merge"] = auto_merge
        if ignore is not None:
            self._values["ignore"] = ignore
        if ignore_projen is not None:
            self._values["ignore_projen"] = ignore_projen
        if schedule_interval is not None:
            self._values["schedule_interval"] = schedule_interval
        if versioning_strategy is not None:
            self._values["versioning_strategy"] = versioning_strategy

    @builtins.property
    def auto_merge(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically merge dependabot PRs if build CI build passes.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_merge")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore(self) -> typing.Optional[typing.List[DependabotIgnore]]:
        '''(experimental) You can use the ``ignore`` option to customize which dependencies are updated.

        The ignore option supports the following options.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("ignore")
        return typing.cast(typing.Optional[typing.List[DependabotIgnore]], result)

    @builtins.property
    def ignore_projen(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignores updates to ``projen``.

        This is required since projen updates may cause changes in committed files
        and anti-tamper checks will fail.

        Projen upgrades are covered through the ``ProjenUpgrade`` class.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ignore_projen")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schedule_interval(self) -> typing.Optional["DependabotScheduleInterval"]:
        '''(experimental) How often to check for new versions and raise pull requests.

        :default: ScheduleInterval.DAILY

        :stability: experimental
        '''
        result = self._values.get("schedule_interval")
        return typing.cast(typing.Optional["DependabotScheduleInterval"], result)

    @builtins.property
    def versioning_strategy(self) -> typing.Optional["VersioningStrategy"]:
        '''(experimental) The strategy to use when edits manifest and lock files.

        :default:

        VersioningStrategy.LOCKFILE_ONLY The default is to only update the
        lock file because package.json is controlled by projen and any outside
        updates will fail the build.

        :stability: experimental
        '''
        result = self._values.get("versioning_strategy")
        return typing.cast(typing.Optional["VersioningStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DependabotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.github.DependabotScheduleInterval")
class DependabotScheduleInterval(enum.Enum):
    '''(experimental) How often to check for new versions and raise pull requests for version updates.

    :stability: experimental
    '''

    DAILY = "DAILY"
    '''(experimental) Runs on every weekday, Monday to Friday.

    :stability: experimental
    '''
    WEEKLY = "WEEKLY"
    '''(experimental) Runs once each week.

    By default, this is on Monday.

    :stability: experimental
    '''
    MONTHLY = "MONTHLY"
    '''(experimental) Runs once each month.

    This is on the first day of the month.

    :stability: experimental
    '''


class GitHub(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.GitHub",
):
    '''
    :stability: experimental
    '''

    def __init__(self, project: _Project_57d89203) -> None:
        '''
        :param project: -

        :stability: experimental
        '''
        jsii.create(GitHub, self, [project])

    @jsii.member(jsii_name="addDependabot")
    def add_dependabot(
        self,
        *,
        auto_merge: typing.Optional[builtins.bool] = None,
        ignore: typing.Optional[typing.List[DependabotIgnore]] = None,
        ignore_projen: typing.Optional[builtins.bool] = None,
        schedule_interval: typing.Optional[DependabotScheduleInterval] = None,
        versioning_strategy: typing.Optional["VersioningStrategy"] = None,
    ) -> Dependabot:
        '''
        :param auto_merge: (experimental) Automatically merge dependabot PRs if build CI build passes. Default: true
        :param ignore: (experimental) You can use the ``ignore`` option to customize which dependencies are updated. The ignore option supports the following options. Default: []
        :param ignore_projen: (experimental) Ignores updates to ``projen``. This is required since projen updates may cause changes in committed files and anti-tamper checks will fail. Projen upgrades are covered through the ``ProjenUpgrade`` class. Default: true
        :param schedule_interval: (experimental) How often to check for new versions and raise pull requests. Default: ScheduleInterval.DAILY
        :param versioning_strategy: (experimental) The strategy to use when edits manifest and lock files. Default: VersioningStrategy.LOCKFILE_ONLY The default is to only update the lock file because package.json is controlled by projen and any outside updates will fail the build.

        :stability: experimental
        '''
        options = DependabotOptions(
            auto_merge=auto_merge,
            ignore=ignore,
            ignore_projen=ignore_projen,
            schedule_interval=schedule_interval,
            versioning_strategy=versioning_strategy,
        )

        return typing.cast(Dependabot, jsii.invoke(self, "addDependabot", [options]))

    @jsii.member(jsii_name="addMergifyRules")
    def add_mergify_rules(self, *rules: "MergifyRule") -> None:
        '''
        :param rules: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addMergifyRules", [*rules]))

    @jsii.member(jsii_name="addPullRequestTemplate")
    def add_pull_request_template(
        self,
        *content: builtins.str,
    ) -> "PullRequestTemplate":
        '''
        :param content: -

        :stability: experimental
        '''
        return typing.cast("PullRequestTemplate", jsii.invoke(self, "addPullRequestTemplate", [*content]))

    @jsii.member(jsii_name="addWorkflow")
    def add_workflow(self, name: builtins.str) -> "GithubWorkflow":
        '''
        :param name: -

        :stability: experimental
        '''
        return typing.cast("GithubWorkflow", jsii.invoke(self, "addWorkflow", [name]))


class GithubWorkflow(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.GithubWorkflow",
):
    '''
    :stability: experimental
    '''

    def __init__(self, github: GitHub, name: builtins.str) -> None:
        '''
        :param github: -
        :param name: -

        :stability: experimental
        '''
        jsii.create(GithubWorkflow, self, [github, name])

    @jsii.member(jsii_name="addJobs")
    def add_jobs(self, jobs: typing.Mapping[builtins.str, typing.Any]) -> None:
        '''
        :param jobs: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addJobs", [jobs]))

    @jsii.member(jsii_name="on")
    def on(self, events: typing.Mapping[builtins.str, typing.Any]) -> None:
        '''
        :param events: -

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "on", [events]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="file")
    def file(self) -> _YamlFile_909731b0:
        '''
        :stability: experimental
        '''
        return typing.cast(_YamlFile_909731b0, jsii.get(self, "file"))


class Mergify(
    _Component_2b0ad27f,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.Mergify",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        github: GitHub,
        *,
        rules: typing.Optional[typing.List["MergifyRule"]] = None,
    ) -> None:
        '''
        :param github: -
        :param rules: 

        :stability: experimental
        '''
        options = MergifyOptions(rules=rules)

        jsii.create(Mergify, self, [github, options])

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        *,
        actions: typing.Mapping[builtins.str, typing.Any],
        conditions: typing.List[builtins.str],
        name: builtins.str,
    ) -> None:
        '''
        :param actions: 
        :param conditions: 
        :param name: 

        :stability: experimental
        '''
        rule = MergifyRule(actions=actions, conditions=conditions, name=name)

        return typing.cast(None, jsii.invoke(self, "addRule", [rule]))


@jsii.data_type(
    jsii_type="projen.github.MergifyOptions",
    jsii_struct_bases=[],
    name_mapping={"rules": "rules"},
)
class MergifyOptions:
    def __init__(
        self,
        *,
        rules: typing.Optional[typing.List["MergifyRule"]] = None,
    ) -> None:
        '''
        :param rules: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def rules(self) -> typing.Optional[typing.List["MergifyRule"]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List["MergifyRule"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MergifyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.github.MergifyRule",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "conditions": "conditions", "name": "name"},
)
class MergifyRule:
    def __init__(
        self,
        *,
        actions: typing.Mapping[builtins.str, typing.Any],
        conditions: typing.List[builtins.str],
        name: builtins.str,
    ) -> None:
        '''
        :param actions: 
        :param conditions: 
        :param name: 

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "actions": actions,
            "conditions": conditions,
            "name": name,
        }

    @builtins.property
    def actions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def conditions(self) -> typing.List[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MergifyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PullRequestTemplate(
    _TextFile_4a74808c,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen.github.PullRequestTemplate",
):
    '''(experimental) Template for GitHub pull requests.

    :stability: experimental
    '''

    def __init__(
        self,
        github: GitHub,
        *,
        lines: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''
        :param github: -
        :param lines: (experimental) The contents of the template. You can use ``addLine()`` to add additional lines. Default: - a standard default template will be created.

        :stability: experimental
        '''
        options = PullRequestTemplateOptions(lines=lines)

        jsii.create(PullRequestTemplate, self, [github, options])


@jsii.data_type(
    jsii_type="projen.github.PullRequestTemplateOptions",
    jsii_struct_bases=[],
    name_mapping={"lines": "lines"},
)
class PullRequestTemplateOptions:
    def __init__(
        self,
        *,
        lines: typing.Optional[typing.List[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for ``PullRequestTemplate``.

        :param lines: (experimental) The contents of the template. You can use ``addLine()`` to add additional lines. Default: - a standard default template will be created.

        :stability: experimental
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if lines is not None:
            self._values["lines"] = lines

    @builtins.property
    def lines(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The contents of the template.

        You can use ``addLine()`` to add additional lines.

        :default: - a standard default template will be created.

        :stability: experimental
        '''
        result = self._values.get("lines")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTemplateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.github.VersioningStrategy")
class VersioningStrategy(enum.Enum):
    '''(experimental) The strategy to use when edits manifest and lock files.

    :stability: experimental
    '''

    LOCKFILE_ONLY = "LOCKFILE_ONLY"
    '''(experimental) Only create pull requests to update lockfiles updates.

    Ignore any new
    versions that would require package manifest changes.

    :stability: experimental
    '''
    AUTO = "AUTO"
    '''(experimental) - For apps, the version requirements are increased.

    - For libraries, the range of versions is widened.

    :stability: experimental
    '''
    WIDEN = "WIDEN"
    '''(experimental) Relax the version requirement to include both the new and old version, when possible.

    :stability: experimental
    '''
    INCREASE = "INCREASE"
    '''(experimental) Always increase the version requirement to match the new version.

    :stability: experimental
    '''
    INCREASE_IF_NECESSARY = "INCREASE_IF_NECESSARY"
    '''(experimental) Increase the version requirement only when required by the new version.

    :stability: experimental
    '''


__all__ = [
    "AutoMerge",
    "AutoMergeOptions",
    "Dependabot",
    "DependabotIgnore",
    "DependabotOptions",
    "DependabotScheduleInterval",
    "GitHub",
    "GithubWorkflow",
    "Mergify",
    "MergifyOptions",
    "MergifyRule",
    "PullRequestTemplate",
    "PullRequestTemplateOptions",
    "VersioningStrategy",
]

publication.publish()
