#!/usr/bin/env bash
# Run locally: ./deploy_us_server.sh [--host us-server|96.9.225.9|100.80.6.84]
# --check validates local artifacts without SSH or starting a service.
# Uses existing root SSH keys/config only. No package installs, fees or prompts.
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
HOSTS=(us-server 96.9.225.9 100.80.6.84)
SSH_OPTIONS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=yes)
CHECK_ONLY=0
while (($#)); do
  case "$1" in
    --check) CHECK_ONLY=1; shift ;;
    --host)
      [[ $# -ge 2 ]] || { echo "--host requires an address" >&2; exit 2; }
      case "$2" in
        us-server|96.9.225.9|100.80.6.84) HOSTS=("$2") ;;
        *) echo "Use us-server or the specified US VPS public or Tailscale address." >&2; exit 2 ;;
      esac
      shift 2 ;;
    *) echo "Usage: $0 [--check] [--host us-server|96.9.225.9|100.80.6.84]" >&2; exit 2 ;;
  esac
done

for executable in python3 ssh rsync; do command -v "$executable" >/dev/null; done
test -x "$SCRIPT_DIR/sniper_daemon.py"
test -x "$SCRIPT_DIR/proxy-sniper.service"
python3 - "$SCRIPT_DIR/sniper_daemon.py" <<'PY'
import sys
with open(sys.argv[1], encoding="utf-8") as stream:
    compile(stream.read(), sys.argv[1], "exec")
print("Local Python syntax: PASS")
PY
python3 "$SCRIPT_DIR/sniper_daemon.py" --dry-run
if [[ "$CHECK_ONLY" == 1 ]]; then
  echo "Local deployment artifacts: PASS (no remote changes)"
  exit 0
fi

TARGET=""
for host in "${HOSTS[@]}"; do
  # Keep the alias intact so SSH uses its configured user, key and host identity.
  destination="$host"
  [[ "$host" == us-server ]] || destination="root@$host"
  if ssh "${SSH_OPTIONS[@]}" "$destination" 'command -v python3 >/dev/null && command -v rsync >/dev/null && command -v systemctl >/dev/null && test -x /usr/bin/python3'; then
    TARGET="$destination"
    break
  fi
done
[[ -n "$TARGET" ]] || { echo "Cannot reach the US VPS with existing root SSH access, or required server commands are missing." >&2; exit 1; }

ssh "${SSH_OPTIONS[@]}" "$TARGET" 'bash -se' <<'REMOTE'
id -u proxy-sniper >/dev/null 2>&1 || useradd --system --user-group --no-create-home --shell /usr/sbin/nologin proxy-sniper
install -d -m 0755 -o proxy-sniper -g proxy-sniper /opt/kais-proxy-sniper
# Preserve the actual previous installation and state before upgrading in place.
backup_dir="/opt/kais-proxy-sniper/backups/$(date -u +%Y%m%dT%H%M%SZ)"
install -d -m 0700 "$backup_dir"
for artifact in sniper_daemon.py proxy-sniper.service state.json matched_leads.jsonl; do
  if [[ -f "/opt/kais-proxy-sniper/$artifact" ]]; then
    cp -p "/opt/kais-proxy-sniper/$artifact" "$backup_dir/"
  fi
done
if [[ -f /etc/systemd/system/proxy-sniper.service ]]; then
  cp -p /etc/systemd/system/proxy-sniper.service "$backup_dir/installed.service"
fi
REMOTE

# Only code and service definition are transferred; preserve state and lead ledger.
rsync -az -e 'ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=yes' \
  "$SCRIPT_DIR/sniper_daemon.py" "$SCRIPT_DIR/proxy-sniper.service" "$TARGET:/opt/kais-proxy-sniper/"

ssh "${SSH_OPTIONS[@]}" "$TARGET" 'bash -se' <<'REMOTE'
cd /opt/kais-proxy-sniper
# Root-run rsync/deploy leaves root-owned files the daemon cannot append to.
chown -R proxy-sniper:proxy-sniper /opt/kais-proxy-sniper
/usr/bin/python3 -c 'from pathlib import Path; p = Path("sniper_daemon.py"); compile(p.read_text(), str(p), "exec")'
runuser -u proxy-sniper -- /usr/bin/python3 sniper_daemon.py --dry-run
install -m 0644 proxy-sniper.service /etc/systemd/system/proxy-sniper.service
systemd-analyze verify /etc/systemd/system/proxy-sniper.service
systemctl daemon-reload
systemctl enable proxy-sniper.service
systemctl restart proxy-sniper.service
# Require the process to remain active after startup, rather than only at fork.
sleep 3
systemctl is-active --quiet proxy-sniper.service
systemctl --no-pager --full status proxy-sniper.service
REMOTE
echo "Deployed to $TARGET. Read lead/error output with: journalctl -u proxy-sniper.service --no-pager"
