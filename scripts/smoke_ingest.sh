#!/usr/bin/env bash
set -euo pipefail
judgment-ingest status
judgment-ingest run --source fcl --limit 5 --dry-run
