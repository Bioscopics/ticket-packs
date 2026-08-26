#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["cursor-sdk>=0.1.9,<0.2"]
# ///
"""Operate Cursor SDK agents with JSON output suitable for Codex."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Mapping, Sequence
from enum import Enum
from pathlib import Path
from typing import Any

from cursor_sdk import (
    Agent,
    CloudAgentOptions,
    CloudEnvironment,
    CloudRepository,
    Cursor,
    CursorAgentError,
    LocalAgentOptions,
)


class UsageError(Exception):
    """A user-correctable CLI error."""


def plain(value: Any) -> Any:
    """Convert SDK objects into JSON-safe values without private fields."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return plain(value.value)
    if isinstance(value, Path):
        return str(value)
    if dataclasses.is_dataclass(value):
        return {
            field.name: plain(getattr(value, field.name))
            for field in dataclasses.fields(value)
            if not field.name.startswith("_")
        }
    if isinstance(value, Mapping):
        return {str(key): plain(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [plain(item) for item in value]
    to_dict = getattr(value, "to_dict", None)
    if callable(to_dict):
        return plain(to_dict())
    to_json = getattr(value, "to_json", None)
    if callable(to_json):
        return plain(to_json())
    return str(value)


def emit(value: Any, *, pretty: bool = False, stream: Any = sys.stdout) -> None:
    json.dump(
        plain(value),
        stream,
        indent=2 if pretty else None,
        sort_keys=pretty,
        ensure_ascii=False,
    )
    stream.write("\n")
    stream.flush()


def require_api_key(env_name: str) -> str:
    key = os.environ.get(env_name, "").strip()
    if not key:
        raise UsageError(
            f"Missing Cursor API key in {env_name}. Create one in Cursor Dashboard "
            "-> Integrations and export it without printing it."
        )
    # The SDK's default bridge reads CURSOR_API_KEY.
    os.environ["CURSOR_API_KEY"] = key
    return key


def change_workspace(raw_path: str | None) -> Path:
    path = Path(raw_path or os.getcwd()).expanduser().resolve()
    if not path.is_dir():
        raise UsageError(f"Workspace is not a directory: {path}")
    os.chdir(path)
    return path


def normalize_model_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def filter_models(models: list[Any], query: str | None) -> list[Any]:
    if not query:
        return models
    needle = normalize_model_name(query)
    return [
        model
        for model in models
        if needle in normalize_model_name(model.id)
        or needle in normalize_model_name(model.display_name)
    ]


def resolve_model(query: str, api_key: str) -> Any:
    models = list(Cursor.models.list(api_key=api_key))
    query_folded = query.casefold()
    exact_id = [model for model in models if model.id.casefold() == query_folded]
    if len(exact_id) == 1:
        return exact_id[0]

    normalized = normalize_model_name(query)
    exact_name = [
        model
        for model in models
        if normalize_model_name(model.display_name) == normalized
        or normalize_model_name(model.id) == normalized
    ]
    if len(exact_name) == 1:
        return exact_name[0]

    partial = filter_models(models, query)
    if len(partial) == 1:
        return partial[0]
    if partial:
        choices = ", ".join(f"{model.display_name} ({model.id})" for model in partial)
        raise UsageError(f"Model query {query!r} is ambiguous. Candidates: {choices}")

    available = ", ".join(
        f"{model.display_name} ({model.id})" for model in models[:25]
    )
    raise UsageError(
        f"Model {query!r} is not available to this Cursor account. "
        f"Available models include: {available or 'none returned'}"
    )


def parse_model_params(raw_values: list[str], model: Any) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw in raw_values:
        if "=" not in raw:
            raise UsageError(f"Model parameter must use ID=VALUE: {raw!r}")
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise UsageError(f"Model parameter must use non-empty ID=VALUE: {raw!r}")
        parsed[key] = value

    definitions = {definition.id: definition for definition in model.parameters}
    for key, value in parsed.items():
        if key not in definitions:
            raise UsageError(
                f"Model {model.id!r} has no parameter {key!r}. "
                f"Valid parameters: {', '.join(definitions) or 'none'}"
            )
        allowed = {item.value for item in definitions[key].values}
        if allowed and value not in allowed:
            raise UsageError(
                f"Invalid value {value!r} for {key!r}. "
                f"Valid values: {', '.join(sorted(allowed))}"
            )
    return parsed


def model_selection(model: Any, raw_params: list[str]) -> str | dict[str, Any]:
    params = parse_model_params(raw_params, model)
    if not params:
        return model.id
    return {
        "id": model.id,
        "params": [{"id": key, "value": value} for key, value in params.items()],
    }


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt is not None:
        prompt = args.prompt
    elif args.prompt_file is not None:
        path = Path(args.prompt_file).expanduser().resolve()
        if not path.is_file():
            raise UsageError(f"Prompt file does not exist: {path}")
        prompt = path.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        prompt = sys.stdin.read()
    else:
        raise UsageError("Provide --prompt, --prompt-file, or prompt text on stdin.")
    if not prompt.strip():
        raise UsageError("Prompt cannot be empty.")
    return prompt


def git_value(*args: str) -> str | None:
    result = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and value else None


def resolve_cloud_repositories(args: argparse.Namespace) -> list[Any]:
    urls = list(args.repo or [])
    if not urls:
        origin = git_value("config", "--get", "remote.origin.url")
        if origin:
            urls.append(origin)
    if not urls:
        raise UsageError(
            "Cloud runtime requires --repo URL or a git checkout with remote.origin.url."
        )
    ref = args.ref or git_value("branch", "--show-current")
    return [CloudRepository(url=url, starting_ref=ref or None) for url in urls]


def run_payload(run: Any) -> dict[str, Any]:
    return {
        "run_id": getattr(run, "id", ""),
        "agent_id": getattr(run, "agent_id", ""),
        "status": getattr(run, "status", ""),
        "result": getattr(run, "result", ""),
        "model": plain(getattr(run, "model", None)),
        "duration_ms": getattr(run, "duration_ms", 0),
        "git": plain(getattr(run, "git", None)),
        "created_at": getattr(run, "created_at", None),
        "usage": plain(getattr(run, "usage", None)),
    }


def finish_run(run: Any, *, stream_text: bool) -> dict[str, Any]:
    if stream_text:
        for chunk in run.iter_text():
            print(chunk, end="", file=sys.stderr, flush=True)
        print(file=sys.stderr, flush=True)
    result = run.wait()
    return {
        "run": run_payload(run),
        "terminal_result": plain(result),
    }


def prompt_summary(prompt: str) -> dict[str, Any]:
    return {
        "characters": len(prompt),
        "sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
    }


def command_models(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    models = list(Cursor.models.list(api_key=api_key))
    matches = filter_models(models, args.filter)
    return {"count": len(matches), "models": matches}


def command_start(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    workspace = change_workspace(args.cwd)
    prompt = read_prompt(args)
    model = resolve_model(args.model, api_key)
    selection = model_selection(model, args.model_param)

    local_options = None
    cloud_options = None
    config: dict[str, Any] = {
        "runtime": args.runtime,
        "model": plain(selection),
        "resolved_model": {"id": model.id, "display_name": model.display_name},
        "name": args.name,
        "workspace": str(workspace),
        "prompt": prompt_summary(prompt),
    }
    if args.runtime == "local":
        local_options = LocalAgentOptions(cwd=str(workspace))
        config["local"] = plain(local_options)
    else:
        repositories = resolve_cloud_repositories(args)
        environment = CloudEnvironment(type="cloud", name=args.cloud_environment)
        cloud_options = CloudAgentOptions(
            env=environment,
            repos=repositories,
            work_on_current_branch=args.work_on_current_branch or None,
            auto_create_pr=args.auto_create_pr or None,
            skip_reviewer_request=args.skip_reviewer_request or None,
        )
        config["cloud"] = plain(cloud_options)

    if args.dry_run:
        return {"dry_run": True, "configuration": config}

    agent = Agent.create(
        model=selection,
        api_key=api_key,
        name=args.name,
        local=local_options,
        cloud=cloud_options,
    )
    run = agent.send(prompt)
    if args.detach:
        return {
            "detached": True,
            "agent_id": agent.agent_id,
            "run": run_payload(run),
        }
    return {"agent_id": agent.agent_id, **finish_run(run, stream_text=args.stream)}


def command_send(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    change_workspace(args.cwd)
    prompt = read_prompt(args)
    options: dict[str, Any] = {}
    if args.model:
        model = resolve_model(args.model, api_key)
        options["model"] = model_selection(model, args.model_param)
    elif args.model_param:
        raise UsageError("--model-param requires --model on a follow-up.")

    agent = Agent.resume(args.agent_id, {"apiKey": api_key})
    run = agent.send(prompt, options or None)
    if args.detach:
        return {
            "detached": True,
            "agent_id": agent.agent_id,
            "run": run_payload(run),
        }
    return {"agent_id": agent.agent_id, **finish_run(run, stream_text=args.stream)}


def command_status(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    change_workspace(args.cwd)
    run = Agent.get_run(args.run_id, {"apiKey": api_key})
    if args.wait:
        return finish_run(run, stream_text=args.stream)
    return {"run": run_payload(run)}


def command_agents(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    workspace = change_workspace(args.cwd)
    options: dict[str, Any] = {
        "apiKey": api_key,
        "limit": args.limit,
        "includeArchived": args.include_archived,
    }
    if args.runtime:
        options["runtime"] = args.runtime
    if args.runtime == "local" or args.cwd:
        options["cwd"] = str(workspace)
    page = Agent.list(options)
    return {
        "items": list(page.items),
        "next_cursor": page.next_cursor,
    }


def command_runs(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    workspace = change_workspace(args.cwd)
    options: dict[str, Any] = {"apiKey": api_key, "limit": args.limit}
    if args.runtime:
        options["runtime"] = args.runtime
    cwd_filter = str(workspace) if args.runtime == "local" else None
    page = Agent.list_runs(args.agent_id, options, cwd=cwd_filter)
    return {
        "items": [run_payload(run) for run in page.items],
        "next_cursor": page.next_cursor,
    }


def command_messages(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    change_workspace(args.cwd)
    agent = Agent.resume(args.agent_id, {"apiKey": api_key})
    return {"agent_id": agent.agent_id, "messages": agent.list_messages()}


def command_cancel(args: argparse.Namespace, api_key: str) -> dict[str, Any]:
    change_workspace(args.cwd)
    # The default SDK bridge reads the key from CURSOR_API_KEY.
    Agent.cancel_run(args.run_id, agent_id=args.agent_id)
    return {"cancelled": True, "run_id": args.run_id, "agent_id": args.agent_id}


def add_prompt_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--prompt", help="Prompt text; prefer --prompt-file for multiline text")
    group.add_argument("--prompt-file", help="UTF-8 file containing the prompt")


def add_execution_arguments(parser: argparse.ArgumentParser) -> None:
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--detach", action="store_true", help="Return after starting the run")
    mode.add_argument("--stream", action="store_true", help="Stream assistant text to stderr")


def add_workspace_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--cwd", help="Workspace directory; defaults to the current directory")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Launch and manage Cursor SDK agents with JSON output."
    )
    parser.add_argument(
        "--api-key-env",
        default="CURSOR_API_KEY",
        help="Environment variable containing the Cursor API key",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    subparsers = parser.add_subparsers(dest="command", required=True)

    models = subparsers.add_parser("models", help="List models available to the account")
    models.add_argument("--filter", help="Filter by model ID or display name")
    models.set_defaults(handler=command_models)

    start = subparsers.add_parser("start", help="Create an agent and start its first run")
    start.add_argument("--runtime", required=True, choices=("local", "cloud"))
    start.add_argument("--model", required=True, help="Exact ID or unambiguous model name")
    start.add_argument("--model-param", action="append", default=[], metavar="ID=VALUE")
    start.add_argument("--name", help="Optional agent name")
    add_workspace_argument(start)
    add_prompt_arguments(start)
    add_execution_arguments(start)
    start.add_argument("--dry-run", action="store_true", help="Validate without launching")
    start.add_argument("--repo", action="append", help="Cloud repository URL; repeatable")
    start.add_argument("--ref", help="Starting branch, tag, or commit for cloud repositories")
    start.add_argument("--cloud-environment", help="Named Cursor cloud environment")
    start.add_argument("--work-on-current-branch", action="store_true")
    start.add_argument("--auto-create-pr", action="store_true")
    start.add_argument("--skip-reviewer-request", action="store_true")
    start.set_defaults(handler=command_start)

    send = subparsers.add_parser("send", help="Send a follow-up prompt to an agent")
    send.add_argument("--agent-id", required=True)
    send.add_argument("--model", help="Optional model override")
    send.add_argument("--model-param", action="append", default=[], metavar="ID=VALUE")
    add_workspace_argument(send)
    add_prompt_arguments(send)
    add_execution_arguments(send)
    send.set_defaults(handler=command_send)

    status = subparsers.add_parser("status", help="Inspect or wait for a run")
    status.add_argument("--run-id", required=True)
    status.add_argument("--wait", action="store_true")
    status.add_argument("--stream", action="store_true", help="Stream assistant text while waiting")
    add_workspace_argument(status)
    status.set_defaults(handler=command_status)

    agents = subparsers.add_parser("agents", help="List Cursor agents")
    agents.add_argument("--runtime", choices=("local", "cloud"))
    agents.add_argument("--include-archived", action="store_true")
    agents.add_argument("--limit", type=int, default=100)
    add_workspace_argument(agents)
    agents.set_defaults(handler=command_agents)

    runs = subparsers.add_parser("runs", help="List runs for an agent")
    runs.add_argument("--agent-id", required=True)
    runs.add_argument("--runtime", choices=("local", "cloud"))
    runs.add_argument("--limit", type=int, default=100)
    add_workspace_argument(runs)
    runs.set_defaults(handler=command_runs)

    messages = subparsers.add_parser("messages", help="List messages for an agent")
    messages.add_argument("--agent-id", required=True)
    add_workspace_argument(messages)
    messages.set_defaults(handler=command_messages)

    cancel = subparsers.add_parser("cancel", help="Cancel a running agent run")
    cancel.add_argument("--run-id", required=True)
    cancel.add_argument("--agent-id")
    add_workspace_argument(cancel)
    cancel.set_defaults(handler=command_cancel)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        api_key = require_api_key(args.api_key_env)
        result = args.handler(args, api_key)
        emit(result, pretty=args.pretty)
        return 0
    except UsageError as error:
        emit(
            {"error": {"type": "usage_error", "message": str(error)}},
            pretty=getattr(args, "pretty", False),
            stream=sys.stderr,
        )
        return 2
    except CursorAgentError as error:
        emit(
            {
                "error": {
                    "type": error.__class__.__name__,
                    "message": error.message,
                    "code": error.code,
                    "status": error.status,
                    "retryable": error.is_retryable,
                    "request_id": error.request_id,
                    "retry_after": error.retry_after,
                }
            },
            pretty=getattr(args, "pretty", False),
            stream=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        emit(
            {"error": {"type": "interrupted", "message": "Interrupted"}},
            stream=sys.stderr,
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
