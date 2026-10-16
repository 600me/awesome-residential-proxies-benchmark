#!/usr/bin/env bash
# Rebuild the static pages and extension ZIP, then deploy only these two sites.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
SSH_OPTIONS=(-o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes)
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/kais-proxy-domains.XXXXXX")"
REMOTE_STAGE=""
cleanup() {
  rm -rf -- "$STAGE"
  if [[ -n "$REMOTE_STAGE" ]]; then
    ssh "${SSH_OPTIONS[@]}" us-server "rm -rf -- '$REMOTE_STAGE'" || true
  fi
}
trap cleanup EXIT

python3 - "$STAGE" <<'PY'
from pathlib import Path
import html
import json
import sys
from urllib.parse import urlparse
import zipfile
from markdown_it import MarkdownIt

stage = Path(sys.argv[1])
md = MarkdownIt('commonmark', {'html': False}).enable('table')
style = '''body{font:17px/1.65 system-ui,sans-serif;margin:0;color:#17253b;background:#f4f7fb}
main{max-width:1100px;margin:auto;padding:40px 24px}a{color:#0758b8;overflow-wrap:anywhere}
h1,h2{line-height:1.25}table{border-collapse:collapse;display:block;overflow-x:auto;background:white}
th,td{padding:12px;border:1px solid #d5deeb;text-align:left}pre{overflow:auto;padding:18px;background:#e4ebf5}
code{overflow-wrap:anywhere}nav{padding-bottom:20px;border-bottom:1px solid #ccd8e8}li{margin:12px 0}'''
def page(title, content, lang):
    return ('<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>'+html.escape(title)+'</title><link rel="stylesheet" href="/style.css"></head>'
            '<body><main><nav><a href="/">Benchmark</a> · '
            '<a href="/privacy.html">Privacy policy</a></nav>'+content+'</main></body></html>\n')
listing = Path('extension/store-assets/STORE_LISTING.md').read_text()
policy = listing.split('## Privacy policy / disclosure\n', 1)[1].split('\n## ', 1)[0]
assert sum(line.startswith('- ') for line in policy.splitlines()) == 7
(stage/'index.html').write_text(page('Residential Proxy Benchmark', md.render(Path('README.md').read_text()), 'zh-CN'))
(stage/'privacy.html').write_text(page('Proxy Fraud Checker — Privacy policy', '<h1>Proxy Fraud Checker — Privacy policy</h1>'+md.render(policy), 'en'))
(stage/'style.css').write_text(style)

config = json.loads(Path('config/affiliates.yaml').read_text())
routes = []
for vendor in config['vendors']:
    short = urlparse(vendor['referral_url'])
    destination = vendor['destination_url']
    assert short.scheme == 'https' and short.netloc == 'go.272738.xyz'
    assert short.path in ['/smartproxy', '/brightdata', '/apify', '/oxylabs']
    assert urlparse(destination).scheme == 'https' and not any(c in destination for c in '\n\r"{};\\')
    routes.append('    location = '+short.path+' { return 301 "'+destination+'"; }')
static = '''    root /var/www/kais-proxy-benchmark;
    index index.html;
    charset utf-8;
    access_log off;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy no-referrer always;
    location / { try_files $uri $uri/ =404; }
'''
links = '\n'.join(routes)+'''
    access_log off;
    add_header Referrer-Policy no-referrer always;
    location = / { return 301 https://proxy.mybskm.top/; }
    location / { return 404; }
'''
for name, domain, body in [('kais-proxy-benchmark','proxy.mybskm.top',static), ('kais-proxy-links','go.272738.xyz',links)]:
    bootstrap = 'server {\n    listen 80;\n    server_name '+domain+';\n'+body+'}\n'
    (stage/(name+'-http')).write_text(bootstrap)
    tls = ('server {\n    listen 80;\n    server_name '+domain+';\n'
           '    location / { return 301 https://$host$request_uri; }\n}\n'
           'server {\n    listen 443 ssl http2;\n    server_name '+domain+';\n'
           '    ssl_certificate /etc/letsencrypt/live/'+domain+'/fullchain.pem;\n'
           '    ssl_certificate_key /etc/letsencrypt/live/'+domain+'/privkey.pem;\n'
           '    include /etc/letsencrypt/options-ssl-nginx.conf;\n'
           '    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;\n'+body+'}\n')
    (stage/name).write_text(tls)

extension = Path('extension')
with zipfile.ZipFile(extension/'proxy-fraud-checker.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in ['manifest.json', 'popup.html', 'popup.js', 'popup.css',
                 'icons/icon16.png', 'icons/icon48.png', 'icons/icon128.png',
                 'store-assets/STORE_LISTING.md']:
        archive.write(extension/name, name)
print('Generated benchmark, full privacy policy, four redirect routes and extension ZIP.')
PY

REMOTE_STAGE="$(ssh "${SSH_OPTIONS[@]}" us-server 'mktemp -d /tmp/kais-proxy-domains.XXXXXX')"
scp "${SSH_OPTIONS[@]}" "$STAGE/"* "us-server:$REMOTE_STAGE/"
ssh "${SSH_OPTIONS[@]}" us-server bash -se -- "$REMOTE_STAGE" <<'REMOTE'
stage="$1"
nginx -t
backup="/var/backups/kais-proxy-domains-$(date -u +%Y%m%dT%H%M%SZ)"
install -d -m 0700 "$backup"
tar -czf "$backup/nginx-before.tar.gz" -C /etc nginx
# Existing site and global configuration hashes must stay identical.
find /etc/nginx -type f ! -name kais-proxy-benchmark ! -name kais-proxy-links -exec sha256sum {} + > "$stage/existing-nginx.sha256"
systemctl show nginx kais-email-guard us-h2-node proxy-sniper -p Id -p MainPID -p ActiveEnterTimestamp -p NRestarts > "$stage/services-before"
install -d -m 0755 /var/www/kais-proxy-benchmark
install -m 0644 "$stage/index.html" "$stage/privacy.html" "$stage/style.css" /var/www/kais-proxy-benchmark/
for name in kais-proxy-benchmark kais-proxy-links; do
  if [[ ! -e "/etc/nginx/sites-available/$name" ]]; then
    install -m 0644 "$stage/$name-http" "/etc/nginx/sites-available/$name"
  fi
  ln -sfn "/etc/nginx/sites-available/$name" "/etc/nginx/sites-enabled/$name"
done
nginx -t
systemctl reload nginx
certbot --nginx -d proxy.mybskm.top --non-interactive --agree-tos -m 600megd@gmail.com --redirect --keep-until-expiring
certbot --nginx -d go.272738.xyz --non-interactive --agree-tos -m 600megd@gmail.com --redirect --keep-until-expiring
for name in kais-proxy-benchmark kais-proxy-links; do
  install -m 0644 "$stage/$name" "/etc/nginx/sites-available/$name"
done
nginx -t
systemctl reload nginx
sha256sum --check --quiet "$stage/existing-nginx.sha256"
systemctl show nginx kais-email-guard us-h2-node proxy-sniper -p Id -p MainPID -p ActiveEnterTimestamp -p NRestarts > "$stage/services-after"
diff -u "$stage/services-before" "$stage/services-after"
systemctl is-active nginx kais-email-guard us-h2-node proxy-sniper
for domain in proxy.mybskm.top go.272738.xyz; do
  openssl x509 -in "/etc/letsencrypt/live/$domain/fullchain.pem" -noout -subject -dates
done
echo "Deployment complete; existing configurations and service process identities unchanged. Backup: $backup"
REMOTE
