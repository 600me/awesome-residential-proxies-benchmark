# Chrome Web Store listing

## Title
Proxy Fraud Checker

## Short description
See your public IP, hosting/ISP status and proxy/VPN risk signals in one click. No signup, no background access.

## Detailed description
Your exit IP is one of the first things many anti-bot systems evaluate. Check it before you debug anything else.

Proxy Fraud Checker shows the public IP your browser actually presents, whether that address belongs to a hosting provider or a non-hosting ISP, its provider/ASN, and the risk flags reported by a third-party lookup. It runs only when you open the popup or press Check again: no signup, no background polling, no page access, no analytics.

The popup then explains what the result does and does not mean. If the address is a hosting range or is flagged as a VPN, proxy or Tor node, the extension may show one clearly labeled paid link to a residential proxy provider. If the address looks like a normal ISP, no paid link is shown and the extension instead explains how to test the IP your crawler actually uses. Detection signals are third-party estimates: they can be incomplete or wrong, and they do not prove that a site blocked you or that a different IP will succeed.

Cost math, not marketing: 100GB of usable data can cost more than the sticker price suggests. Illustrative assumptions only — at $1/GB and 10% usable yield, hosting traffic costs $1,000; at $5/GB and 80% yield, residential traffic costs $625. The difference is $375. These are hypothetical inputs, not vendor prices, measured success rates or promised savings. Test on your own workload before purchasing.

Benchmark and methodology: https://proxy.mybskm.top/

## Affiliate disclosure
- The popup contains one paid link, to Decodo (formerly Smartproxy). If you subscribe through it, the publisher may earn a commission at no additional cost to you. The result shown above the link is produced by the IP lookup and is not affected by the commission.
- As of 2026-10-18, the Decodo landing page lists code TAKE5 for 5% off the first month on eligible plans, plus a 3-day free trial. Offers and terms are controlled by Decodo and can change; verify at checkout.
- No other provider link is shown. Bright Data is not displayed in v1.0.1 because no active affiliate agreement is in place.
- The extension does not modify links or cookies on other websites, does not inject affiliate codes, and does not open any link without a click.

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
Submission status: v1.0.1 was uploaded to the existing Proxy Fraud Checker item, the detailed description and affiliate disclosure above were saved, and screenshot-1280x800-v101.png replaced the previous screenshot. The Developer Dashboard confirmed submission and shows Pending review. Automatic publication after approval is enabled. Submission is not approval or publication of v1.0.1.

v1.0.1 changes: removed the leftover Chinese campaign line, removed the inactive Bright Data button, replaced the static offer block with a result-aware explanation (hosting / VPN-proxy-Tor / clean ISP / unknown), added the real Decodo offer and a one-line affiliate disclosure, and added a footer link to the store reviews page. No permission, host access or CSP change.

The runtime ZIP contains manifest.json, popup.html, popup.js, popup.css and the three PNG icons. It does not contain this listing file, screenshots or any internal notes.

Upload the ZIP in the Developer Dashboard; for local testing, unzip it and use chrome://extensions → Developer mode → Load unpacked. Public privacy URL: https://proxy.mybskm.top/privacy.html.

API schema reference: https://github.com/ipqwery/ipqwery
Chrome host permissions: https://developer.chrome.com/docs/extensions/develop/concepts/network-requests
