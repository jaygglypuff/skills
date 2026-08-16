#!/usr/bin/env bash
# Package the skill as humanize.skill, ready to upload to Claude.
set -euo pipefail

cd "$(dirname "$0")"
OUT="humanize.skill"

echo "Running tests first..."
python3 tests/test_ai_tells.py 2>&1 | tail -3

echo
echo "Packaging..."
rm -f "$OUT"
zip -q -r "$OUT" humanize \
  -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' '*/tells.json'

echo "Built $OUT"
unzip -l "$OUT" | sed -n '4,20p'
