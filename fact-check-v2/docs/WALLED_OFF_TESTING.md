# Walled-Off Testing Guide

This mode enforces that only allowlisted tools run during tests.

## Allowed tools policy

- exact: `fact-checker`
- prefix: `fact-checker.`
- prefix: `mcp.`

Any other tool call is blocked and logged.

## Run real analysis with trace output

```powershell
cd fact-check-v2
fact-check-v2 gap-analyze --facts .\examples\facts.json --articles .\examples\articles --source-root ..\copilot\skills\sources --trace .\out\tool_calls_gap.jsonl
fact-check-v2 batch-run --facts .\examples\facts.json --articles .\examples\articles --chunk-size 8 --workers 2 --source-root ..\copilot\skills\sources --trace .\out\tool_calls_batch.jsonl
```

Expected:
- Tool calls are printed to chat/stdout during execution.
- Trace files contain one JSON line per tool invocation.
- Calls use `fact-checker.*` or `mcp.*` namespaces in strict environments.

## Run sandbox verification

```powershell
cd fact-check-v2
fact-check-v2 sandbox-test --trace .\out\tool_calls.jsonl
echo $LASTEXITCODE
```

Expected:
- JSON event lines printed to chat/stdout for every call
- `status=ok` for allowlisted tools
- `status=blocked` for disallowed tools
- non-zero exit in strict mode when blocked calls are present

## Tool-call chat logging requirements

Every event must include:
- timestamp
- correlation_id
- tool_name
- args_summary
- status
- latency_ms
- message

## CI check pattern

Use strict mode and fail pipeline if:
- blocked calls are not present when expected in negative tests
- any event is missing required fields
- transcript event count does not match invocation count
