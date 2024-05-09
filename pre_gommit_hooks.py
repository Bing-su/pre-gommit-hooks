from __future__ import annotations

import asyncio
import os
from pathlib import Path
from urllib.parse import quote

import httpx
import yaml
from pydantic import BaseModel, Field
from returns.future import FutureResultE, future_safe
from returns.io import IOFailure, IOSuccess, impure_safe
from returns.pipeline import flow
from returns.result import Failure, ResultE, Success

YAML_FILE = ".pre-commit-hooks.yaml"
BASE_URL = "https://api.deps.dev/v3"


def _quote_url(url: str) -> str:
    return quote(url, safe="")


def _remove_version(package: str) -> str:
    pkg, _, _ = package.partition("@")
    return pkg


def _alias(package: str) -> str:
    match package:
        case "github.com/golangci/golangci-lint/cmd/golangci-lint":
            return "github.com/golangci/golangci-lint"
        case "golang.org/x/tools/cmd/goimports":
            return "golang.org/x/tools"
        case _:
            return package


def get_name(package: str) -> str:
    return flow(
        package,
        _remove_version,
        _alias,
        _quote_url,
    )


class VersionKey(BaseModel):
    system: str
    name: str
    version: str


class Version(BaseModel):
    version_key: VersionKey = Field(alias="versionKey")
    is_default: bool = Field(alias="isDefault")


class PackageKey(BaseModel):
    system: str
    name: str


class Package(BaseModel):
    package_key: PackageKey = Field(alias="packageKey")
    versions: list[Version]
    orig: str = ""


@future_safe
async def get_version(package: str, system: str = "go") -> Package:
    pkg = get_name(package)
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        resp = await client.get(f"/systems/{system}/packages/{pkg}")
        resp.raise_for_status()
        result = Package.model_validate_json(resp.content)
        result.orig = package
        return result


def latest_version(package: Package) -> ResultE[str]:
    versions = package.versions
    for version in versions:
        if version.is_default:
            latest = version.version_key.version
            pkg, _, _ = package.orig.partition("@")
            return Success(f"{pkg}@{latest}")

    msg = "No default version found"
    return Failure(RuntimeError(msg))


class Hook(BaseModel):
    id: str
    name: str
    entry: str
    types: list[str] = ["go"]
    language: str = "golang"
    additional_dependencies: list[str] = []
    description: str = ""


@impure_safe
def read_yaml(path: str | os.PathLike[str] = YAML_FILE) -> list[Hook]:
    with Path(path).open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return [Hook.model_validate(hook) for hook in data]


def update_deps(deps: list[str]) -> list[FutureResultE[str]]:
    return [get_version(dep).bind_result(latest_version) for dep in deps]


async def update_hook(hook: Hook) -> Hook:
    new = hook.model_copy()
    new_deps = await asyncio.gather(*update_deps(new.additional_dependencies))
    result = []

    for i, dep in enumerate(new_deps):
        match dep:
            case IOSuccess(Success(suc)):
                result.append(suc)
            case IOFailure(_):
                result.append(new.additional_dependencies[i])
            case _:
                msg = "Unreachable"
                raise RuntimeError(msg)

    new.additional_dependencies = result
    return new


async def update(hooks: list[Hook]) -> list[Hook]:
    tasks: list[asyncio.Task[Hook]] = []
    async with asyncio.TaskGroup() as tg:
        for old in hooks:
            task = tg.create_task(update_hook(old))
            tasks.append(task)

    return [task.result() for task in tasks]


def update_github_output(value: str):
    if "GITHUB_OUTPUT" not in os.environ:
        return
    path = Path(os.environ["GITHUB_OUTPUT"])
    with path.open("a", encoding="utf-8") as file:
        file.write(f"UPDATED={value}\n")


def is_updated(old: list[Hook], new: list[Hook]) -> bool:
    return any(o != n for o, n in zip(old, new, strict=True))


def main():
    io_hooks = read_yaml(YAML_FILE)
    match io_hooks:
        case IOSuccess(Success(suc)):
            hooks = suc
        case IOFailure(Failure(exc)):
            raise exc
        case _:
            msg = "Unreachable"
            raise RuntimeError(msg)

    updated = asyncio.run(update(hooks))
    data = [hook.model_dump() for hook in updated]

    with Path(YAML_FILE).open("w", encoding="utf-8") as file:
        yaml.dump(data, file, sort_keys=False)

    if is_updated(hooks, updated):
        update_github_output("true")
    else:
        update_github_output("false")


if __name__ == "__main__":
    main()
