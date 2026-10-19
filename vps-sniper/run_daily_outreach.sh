#!/usr/bin/env bash
# Daily GitHub issue outreach for kais-proxy-sniper.
#
# Installed as /opt/kais-proxy-sniper/run_daily_outreach.sh, owned by
# proxy-sniper, mode 0755. Cron invokes it once per day; no secrets are printed.
#
# Flow:
#   1. Pre-flight anonymous shadowban check. Exit 2 from `--check-shadowban`
#      means a recent comment is not publicly visible -> circuit break, no post.
#   2. Post the daily comments with the permanent deepseek-chat alias.
#   3. Post-run attribution snapshot: real external human 302 clicks by `src`.
#
# Verification runs: DAILY_OUTREACH_SKIP_POST=1 exercises steps 1 and 3 without
# posting anything.
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
LOG_DIR="$APP_DIR/logs"
ALERT_LOG="$LOG_DIR/shadowban_alert.log"
SHADOWBAN_REPORT="$LOG_DIR/shadowban_check_latest.json"
export SHADOWBAN_REPORT

cd "$APP_DIR"

# 1. Anonymous shadowban self-check (no token, logged-out visitor view).
#    2 = hidden comment -> circuit breaker. 0 = all visible. 1 = inconclusive
#    (anonymous rate limit / network): proceed, because it is not evidence of a ban.
shadowban_rc=0
"$PYTHON" gh-answer.py --check-shadowban >"$SHADOWBAN_REPORT" 2>>"$LOG_DIR/shadowban_check.err" || shadowban_rc=$?
if [[ "$shadowban_rc" -eq 2 ]]; then
  printf '%s CIRCUIT_BREAK shadowban detected: recent comment(s) not publicly visible; daily posting skipped\n' \
    "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >>"$ALERT_LOG"
  echo "circuit breaker: recent GitHub comments are not publicly visible; nothing posted" >&2
  exit 2
fi
echo "shadowban pre-check rc=$shadowban_rc (0=visible, 1=inconclusive-for-network); proceeding"

# 2. Daily posting.
post_rc=0
if [[ "${DAILY_OUTREACH_SKIP_POST:-0}" == "1" ]]; then
  echo "verification run: DAILY_OUTREACH_SKIP_POST=1, no comments posted"
else
  "$PYTHON" gh-answer.py --once --post --limit "$LIMIT" || post_rc=$?
fi

# 3. Post-run attribution snapshot. traffic_audit.py writes
#    traffic_audit_report.json and prints a one-line funnel summary JSON.
audit_rc=0
"$PYTHON" traffic_audit.py 2>&1 | tee -a "$LOG_DIR/traffic_audit.log" || audit_rc=$?

if [[ "$post_rc" -ne 0 ]]; then
  echo "posting exited with $post_rc" >&2
  exit "$post_rc"
fi
if [[ "$audit_rc" -ne 0 ]]; then
  echo "traffic_audit.py exited with $audit_rc" >&2
  exit "$audit_rc"
fi
exit 0
