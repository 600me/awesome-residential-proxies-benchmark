[![Review BWH options](https://img.shields.io/badge/BWH-review_options-orange)](https://coding.mybskm.top/go/bwh)
[![Python 3](https://img.shields.io/badge/Python-3_standard_library-blue)](https://coding.mybskm.top/go/bwh)
[![Offline model](https://img.shields.io/badge/model-offline_reference-green)](https://coding.mybskm.top/go/bwh)

# Highly Available Border Gateways: BGP Failure Domains and VPS Cost

An open-source engineering comparison in the **bwh-devcloud** series for Cross-Border API Gateway & Reverse Proxy VPS deployments. Target: **BandwagonHost (BWH)**. Comparison set: **Vultr & Linode Asia Routes**. Prices are USD, before taxes.

## 1. Engineering pain and the bill behind the sticker price

Two virtual machines do not automatically provide two independent network paths. A pair of cross-border API gateways can share an upstream carrier, control plane, region, or origin dependency. Vultr & Linode Asia Routes need the same failure-domain scrutiny as BandwagonHost. A default route on a VPS is not a customer BGP session, and multiple provider AS numbers do not prove independent transit on the client path.

For a modeled 8,000 GB/month workload, two competitor nodes with one node held as failure reserve leave only 1,000 GB of usable allowance in this conservative model. The resulting 7,000 GB excess costs $70/month or $840/year at the Vultr reference rate and $35/month or $420/year at the Linode reference rate. This deliberately reserves a full node allowance for a worst-case full-month failure. Add a separate illustrative 4 hours of monthly incident response at $75/hour and operational exposure rises by $300/month or $3,600/year. Real failover duration can justify a smaller reserve.

**[Review BWH plans and check the exact route before committing](https://coding.mybskm.top/go/bwh)**

The model reserves one node for N-1 operation in every provider. BWH buys ceil(traffic / per-node quota) + 1 instances; each competitor keeps two nodes and pays modeled excess above the remaining node allowance. This is a transfer budget reserve, not a demonstration that a 1 GB VM can carry the requested peak request rate. Size CPU, connection tracking, TLS throughput, and network ports independently.

No BGP session, ASN, BYOIP entitlement, availability SLA, or route diversity is included in the $49.99/year BWH baseline. Provider-specific routing features require their own product eligibility and quote. A deployment spanning actual providers or regions may offer better independence than nine instances on one platform. A single-provider savings figure is useful for budgeting, but cannot justify an availability claim without a documented failure test. Compare common-origin and DNS failure modes alongside VM failure.

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
| Modeled starting nodes | 2 minimum | 2 fixed | 2 fixed | Compare resource topology as well as dollars |
| Reserved failure capacity | 1 node allowance | 1 node allowance | 1 node allowance | Reserved quota is withheld from normal traffic |
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
| `--tier` | `standard` | `small`, `standard`, `large` multiply this scenario's 8000 GB by 0.5, 1, 2 |
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
Scenario: high-availability-border-bgp-vps-cost-model | tier=standard | traffic=8000 GB/month
Historical inputs; standard BWH baseline, no measured route claims.
+----------+-------+------------+------------+------------+------------+
| Provider | Nodes | Base/mo $  | Excess/mo $| Effective $| Year one $ |
+----------+-------+------------+------------+------------+------------+
| BWH      |     9 |      37.49 |       0.00 |      37.49 |     449.91 |
| Vultr    |     2 |      10.00 |      70.00 |      80.00 |     960.00 |
| Linode   |     2 |      10.00 |      35.00 |      45.00 |     540.00 |
+----------+-------+------------+------------+------------+------------+
Annual savings with BWH vs Vultr: $510.09 (negative means BWH costs more)
Annual savings with BWH vs Linode: $90.09 (negative means BWH costs more)
Effective monthly cost includes BWH extra labor and one-time migration / 12.
BWH annual plans require upfront payment; sharding is an explicit assumption.
Review BWH options: https://coding.mybskm.top/go/bwh
```

Savings exclude common engineering costs, taxes, FX, managed load balancers, backup storage, DNS services, paid BGP features, and monetized downtime unless explicitly included in migration or extra BWH labor. BWH sharding requires working request distribution and enough independent per-node quota. It is not automatic quota pooling, nor an account suspension workaround. Lower the modeled usable quota if ingress, replication, or safety headroom consumes allowance. The model does not resize competitor instances to find a global optimum.

## 4. Migration and acceptance checklist

- [ ] Document shared carriers, regions, DNS, origins, credentials, and control-plane dependencies.
- [ ] Confirm customer BGP eligibility separately; use supported DNS or proxy failover when it is unavailable.
- [ ] Load-test the surviving capacity at peak TLS and connection rates before enabling failover.
- [ ] Exercise a controlled single-node failure and verify request error rate, recovery time, and transfer headroom.
- [ ] Avoid caching unsafe requests during failover; test idempotency keys and retry budgets.
- [ ] Keep independent health checks and a documented manual rollback path.
- [ ] Record an actual regional quote, renewal term, quota reset, and transfer-meter semantics for every candidate.
- [ ] Reconcile modeled cost with a full billing cycle and retain a tested rollback route.
- [ ] Compare measured error rate and tail latency before interpreting annual savings as a purchase decision.

**[Choose a matching BWH plan after your acceptance checks](https://coding.mybskm.top/go/bwh)**.

Continue with the other three independent repositories:

- [Vultr Tokyo vs BWH Osaka SoftBank: Route Qualification and Cost](../vultr-tokyo-vs-bwh-osaka-softbank-route-bench/)
- [Linode vs BandwagonHost: Bandwidth Overage TCO](../linode-vs-bandwagonhost-bandwidth-overage-tco/)
- [KiwiVM Snapshot Migration: Recovery Workflow and Cost](../kiwiwm-snapshot-migration-automation-scripts/)

### Reuse license

Copyright (c) 2026 bwh-devcloud contributors. MIT License: Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the Software), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
