#!/usr/bin/env bash
# contract-lookup.sh — Cache an API Contract source (Tier 1-C) for reuse across fleet tracks
#
# Fetches the ARM/Bicep templates schema page and the Azure CLI `--help` for a given
# provider + property ONCE, so every track reconciling the same numeric/enum/default
# claim reads one cached lookup instead of re-fetching the contract per track.
#
# Usage:
#   ./contract-lookup.sh <provider-path> <property> [cache-dir]
#
# Example:
#   ./contract-lookup.sh microsoft.network/loadbalancers idleTimeoutInMinutes ./cache/
#
# Output (in cache-dir/):
#   contract_<provider-slug>_<property>_YYYYMMDD.json   metadata + resolved URLs
#   contract_<provider-slug>_<property>_YYYYMMDD.md     fetched templates schema page (markdown)
#   contract_<provider-slug>_<property>_YYYYMMDD.help   az <cmd> --help output (if az is available)
#
# Notes:
#   - Read-only. Fetches public learn.microsoft.com pages and local `az --help` only.
#   - Never creates or mutates Azure resources (that is Live Validation, Tier 4b).

set -euo pipefail

PROVIDER_PATH="${1:?Usage: $0 <provider-path> <property> [cache-dir]   e.g. microsoft.network/loadbalancers idleTimeoutInMinutes}"
PROPERTY="${2:?Missing <property>   e.g. idleTimeoutInMinutes}"
CACHE_DIR="${3:-./cache}"
DATE=$(date +%Y%m%d)
BUDGET=2000

mkdir -p "$CACHE_DIR"

PROVIDER_SLUG=$(echo "$PROVIDER_PATH" | tr '/' '-' | tr '[:upper:]' '[:lower:]')
BASENAME="contract_${PROVIDER_SLUG}_${PROPERTY}_${DATE}"

TEMPLATES_URL="https://learn.microsoft.com/azure/templates/${PROVIDER_PATH}"
CLI_GROUP=$(echo "$PROVIDER_PATH" | sed 's#^microsoft\.##; s#/# #')

echo "=== API Contract Lookup (Tier 1-C) ==="
echo "Provider:  $PROVIDER_PATH"
echo "Property:  $PROPERTY"
echo "Templates: $TEMPLATES_URL"
echo "Cache:     $CACHE_DIR"
echo ""

# 1. Fetch the ARM/Bicep templates schema page (markdown via Learn MCP-equivalent or curl).
#    Prefer the Learn CLI if present; fall back to curl with a markdown Accept header.
SCHEMA_FILE="${CACHE_DIR}/${BASENAME}.md"
if command -v learn >/dev/null 2>&1; then
  learn fetch "$TEMPLATES_URL" --max-tokens "$BUDGET" >"$SCHEMA_FILE" 2>/dev/null || true
fi
if [ ! -s "$SCHEMA_FILE" ] && command -v curl >/dev/null 2>&1; then
  curl -fsSL -H 'Accept: text/markdown, text/html' "$TEMPLATES_URL" >"$SCHEMA_FILE" 2>/dev/null || true
fi

# 2. Capture the Azure CLI parameter reference (accepted ranges/defaults) if az is installed.
HELP_FILE="${CACHE_DIR}/${BASENAME}.help"
if command -v az >/dev/null 2>&1; then
  # shellcheck disable=SC2086
  az $CLI_GROUP --help >"$HELP_FILE" 2>/dev/null || true
fi

# 3. Write a small metadata record so tracks can locate the cached artifacts.
META_FILE="${CACHE_DIR}/${BASENAME}.json"
cat >"$META_FILE" <<EOF
{
  "provider_path": "${PROVIDER_PATH}",
  "property": "${PROPERTY}",
  "date": "${DATE}",
  "contract_source": "${TEMPLATES_URL}",
  "schema_file": "${SCHEMA_FILE}",
  "cli_help_file": "${HELP_FILE}",
  "tier": "1-C"
}
EOF

echo "Wrote:"
echo "  $META_FILE"
[ -s "$SCHEMA_FILE" ] && echo "  $SCHEMA_FILE" || echo "  (schema page not cached — fetch it via microsoft_docs_fetch in-agent)"
[ -s "$HELP_FILE" ] && echo "  $HELP_FILE" || echo "  (az --help not captured — az CLI not available)"
echo ""
echo "Tracks should read contract_value from the schema page / CLI help and record contract_source=${TEMPLATES_URL}"
