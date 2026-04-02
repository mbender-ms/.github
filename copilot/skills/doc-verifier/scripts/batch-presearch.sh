#!/usr/bin/env bash
# batch-presearch.sh — Pre-search claims against Microsoft Learn before agent verification
#
# Uses @microsoft/learn-cli to bulk-search claim keywords and cache results as JSON.
# Agents read the cache instead of making live MCP calls for every claim.
#
# Usage:
#   ./batch-presearch.sh claims_manifest.md [output_dir]
#
# Prerequisites:
#   npm install -g @microsoft/learn-cli
#
# Input: A claim manifest file (from claim-manifest.prompt.md) with lines like:
#   | C001 | 23 | feature | "Health probes support HTTP, HTTPS, and TCP" | — |
#
# Output: One JSON file per service area group in output_dir/
#   search_azure-load-balancer_YYYYMMDD.json
#   search_azure-virtual-network_YYYYMMDD.json

set -euo pipefail

MANIFEST="${1:?Usage: $0 <claims_manifest.md> [output_dir]}"
OUTPUT_DIR="${2:-./presearch_cache}"
DATE=$(date +%Y%m%d)
BUDGET=2000

mkdir -p "$OUTPUT_DIR"

echo "=== Microsoft Learn Pre-Search ==="
echo "Manifest: $MANIFEST"
echo "Output:   $OUTPUT_DIR"
echo ""

# Extract unique service areas from the manifest
# Looks for H3 headers like: ### Azure Load Balancer (8 claims)
SERVICE_AREAS=$(grep -E '^### ' "$MANIFEST" | sed 's/### //' | sed 's/ ([0-9]* claims)//' | sed 's/ /-/g' | tr '[:upper:]' '[:lower:]')

if [ -z "$SERVICE_AREAS" ]; then
  echo "ERROR: No service area groups found in manifest."
  echo "Expected H3 headers like: ### Azure Load Balancer (8 claims)"
  exit 1
fi

# Extract claim text from table rows (column 4 in the claims table)
# Format: | C001 | 23 | feature | "Health probes support HTTP, HTTPS, and TCP" | — |
extract_claims_for_area() {
  local area_header="$1"
  # Find the section, then extract claim text from table rows until next H3 or EOF
  awk -v header="$area_header" '
    $0 ~ "^### " header { found=1; next }
    found && /^### / { found=0 }
    found && /^\| C[0-9]/ {
      # Extract 4th column (claim text), strip quotes and pipes
      split($0, cols, "|")
      gsub(/^[[:space:]]*"|"[[:space:]]*$/, "", cols[5])
      if (cols[5] != "" && cols[5] != "—") print cols[5]
    }
  ' "$MANIFEST"
}

# Deduplicate search terms: extract key nouns from claims
# Keeps queries short (1-6 words) for best Learn MCP results
build_search_queries() {
  local claims="$1"
  echo "$claims" | while IFS= read -r claim; do
    # Strip common filler, keep service-specific terms
    echo "$claim" | \
      sed 's/["""]//g' | \
      sed 's/supports\|enables\|allows\|requires\|provides\|configures//gi' | \
      tr -s ' ' | \
      head -c 80
  done | sort -u | head -20  # Max 20 queries per service area
}

TOTAL_QUERIES=0
TOTAL_RESULTS=0

for area in $SERVICE_AREAS; do
  # Convert slug back to readable header for matching
  readable=$(echo "$area" | sed 's/-/ /g')

  echo "--- Searching: $readable ---"

  OUTPUT_FILE="$OUTPUT_DIR/search_${area}_${DATE}.json"

  # Build query list from claims in this area
  claims=$(extract_claims_for_area "$readable")
  queries=$(build_search_queries "$claims")

  if [ -z "$queries" ]; then
    echo "  No claims found for this area, skipping."
    continue
  fi

  # Initialize the output JSON array
  echo '{"service_area": "'"$readable"'", "date": "'"$DATE"'", "results": [' > "$OUTPUT_FILE"

  FIRST=true
  query_count=0

  while IFS= read -r query; do
    [ -z "$query" ] && continue

    # Add comma separator between results
    if [ "$FIRST" = true ]; then
      FIRST=false
    else
      echo "," >> "$OUTPUT_FILE"
    fi

    echo "  Querying: $query"

    # Run the search and capture JSON output
    # --json flag returns structured results
    result=$(npx -y @microsoft/learn-cli search "$query" --json 2>/dev/null || echo '{"error": "search failed", "query": "'"$query"'"}')

    echo '  {"query": "'"$query"'", "response": '"$result"'}' >> "$OUTPUT_FILE"

    query_count=$((query_count + 1))
    TOTAL_QUERIES=$((TOTAL_QUERIES + 1))

    # Rate limit: 500ms between queries to be polite
    sleep 0.5

  done <<< "$queries"

  echo ']}'  >> "$OUTPUT_FILE"

  result_count=$(grep -c '"title"' "$OUTPUT_FILE" 2>/dev/null || echo 0)
  TOTAL_RESULTS=$((TOTAL_RESULTS + result_count))

  echo "  Saved: $OUTPUT_FILE ($query_count queries, ~$result_count results)"
  echo ""
done

echo "=== Pre-search complete ==="
echo "Total queries:  $TOTAL_QUERIES"
echo "Total results:  ~$TOTAL_RESULTS"
echo "Cache dir:      $OUTPUT_DIR"
echo ""
echo "Next steps:"
echo "  1. Review the cache files for relevance"
echo "  2. Run fan-out-verify or fleet-batch-verify"
echo "     Agents can read these cache files instead of making live MCP calls"
echo "     for initial search — use docs_fetch only for pages that need full content"
