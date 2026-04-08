# fact-check-v2

Local-first fact checking toolkit with:
- Gap analysis for provided facts versus article corpus
- Graded reporting with future-update signals
- Proposal-driven updates with individual and bulk apply modes
- Chunked multi-agent execution planning (8-10 files per block)
- Sandbox mode to restrict tool calls to allowlisted MCP tools + fact-checker
- Chat-style tool call tracing for test/audit visibility

## Quick start

```powershell
cd fact-check-v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## Team install (portable)

Use one of these options for teammates:

1. Editable development install:

```powershell
git clone <repo-url>
cd .github/fact-check-v2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

2. Isolated CLI install with pipx:

```powershell
pipx install .
```

3. CI-friendly non-editable install:

```powershell
pip install .
```

## Commands

```powershell
fact-check-v2 gap-analyze --facts .\examples\facts.json --articles .\examples\articles --source-root ..\copilot\skills\sources --trace .\out\tool_calls.jsonl
fact-check-v2 report --analysis .\out\analysis.json --output .\out\factcheck_report.md
fact-check-v2 propose-updates --analysis .\out\analysis.json --output .\out\proposals.json
fact-check-v2 apply-updates --proposals .\out\proposals.json --mode individual --id P-1
fact-check-v2 apply-updates --proposals .\out\proposals.json --mode bulk --min-risk low
fact-check-v2 batch-plan --articles .\examples\articles --chunk-size 10
fact-check-v2 batch-run --facts .\examples\facts.json --articles .\examples\articles --chunk-size 8 --workers 4 --source-root ..\copilot\skills\sources --trace .\out\tool_calls.jsonl
fact-check-v2 review-folder --facts .\examples\facts.json --articles .\examples\articles --analysis-output .\out\analysis_review.json --report-output .\out\factcheck_review.md --proposals-output .\out\proposals_review.json --source-root ..\copilot\skills\sources --trace .\out\tool_calls_review.jsonl
fact-check-v2 run-status --run-id <run-id>
fact-check-v2 proposal-decision --run-id <run-id> --proposal-id P-1 --decision accepted
fact-check-v2 review-transition --run-id <run-id> --action approve
fact-check-v2 apply-approved --run-id <run-id> --proposals .\out\proposals_review.json --min-risk medium
fact-check-v2 sandbox-test --trace .\out\tool_calls.jsonl
```

`review-folder` is approval-gated by default: it generates analysis, report, and proposals but does not apply updates.

## Testing in a walled-off environment

1. Use `sandbox-test` command to execute policy checks with strict allowlist.
2. Default policy allows:
   - `fact-checker`
   - Any tool name starting with `fact-checker.`
   - Any tool name starting with `mcp.`
3. Every tool call is emitted as JSON to stdout and written to the trace file.
4. Any disallowed tool call is blocked and logged with `status=blocked`.

## Test protocol starter

```powershell
cd fact-check-v2
python -m unittest discover -s tests -p "test_*.py"
```

For strict sandbox instructions, see `docs/WALLED_OFF_TESTING.md`.
