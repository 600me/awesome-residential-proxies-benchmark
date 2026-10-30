# 夜间 `dd-lan` (36核) 全网野生 CPS 同行逆向掘金报告
- **启动时间**: `2026-10-29T15:39:01.449227+00:00`
- **完成时间**: `2026-10-29T15:46:36.136118+00:00`
- **捕获外部同行寄生项目总数**: **58 个**（覆盖 `npmjs.com`、`huggingface.co/spaces`、`dev.to`、`github.com`）
- **识别出外部商业/联盟目标域名总数**: **90 个**

## 一、高频被同行寄生的商业/联盟域名 Top 40
| 排名 | 目标商业/短链域名 | 被寄生项目数 | 涉及寄生平台 | 野生返佣链接样本 | 同行项目样本 |
| :--- | :--- | :---: | :--- | :--- | :--- |
| 1 | `runcrate.ai` | 7 | dev.to | `https://www.runcrate.ai/?utm_source=devto&amp;utm_medium=post&amp` | https://dev.to/runcrate/text-embedding-throughput-per-dollar-bge-small-base-and-large-on-rtx-5090-l40s-rtx-a6000-and-nlg |
| 2 | `aicostbudget.com` | 2 | github.com, huggingface.co/spaces | `https://aicostbudget.com/en/model-switch-cost-calculator?utm_sour` | https://huggingface.co/spaces/aicostbudget-ai/llm-api-pricing-calculator |
| 3 | `kenwalger.com` | 2 | dev.to | `https://www.kenwalger.com/blog/software-engineering/tuesday-isnt-` | https://dev.to/kenwalger/four-ways-a-test-can-lie-to-you-2ibf |
| 4 | `russellsteadman.com` | 2 | npmjs.com | `https://www.russellsteadman.com/?utm_source=aff_repo&utm_medium=r` | https://www.npmjs.com/package/affiliate |
| 5 | `dash.capmonster.cloud` | 2 | npmjs.com | `https://docs.capmonster.cloud/docs/external-services/?utm_source=` | https://www.npmjs.com/package/@zennolab_com/capmonstercloud-client |
| 6 | `docs.capmonster.cloud` | 2 | npmjs.com | `https://docs.capmonster.cloud/docs/external-services/?utm_source=` | https://www.npmjs.com/package/@zennolab_com/capmonstercloud-client |
| 7 | `capmonster.cloud` | 2 | npmjs.com | `https://docs.capmonster.cloud/docs/external-services/?utm_source=` | https://www.npmjs.com/package/@zennolab_com/capmonstercloud-client |
| 8 | `bit.ly` | 2 | npmjs.com | `http://bit.ly/1xXZcKo` | https://www.npmjs.com/package/@infosimples/node_two_captcha |
| 9 | `outrank.so` | 2 | npmjs.com | `https://outrank.so/?via=next-seo` | https://www.npmjs.com/package/next-seo |
| 10 | `aiolaola.com` | 2 | npmjs.com | `https://aiolaola.com/?utm_source=github&utm_campaign=agents` | https://www.npmjs.com/package/agency-agents-zh |
| 11 | `schof.co` | 2 | npmjs.com | `https://schof.co/consulting/?utm_source=flexible-agency/react-nat` | https://www.npmjs.com/package/react-native-map-link |
| 12 | `registry.modelcontextprotocol.io` | 2 | github.com, npmjs.com | `https://registry.modelcontextprotocol.io/v0/servers?search=com.ma` | https://www.npmjs.com/package/@mambalabsdev/mcp-talent-agency-lookup |
| 13 | `bizon.solutions` | 2 | npmjs.com | `https://www.bizon.solutions?utm_source=github&utm_medium=readme&u` | https://www.npmjs.com/package/@sp-api-sdk/fba-inventory-api-v1 |
| 14 | `zenserp.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 15 | `geracodigo.com.br` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 16 | `ipstack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 17 | `monit.ly` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 18 | `hotstoks.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 19 | `api.postcodedata.nl` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 20 | `weatherstack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 21 | `currencylayer.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 22 | `exchangeratesapi.io` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 23 | `ipapi.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 24 | `aviationstack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 25 | `fixer.io` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 26 | `mailboxlayer.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 27 | `mercadopago.com.br` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 28 | `exchangerate.host` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 29 | `filestack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 30 | `marketstack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 31 | `mediastack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 32 | `screenshotlayer.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 33 | `cutt.ly` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 34 | `vatlayer.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 35 | `numverify.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 36 | `coinlayer.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 37 | `userstack.com` | 2 | github.com | `https://currencylayer.com?utm_source=Github&utm_medium=Referral&u` | https://github.com/public-apis/public-apis |
| 38 | `cloudgpu.app` | 1 | dev.to | `https://cloudgpu.app/pricing?utm_source=devto&amp;utm_medium=arti` | https://dev.to/cloudgpu_app/wan-22-a14b-at-720p-on-a-24-gb-gpu-why-it-runs-out-of-memory-and-what-to-change-8nc |
| 39 | `topicwire.online` | 1 | dev.to | `https://topicwire.online/will-profitable-niche-ideas-save-your-la` | https://dev.to/annabel/will-profitable-niche-ideas-save-your-language-blog-3p8b |
| 40 | `faceonlive-face-search-online.hf.space` | 1 | huggingface.co/spaces | `https://faceonlive.com/face-search-online/?utm_source=AFF12345678` | https://huggingface.co/spaces/Zhu-FaceOnLive/Face-Search-Affiliate |
