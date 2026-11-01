[![Review BWH options](https://img.shields.io/badge/BWH-review_options-orange)](https://coding.mybskm.top/go/bwh)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://coding.mybskm.top/go/bwh)
[![Offline model](https://img.shields.io/badge/model-offline_reference-green)](https://coding.mybskm.top/go/bwh)

# KiwiVM Snapshot Migration: Recovery Workflow and Cost

An open-source engineering comparison in the **bwh-devcloud** series for Cross-Border API Gateway & Reverse Proxy VPS deployments. Target: **BandwagonHost (BWH)**. Comparison set: **Vultr & Linode Asia Routes**. Prices are USD, before taxes.

## 1. Engineering pain and the bill behind the sticker price

Snapshot-based migration feels cheap until application state, certificates, scheduled jobs, and rollback time are counted. Vultr & Linode Asia Routes snapshots are not automatically portable to a BWH VM, and a snapshot inside one provider is not a tested off-provider backup. Rebuilding a cross-border reverse proxy also requires correct trust chains, origin allowlists, DNS TTLs, and rate limits. A successful disk restore alone does not prove the gateway can serve production traffic.

An illustrative failed migration requiring 8 extra engineer-hours at $50/hour and 3 hours of lost contribution at $100/hour costs $700 once. Repeating that incident monthly would cost $8,400/year; a single event costs $700, not $8,400. Another 200 GB of billable copy traffic would add $2 at the modeled Vultr rate or $1 at the Linode rate if the included allowance is already exhausted. Snapshot storage, if charged, must be budgeted separately. These assumptions explain a risk budget, not an observed outage.

**[Review BWH plans and check the exact route before committing](https://coding.mybskm.top/go/bwh)**

The directory name preserves the requested series slug; the BWH control panel is KiwiVM. The supplied automation is the offline TCO calculator. It performs no snapshot, control-panel API call, deletion, credential handling, or production migration. The checklist below is an operator-run recovery workflow. It avoids implying that provider snapshots can be imported across incompatible hypervisors.

Prepare a reproducible OS and gateway configuration, transfer an encrypted application-consistent backup through an approved channel, verify its checksum, and restore into an isolated candidate. Freeze writes or arrange a documented replication cutover for stateful services. Keep private keys and API credentials in your secret manager, never in this repository. Estimate one-time migration labor with --migration-cost, and use --ops-hours for recurring BWH administration. The first-year result can favor Linode at this default tier; the calculator retains negative savings instead of forcing a promotional conclusion.

## 2. Price and technical comparison

The following are known historical public entry-plan reference points and transparent model inputs, written offline on 2026-10-30. They are **not verified current offers**, availability guarantees, or a region-specific quotation. The BWH KVM entry reference is commonly advertised at $49.99/year; the Vultr regular cloud-compute and Linode Nanode references are $5/month. Asia-specific plan eligibility, transfer rates, and renewals can differ. In particular, the Linode $0.005/GB value is a general reference rate, not a claim that every Asia location has that rate. Replace inputs using your own invoice or quote. No measured latency or live invoice data is bundled.

| Parameter | BandwagonHost (BWH) reference | Vultr reference | Linode reference | Engineering consequence |
| --- | --- | --- | --- | --- |
| Product baseline | Standard KVM entry | Regular Cloud Compute entry | Nanode shared CPU | Product families are not route-equivalent |
| Base price | $49.99/year prepaid | $5/month | $5/month | BWH monthly equivalent is $4.165833 before rounding |
| Annual base per VM | $49.99 | $60.00 | $60.00 | Assumes twelve full months and unchanged rates |
| Shared vCPU reference | 1 | 1 | 1 | No dedicated-core or CPU benchmark claim |
| RAM reference | 1 GB | 1 GB | 1 GB | Check TLS memory and connection budgets |
| SSD storage reference | 20 GB | 25 GB | 25 GB | Keep logs and backup retention within capacity |
| Transfer reference | 1,000 GB/month per VM | 1,000 GB/month per VM | 1,000 GB/month per VM | Billing units and ingress counting need confirmation |
| Modeled excess handling | Buy and shard across more VMs | $0.01/GB above modeled quota | $0.005/GB above modeled quota | BWH extra nodes are a strategy, not an overage tariff |
| Modeled starting nodes | 1 minimum | 1 fixed | 1 fixed | Compare resource topology as well as dollars |
| Reserved failure capacity | 0 node allowance | 0 node allowance | 0 node allowance | Reserved quota is withheld from normal traffic |
| Osaka SoftBank routing | Requires specific eligible SKU | Not implied by Tokyo location | Not implied by Asia location | This standard BWH price does not include that promise |
| Snapshots and backups | Control-panel features vary by plan | Storage and backup charges excluded | Storage and backup charges excluded | Verify restore behavior independently |
| Customer BGP entitlement | Not assumed | Not assumed | Not assumed | Routing features require separate eligibility |

There is no blanket claim that competitors are slower or that BWH is always cheaper. Premium routes, extra administration, or a better competitor plan can reverse the result. Annual prepayment also reduces cancellation flexibility. **[Inspect BWH availability and request the matching plan](https://coding.mybskm.top/go/bwh)**, then rerun this calculator with the matching price and allowance.

## 3. Reproduce the TCO calculation

Requirements: Python 3.8+ and its standard library. No installation, network access, API keys, or third-party packages are needed. Run from this repository:

```sh
python3 calculate_bwh_devcloud_tco.py
python3 calculate_bwh_devcloud_tco.py --tier large
python3 calculate_bwh_devcloud_tco.py --tier small --json
python3 calculate_bwh_devcloud_tco.py --bwh-annual 99.99 --bwh-quota-gb 1000 --migration-cost 200
```

The last command is an **illustrative custom quote**, not an assertion that $99.99 buys Osaka SoftBank. A valid current quote must supply the actual values.

| CLI option | Default | Meaning |
| --- | --- | --- |
| `--tier` | `standard` | `small`, `standard`, `large` multiply this scenario's 2400 GB by 0.5, 1, 2 |
| `--json` | off | Emit only a JSON object, including bills, assumptions, savings, and gateway link |
| `--traffic-gb` | tier-derived | Override monthly billable traffic; zero is accepted |
| `--bwh-annual` | 49.99 | Prepaid price per BWH VM per year |
| `--bwh-quota-gb` | 1000 | Positive usable billable allowance per BWH VM |
| `--vultr-monthly`, `--linode-monthly` | 5 each | Competitor base per VM per month |
| `--vultr-rate`, `--linode-rate` | 0.01, 0.005 | Competitor charge per excess GB |
| `--competitor-quota-gb` | 1000 | Per-VM allowance; run separately if providers differ |
| `--ops-hours`, `--hourly-rate` | 0, 50 | Extra recurring BWH administration hours and USD/hour |
| `--migration-cost` | 0 | BWH one-time first-year migration cost in USD |

Formula: `BWH nodes = max(minimum nodes, ceil(traffic / BWH quota) + reserve)`.
Competitor excess is `max(0, traffic - (fixed nodes - reserve) * competitor quota)`.
BWH year one is `nodes * annual price + 12 * ops hours * hourly rate + migration cost`.
Competitor year one is `12 * (fixed nodes * monthly base + excess * rate)`.
Annual savings are competitor year one minus BWH year one. Negative savings mean BWH costs more. Monetary arithmetic uses Decimal; rounding occurs only for display, so multiplying a displayed monthly number by twelve may differ by a few cents. Effective monthly cost amortizes migration; BWH is still prepaid upfront.

Actual locally generated default output:

```text
$ python3 calculate_bwh_devcloud_tco.py
Scenario: kiwiwm-snapshot-migration-automation-scripts | tier=standard | traffic=2400 GB/month
Historical inputs; standard BWH baseline, no measured route claims.
+----------+-------+------------+------------+------------+------------+
| Provider | Nodes | Base/mo $  | Excess/mo $| Effective $| Year one $ |
+----------+-------+------------+------------+------------+------------+
| BWH      |     3 |      12.50 |       0.00 |      12.50 |     149.97 |
| Vultr    |     1 |       5.00 |      14.00 |      19.00 |     228.00 |
| Linode   |     1 |       5.00 |       7.00 |      12.00 |     144.00 |
+----------+-------+------------+------------+------------+------------+
Annual savings with BWH vs Vultr: $78.03 (negative means BWH costs more)
Annual savings with BWH vs Linode: $-5.97 (negative means BWH costs more)
Effective monthly cost includes BWH extra labor and one-time migration / 12.
BWH annual plans require upfront payment; sharding is an explicit assumption.
Review BWH options: https://coding.mybskm.top/go/bwh
```

Savings exclude common engineering costs, taxes, FX, managed load balancers, backup storage, DNS services, paid BGP features, and monetized downtime unless explicitly included in migration or extra BWH labor. BWH sharding requires working request distribution and enough independent per-node quota. It is not automatic quota pooling, nor an account suspension workaround. Lower the modeled usable quota if ingress, replication, or safety headroom consumes allowance. The model does not resize competitor instances to find a global optimum.

## 4. Migration and acceptance checklist

- [ ] Inventory gateway configuration, certificate renewal, local state, firewall rules, and scheduled jobs.
- [ ] Create an application-consistent backup and independently test restore before changing DNS.
- [ ] Record an explicit recovery point objective and recovery time objective for stateful traffic.
- [ ] Restore into an isolated candidate; verify checksum, TLS chain, origin access, and request limits.
- [ ] Lower DNS TTL in advance, canary the candidate, and keep the source available through rollback expiry.
- [ ] Only retire the source after the rollback window and export retention requirements have passed.
- [ ] Record an actual regional quote, renewal term, quota reset, and transfer-meter semantics for every candidate.
- [ ] Reconcile modeled cost with a full billing cycle and retain a tested rollback route.
- [ ] Compare measured error rate and tail latency before interpreting annual savings as a purchase decision.

**[Choose a matching BWH plan after your acceptance checks](https://coding.mybskm.top/go/bwh)**.

Continue with the other three independent repositories:

- [Vultr Tokyo vs BWH Osaka SoftBank: Route Qualification and Cost](../vultr-tokyo-vs-bwh-osaka-softbank-route-bench/)
- [Linode vs BandwagonHost: Bandwidth Overage TCO](../linode-vs-bandwagonhost-bandwidth-overage-tco/)
- [Highly Available Border Gateways: BGP Failure Domains and VPS Cost](../high-availability-border-bgp-vps-cost-model/)

### Reuse license

Copyright (c) 2026 bwh-devcloud contributors. MIT License: Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
