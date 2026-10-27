#!/usr/local/bin/python3
import datetime,json
from pathlib import Path
P=Path(__file__).parent/'untapped_high_commission_brands(未占坑高佣品牌蓝海池).json'
FACTS={
'ScraperAPI':('50% recurring; 每客户累计上限 $3000；优惠站须人工批准且费率单独通知','https://www.scraperapi.com/affiliates/','https://www.scraperapi.com/affiliate-terms/'),
'Decodo (Smartproxy)':('最高50%；每新客户最高$2500','https://decodo.com/proxy-affiliate-program'),
'Firstbase':('公开页10%；另有$40示例，实际协议待核实','https://www.firstbase.io/referral-partner-program'),
'RunPod':('普通推荐Pods 3% / Serverless 5%，6个月且为余额；高级联盟10%现金须资格达标','https://www.runpod.io/referral-and-affiliate-program'),
'ZenRows':('自助35%持续12个月；销售协助15%首年；Featured 40%须达标','https://www.zenrows.com/legal/partner-terms'),
'ScrapingBee':('25% recurring；每客户每月上限$62.25','https://www.scrapingbee.com/affiliates/'),
'Apify':('20–30%；宣传每客户最高$5000，档位适用性待核实','https://affiliate.apify.com/'),
'Crawlbase':('25%，最多6个月；至少3个付费推荐及$50才起付','https://crawlbase.com/affiliates'),
'Webshare':('首购50% + 续费10%，每客户上限$3000；KYC/PayPal','https://help.webshare.io/en/articles/8451043-affiliate-program'),
'IPRoyal':('10%，每客户上限$2000；6个月奖励窗口','https://help.iproyal.com/en/articles/7222595-do-you-have-a-referral-system'),
'SOAX':('最高50%，按档位','https://soax.com/affiliates'),
'Rayobyte':('15%总额度；给客户优惠与自身佣金共享该额度','https://portal.rayobyte.com/en/support/solutions/articles/64000262795-do-you-have-an-affiliate-program-'),
'Proxy-Cheap':('25%','https://www.proxy-cheap.com/referrals'),
'DataImpulse':('15%终身；退款扣回、首次提现人工审核','https://help.dataimpulse.com/en/articles/15931568-commissions-and-payouts'),
'DigitalOcean':('10%，12个月；CPS联盟与用户赠金分开','https://www.digitalocean.com/affiliates'),
'Doola':('宣传30%起；同页$900/$1500上限不一致，按合作协议核定','https://www.doola.com/blog/doola-partner-programs-explained-affiliate-iframe-and-white-label/'),
'Deel':('$500合资格销售线索 + $1000成为付费客户；非每次注册','https://www.deel.com/es/affiliates/'),
'BandwagonHost':('22%；首提人工审核，PayPal/账户余额','https://bandwagonhost.com/affiliates-info.php'),
'Evoxt':('10%至对应服务取消；条款限制优惠码站传播','https://evoxt.com/referral-program/','https://evoxt.com/terms-of-service/'),
'HostDare':('最高15%每单','https://www.hostdare.com/affiliates.html')}
d=json.loads(P.read_text())
for r in d['brands']:
 f=FACTS.get(r['brand'])
 if f:
  r.update(commission_rate=f[0],commission_sources=list(f[1:]),commission_checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),commission_status='官方公开条款已读取；本账号适用费率、批准及提现资格未核实')
 if r['brand'] in ['ScraperAPI','Evoxt']:r['action_priority']='先核对优惠站/优惠码传播条款及书面批准'
 if r['brand'] in ['Lambda Labs','Together AI','Modal','Stripe Atlas','Mercury','Vast.ai','Vultr','Cloudways','ScalaHosting','ZgoCloud','GTHost','ExtraVM','GoMami']:
  r['action_priority']='先核实现金佣金、实际协议及账号资格'
d['commission_method']='官方页面实读；没有把用户赠金、主机出租分成、第三方营销宣称当现金CPS；未知保留null。'
P.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Official commission entries',len(FACTS),'/',len(d['brands']))
