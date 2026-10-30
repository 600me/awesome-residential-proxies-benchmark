#!/usr/bin/env bash
trap '' HUP
set -u
WORKSPACE="/Users/a600/project-workspaces(项目工作区)/kais-proxy-cps-benchmark"
LOG_DIR="$WORKSPACE/logs"
MAIN_LOG="$LOG_DIR/night_pi_pipeline_20261029.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$MAIN_LOG"
}

run_with_timeout() {
    local timeout_sec="$1"
    shift
    perl -e '$SIG{HUP}="IGNORE"; alarm shift; exec @ARGV' "$timeout_sec" "$@"
}

cd "$WORKSPACE"
log "=== RESUMING STAGE 1 (GLM-5.3 Top 10 CPS Targets) & STAGE 3 (DS-v4.1 Audit) ==="

run_with_timeout 900 /usr/local/bin/pi --provider cc-switch-open-code-go --model glm-5.3-flash --tools read,write,edit,bash -p "$(cat /tmp/night_stage1_glm53_prompt.txt)" >> "$MAIN_LOG" 2>&1
log "[Stage 1] Finished with exit code $?"

run_with_timeout 600 /usr/local/bin/pi --provider cc-switch-open-code-go --model deepseek-v4.1-flash --tools read,write,bash -p "$(cat /tmp/night_stage3_ds41_audit_prompt.txt)" >> "$MAIN_LOG" 2>&1
log "[Stage 3] Finished with exit code $?"

log "=== STAGE 1 & STAGE 3 COMPLETED ==="
