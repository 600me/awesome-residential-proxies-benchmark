# Chrome Web Store listing

## Title
Proxy Fraud Checker

## Short description
Check your public IP, hosting/ISP signals and reported risk. Compare residential proxies when 403s waste your crawl budget.

## Detailed description
Crawlers or multi-account workflows hitting 403 blocks? Check the IP your browser actually presents before another round of failed requests drains your bandwidth budget.

Proxy Fraud Checker shows your current public IP, Hosting vs ISP/non-hosting classification, provider/ASN and third-party risk signals in one click. It runs only when you open the popup or press Check again. No signup, no background polling, no page access.

100GB of usable data can cost more than the sticker price suggests. Illustrative assumptions: at $1/GB and 10% usable yield, hosting traffic costs $1,000; at $5/GB and 80% yield, residential traffic costs $625. The difference is $375. These are hypothetical inputs, not vendor prices, measured success rates or promised savings.

Crawlers / multi-account workflows frequently blocked by 403s? Explore high-purity residential proxies, exclusive offer placeholders and reproducible benchmarks. Compare Smartproxy and Bright Data through the clearly labeled links in the popup and test on your own workload before purchasing.

Required campaign wording (Chinese): 爬虫/多账号频繁遭遇 403 阻断？推荐高纯度住宅代理（附专属优惠与基准测试）

Referral links:
- Smartproxy: https://go.272738.xyz/smartproxy
- Bright Data: https://go.272738.xyz/brightdata

As of October 17, 2026, the Smartproxy / Decodo short link routes to the approved official affiliate link; qualifying purchases may earn the publisher a commission. The Bright Data application remains pending and its destination still contains an inactive REPLACE_ME referral placeholder. No exclusive discount code is confirmed. Recommendations are advertising links, not independent certification. The extension does not modify links on other websites or inject affiliate codes into your browsing.

An ISP/non-hosting result is a residential candidate, not proof of a residential household, exclusive use or cleanliness. Risk signals may be incomplete or inaccurate. This tool does not measure target-site success, bypass access controls, guarantee 403 avoidance or establish that an IP is fraudulent. Use services within the permissions and terms applicable to your work.

## Privacy policy / disclosure
Public privacy policy: https://proxy.mybskm.top/privacy.html

- Single purpose: display the browser's current public exit IP and its network/risk metadata.
- On popup open or manual refresh, an HTTPS request is sent directly to https://api.ipquery.io/?format=json. IPQuery necessarily receives your exit IP and normal request metadata. It provides the displayed IP, provider/ASN and risk information. Review the provider's current privacy terms at https://ipquery.io before use.
- The extension has no publisher backend. It does not collect browsing history, website content, account identifiers, cookies, passwords, payment information or precise device location. API geolocation fields, if returned, are neither displayed nor retained.
- No analytics, advertising SDK, local persistence, sale of data or data transfer to the publisher. Responses exist only in popup memory and are discarded when it closes. IPQuery's own processing/retention is governed by its terms; the publisher cannot control the provider's logs.
- Affiliate websites receive normal navigation data only if the user explicitly clicks an outgoing link. Requests to the lookup API omit credentials and referrers; outgoing links use noreferrer.
- Only https://api.ipquery.io/* host access is requested, solely for the explicit IP lookup. No tabs, activeTab, history, storage, scripting or all-sites access. No remote executable code.
- User data, if processed by this extension, is used solely to deliver the stated IP lookup feature, consistent with Chrome Web Store User Data Policy and Limited Use requirements.

When you explicitly open a privacy/benchmark page or an affiliate short link, the publisher's static web server receives normal connection metadata, including your exit IP, to serve the page or redirect. Access logging is disabled for these two sites; no analytics or tracking cookies are used. Operational error logs may contain connection metadata. This is separate from the extension's IP lookup, which goes directly to IPQuery.

## Package and submission notes
The ZIP contains manifest.json at its root, popup.html/js/css, three PNG icons and this listing. No build step or dependencies. Upload the ZIP in the Developer Dashboard; for local testing, unzip it and use chrome://extensions → Developer mode → Load unpacked. Chrome may reject direct ZIP dragging; Load unpacked is the supported local route.

Public privacy URL: https://proxy.mybskm.top/privacy.html. Before a public store submission, supply the store's publisher/contact details and required screenshots in the dashboard. This file is the listing text; a ZIP passing local checks does not imply store approval or publication. No fees or store submission are performed by packaging.

API schema reference: https://github.com/ipqwery/ipqwery
Chrome host permissions: https://developer.chrome.com/docs/extensions/develop/concepts/network-requests
