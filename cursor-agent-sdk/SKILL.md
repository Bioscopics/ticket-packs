---
name: cursor-agent-sdk
description: Launch, inspect, and interact with Cursor SDK coding agents from Codex using Cursor-supported models and local or cloud runtimes. Use when the user asks Codex to delegate a coding task to a Cursor agent, run a Cursor agent with Gemini, Grok, Claude, Composer, or another model exposed by Cursor, send follow-up instructions, monitor or cancel a Cursor run, or list Cursor agents and available models.
---

# Cursor Agent SDK

Use the bundled Python CLI to operate Cursor agents. It resolves model names against the user's live Cursor model catalog, so never guess or hard-code a model ID.

This skill launches a Cursor coding agent that uses the selected model inside Cursor's agent harness. It is not a raw Gemini, Grok, or other provider chat API.

## Prerequisites

- Require `uv` and a Cursor API key in `CURSOR_API_KEY`.
- Direct the user to Cursor Dashboard -> Integrations when the key is missing.
- Never print the key, put it in a prompt, or pass it as a command-line value. To use another environment variable, pass its name with the global `--api-key-env` option.

Set the CLI path once:

```bash
CURSOR_AGENTS="${CODEX_HOME:-$HOME/.codex}/skills/cursor-agent-sdk/scripts/cursor_agents.py"
```

## Workflow

1. Establish the requested task, runtime, repository or local directory, and whether the run should be detached. Do not launch more agents than requested.
2. Discover models before every launch:

   ```bash
   "$CURSOR_AGENTS" models --filter gemini
   "$CURSOR_AGENTS" models --filter grok
   ```

3. Use the exact returned model ID. If the requested model is unavailable or ambiguous, report the candidates and ask the user to choose; never silently substitute a different model.
4. Prefer cloud runtime for isolated, asynchronous delegation. Prefer local runtime only when the user wants the agent to work directly in a local checkout. Confirm the target directory before a local launch.
5. Prefer `--prompt-file` for multiline or untrusted prompt text. Never interpolate untrusted text into a shell command.
6. Use `--detach` for an asynchronous run and return both `agent_id` and `run_id`. Without it, wait for the terminal result. Add `--stream` to mirror assistant text to stderr while keeping the final JSON on stdout.
7. Inspect the terminal result and relevant repository changes before treating delegated work as complete.

## Launch Agents

Launch in a local checkout:

```bash
"$CURSOR_AGENTS" start \
  --runtime local \
  --cwd /absolute/path/to/repo \
  --model MODEL_ID \
  --prompt-file /absolute/path/to/prompt.md \
  --stream
```

Launch in Cursor's cloud and return immediately:

```bash
"$CURSOR_AGENTS" start \
  --runtime cloud \
  --cwd /absolute/path/to/local/checkout \
  --model MODEL_ID \
  --prompt-file /absolute/path/to/prompt.md \
  --detach
```

For cloud runs, `--cwd` is used to infer the `origin` URL and current branch. Supply `--repo URL` and optional `--ref REF` explicitly when inference is unsuitable. `--auto-create-pr` authorizes the agent to open a PR; omit it unless requested.

Use `--model-param ID=VALUE` for a model parameter returned by `models`. Use `start --dry-run` to validate the resolved model and launch configuration without creating an agent.

## Interact and Monitor

Send a follow-up:

```bash
"$CURSOR_AGENTS" send \
  --agent-id AGENT_ID \
  --prompt-file /absolute/path/to/follow-up.md \
  --detach
```

Inspect or wait for a run:

```bash
"$CURSOR_AGENTS" status --run-id RUN_ID
"$CURSOR_AGENTS" status --run-id RUN_ID --wait
```

List state or cancel a run:

```bash
"$CURSOR_AGENTS" agents
"$CURSOR_AGENTS" runs --agent-id AGENT_ID
"$CURSOR_AGENTS" messages --agent-id AGENT_ID
"$CURSOR_AGENTS" cancel --run-id RUN_ID --agent-id AGENT_ID
```

Run follow-up, status, and local-list commands from the same workspace used to create a local agent, or provide their `--cwd` option.

## Guardrails

- Treat every launch as cost-incurring and state-changing.
- Do not expose credentials or sensitive environment values to an agent.
- Local agents can edit files and execute commands in the target checkout. Preserve user changes and inspect the diff afterward.
- Cloud agents can push branches or open PRs when configured. Do not enable `--work-on-current-branch` or `--auto-create-pr` without user authorization.
- A successful SDK request only means the run started. Completion requires a terminal run status plus review of the result and artifacts.
