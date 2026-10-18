#!/usr/bin/env bash
# Daily GitHub issue outreach for kais-proxy-sniper.
# Installed as /opt/kais-proxy-sniper/run_daily_outreach.sh and owned by
# proxy-sniper. Cron invokes it once per day; no secrets are printed.
set -euo pipefail
umask 077

APP_DIR="/opt/kais-proxy-sniper"
PYTHON="/usr/bin/python3"
LIMIT=3

for env_file in "$APP_DIR/github-token.env" "$APP_DIR/deepseek.env"; do
  if [[ ! -r "$env_file" ]]; then
    echo "missing or unreadable credential file: $env_file" >&2
    exit 1
  fi
done

# Load credentials into the environment only; never echo their values.
set -a
# shellcheck disable=SC1091
. "$APP_DIR/github-token.env"
# shellcheck disable=SC1091
. "$APP_DIR/deepseek.env"
set +a

# The directive pins the permanent alias deepseek-chat. The credential file may
# carry a historical explicit model lock, so the daily job sets the required
# alias unless DAILY_DEEPSEEK_MODEL is deliberately provided.
export DEEPSEEK_MODEL="${DAILY_DEEPSEEK_MODEL:-deepseek-chat}"

mkdir -p "$APP_DIR/logs"
cd "$APP_DIR"
exec "$PYTHON" gh-answer.py --once --post --limit "$LIMIT"
