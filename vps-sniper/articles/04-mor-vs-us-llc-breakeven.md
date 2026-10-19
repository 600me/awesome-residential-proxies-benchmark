A founder in Lisbon runs a B2B SaaS at **$8,000 MRR** with a **$40 average order value**. She sells to customers in forty countries, prices in US dollars, and pays a Merchant of Record 5% plus 50 cents per order. Her spreadsheet says the MoR costs $500 a month. Stripe's advertised 2.9% plus 30 cents looks like it would cost $292. The gap is $208 a month, or roughly $2,500 a year. She starts planning an escape.

Then she reads a compliance invoice, discovers that 70% of her cards are issued outside the United States, and notices that Stripe charges extra for exactly the customers she has. The real Stripe cost is not $292. It is $459.33 once fixed fees and a $1,000 annual compliance budget are included. The saving is $488 a year, not $2,500. Still positive, but a different decision. If she also settles in euros or pounds and Stripe converts the payout to dollars, Stripe costs **$539.33** a month and the MoR is **$39.33 cheaper every month**.

That is the 5% illusion: the headline spread between two percentage rates is not the spread between two businesses. The correct question is not "is 2.9% lower than 5%?" It is "at my card mix, my order size and my compliance bill, how much revenue do I need before the self-managed route actually wins?" That question has an exact answer, and it moves.

## Why the 2.9% versus 5% comparison fails

Two numbers are being compared as if they describe the same transaction. They do not.

**First, the MoR rate is all-in for card processing.** Lemon Squeezy and Paddle quote roughly 5% plus 50 cents per transaction on their pay-as-you-go plans. That fee covers the payment, the billing layer and the indirect-tax handling the provider performs as the seller of record. There is no separate compliance budget line, because the provider is the merchant. The trade is real: you pay a premium for someone else to own sales-tax registration, collection and remittance on covered sales.

**Second, Stripe's 2.9% is a domestic-card rate.** Stripe's US pricing adds **1.5%** when the card is issued outside the United States, and **1%** when a charge is made in another currency and converted. Neither surcharge appears in the headline. A globally distributed SaaS does not process domestic cards only. The observed international share is an input to the decision, not a footnote.

**Third, the fixed fees differ.** The MoR charges 50 cents per order; Stripe charges 30 cents. That 20-cent spread favors Stripe per order, but it is dwarfed by a five-figure compliance budget at low order values.

**Fourth, an LLC is not free.** Formation is a one-time cost. Keeping the company alive is annual: state reports or franchise tax, a registered agent, and for a foreign-owned single-member LLC the federal filings that carry a $25,000 penalty when missed. The model treats that as an annual budget `C`, divided by twelve so it can be compared with monthly processing fees.

Once those four facts are on the table, the comparison becomes arithmetic instead of vibes.

## The algebra, written out

Let `R` be monthly revenue, `A` the average order value, `N = R / A` the number of orders per month, `C` the annual compliance budget, and `r` the effective Stripe rate including international and FX surcharges.

```text
MoR    = 0.05 × R + 0.50 × N
Stripe = r × R + 0.30 × N + C / 12
N      = R / A
```

Set them equal to find the break-even revenue `B`:

```text
0.05B + 0.50(B / A) = rB + 0.30(B / A) + C / 12
B × [(0.05 − r) + (0.20 / A)] = C / 12
B = (C / 12) / [(0.05 − r) + (0.20 / A)]
```

The bracket is the **rate delta**: the percentage advantage of Stripe over the MoR, plus the fixed-fee advantage per dollar of average order value. If the bracket is zero or negative, Stripe never catches up, no matter how large the revenue. The break-even is not a number; it is a function of three inputs:

- **Effective Stripe rate `r`** — 2.9% domestic, 3.95% at 70% international cards, 4.95% with a 1% FX conversion.
- **Average order value `A`** — smaller orders make the 20-cent fixed-fee gap matter more.
- **Annual compliance budget `C`** — higher overhead pushes the break-even to the right.

The monthly difference is simply `delta = MoR − Stripe`. A positive delta means the LLC route is cheaper this month; negative means the MoR is cheaper. Annualize the unrounded monthly difference, never the rounded display value.

**The one-line rule:** break-even MRR = monthly compliance cost ÷ [(5% − effective Stripe rate) + $0.20 ÷ AOV]. If the denominator is not positive, there is no break-even.

## Three tiers, three completely different answers

The same founder, the same $40 AOV and the same $1,000 annual compliance budget produce three different decisions as the card mix changes.

| Tier | Card mix | Effective Stripe rate | Rate delta | Break-even MRR |
|---|---|---|---|---|
| **Tier 1** | 100% US domestic cards | 2.90% + $0.30 | 2.60% | **$3,205 / mo** |
| **Tier 2** | 70% international cards (+1.5%) | 3.95% + $0.30 | 1.55% | **$5,376 / mo** |
| **Tier 3** | 70% international + 1% FX | 4.95% + $0.30 | 0.55% | **$15,152 / mo** |

The mechanics are worth pausing on. Tier 1's denominator is 2.1% + 0.5% = 2.6%, so $83.33 of monthly overhead divided by 2.6% gives $3,205. Tier 2's denominator is 1.05% + 0.5% = 1.55%, so the same overhead divided by 1.55% gives $5,376. Tier 3's denominator collapses to 0.05% + 0.5% = 0.55%, and the break-even explodes to $15,152. Nothing about the company changed. The customers' card issuers and the settlement currency changed.

## Tier 1: the US-domestic case

At $8,000 MRR and a $40 AOV, there are 200 orders. The MoR charges 5% of revenue plus 50 cents per order: $400 + $100 = **$500.00 per month**. Stripe charges 2.9% of revenue, 30 cents per order and one-twelfth of the compliance budget: $232 + $60 + $83.33 = **$375.33 per month**. The LLC route wins by $124.67 a month, or **$1,496 a year**.

| At $8,000 MRR / $40 AOV / $1,000 a year | MoR | US LLC + Stripe | Difference |
|---|---|---|---|
| Revenue fee | $400.00 | $232.00 | +$168.00 |
| Per-order fee | $100.00 | $60.00 | +$40.00 |
| Compliance budget / 12 | $0.00 | $83.33 | −$83.33 |
| **Monthly total** | **$500.00** | **$375.33** | **+$124.67** |
| **Annual total** | **$6,000.00** | **$4,504.00** | **+$1,496.00** |

The break-even is $3,205 MRR. Below that, the $1,000 compliance budget cannot be recovered from a 2.6-point rate advantage and a 20-cent order advantage. Above it, every additional dollar of revenue widens the gap. That is the honest version of the "2.9% is cheaper" story: it is cheaper, but only after a revenue threshold, and only for a merchant whose customers pay with US-issued cards.

## Tier 2: the global SaaS default

Most non-US SaaS products do not have a 100% domestic card mix. A 70% international share is a realistic planning assumption for a product with customers across Europe, Asia and Latin America. Stripe's effective rate becomes 2.9% + (70% × 1.5%) = **3.95%**.

At $8,000 MRR the fee decomposition is $316 revenue fee + $60 per-order fee + $83.33 compliance = **$459.33 per month**. The MoR is still $500, so the LLC saves $40.67 a month, or **$488 a year**. The break-even rises to **$5,376 MRR** because the rate delta shrank from 2.6% to 1.55% while overhead stayed the same.

Scale changes the picture. At $20,000 MRR with the same $40 AOV, there are 500 orders. The MoR charges $1,000 + $250 = **$1,250 per month**. Stripe charges $790 + $150 + $83.33 = **$1,023.33 per month**. The saving is $226.67 a month, or **$2,720 a year**. The compliance overhead is now a rounding error against the revenue spread, which is why the decision flips decisively once a company is past the break-even and stays there.

| 70% international cards, $40 AOV, $1,000 a year | MoR monthly | Stripe monthly | Monthly saving | Annual saving |
|---|---|---|---|---|
| $8,000 MRR (200 orders) | $500.00 | $459.33 | $40.67 | **$488.00** |
| $20,000 MRR (500 orders) | $1,250.00 | $1,023.33 | $226.67 | **$2,720.00** |

This is the tier where the "lazy tax" argument becomes credible for a $60k ARR business. At $5,000 MRR the LLC route is only barely ahead; at $8,000 it saves $488 a year; at $20,000 it saves $2,720. Staying on a MoR is not irrational at $5,000 MRR. Staying on it at $20,000 MRR without doing the math is how founders donate thousands of dollars a year to convenience they no longer need.

## Tier 3: the non-USD checkout trap

Now add the currency conversion. If the product is priced in euros, pounds or another currency and Stripe converts the charge to US dollars, Stripe's US pricing adds **1%**. The effective rate becomes 4.95%, and the break-even jumps to **$15,152 MRR**.

At $8,000 MRR the numbers are $396 revenue fee + $60 per-order fee + $83.33 compliance = **$539.33 per month**. The MoR is **$500.00**. The self-managed route is now **$39.33 more expensive every month** — about $472 a year — and the founder who switched early would have paid for the privilege of doing more work.

This is the most important operational insight in the whole model. The LLC route is not a maturity badge. It is a bet that your effective Stripe rate stays far enough below 5% to repay a fixed compliance bill. A multi-currency product at low MRR can lose that bet even while its headline processing rate looks cheaper. At $20,000 MRR in Tier 3, the math flips again: Stripe costs $990 + $150 + $83.33 = $1,223.33 against the MoR's $1,250, a saving of just $26.67 a month. The company is above break-even but the margin is thin. At $8,000 MRR it is negative.

There are two honest responses. The first is to stay on the MoR until the revenue is high enough to clear the Tier 3 break-even. The second is to change the input: price and settle in USD, renegotiate the currency conversion, or use a payment setup that does not add the 1% conversion on every charge. The model does not tell you which is possible. It tells you what each choice costs.

## The US LLC bill nobody puts in the headline

Formation is the visible cost and the least interesting one. Firstbase lists a **$399** company-formation package; state filing fees and optional add-ons sit on top. That is a one-time expense, and it is not the number that decides the comparison. The recurring bill is.

- **State annual report or franchise tax.** Wyoming's annual report carries a modest minimum; Delaware's franchise tax starts around $300 for a small LLC. Neither is zero, and both are due whether or not the company earns anything.
- **Registered agent.** Typically $50 to $300 a year. A foreign founder without a US address needs one, and the address is also what keeps service of process and state mail from disappearing.
- **IRS Form 5472 and pro forma Form 1120.** A foreign-owned single-member LLC is generally treated as a disregarded entity for income tax but is still a reporting corporation. It must file Form 5472 with a pro forma Form 1120. Missing or late filing can trigger a **$25,000** penalty. This is the compliance red line, not a paperwork preference.
- **Bookkeeping and tax preparation.** A US return, a foreign owner's information reporting and a home-country filing do not prepare themselves. Even a lean DIY setup consumes hours that have a market price.
- **Banking, mail and sales-tax registrations.** A US business bank account, a mail-forwarding address and any state sales-tax registrations add recurring cost. An LLC does not guarantee Stripe approval, and it does not make sales-tax obligations disappear; it moves them to you.

The model uses **$1,000 a year** as a planning allowance, which is deliberately lean: it covers a modest state bill, a registered agent and basic 5472 preparation in a good year. A founder with a Delaware LLC, professional bookkeeping and multiple state registrations should raise it. The point is not that $1,000 is the true cost for everyone. The point is that the comparison is sensitive to the number, and the calculator lets you change it.

**Do not model the LLC as "Stripe minus 2.1%".** Model it as "Stripe at my effective rate, plus a fixed annual overhead, plus my own time". The break-even formula only works when the overhead is in the equation.

## What to do with this on a Monday morning

1. **Measure your international share.** Export a month of charges from Stripe or your MoR and count cards by issuer country. Do not guess. A 70% assumption is a planning default, not a measurement.
2. **Check your settlement currency.** If you price in USD and receive USD, the FX input is zero. If your checkout charges in local currencies and converts, enable the 1% line and watch the break-even move.
3. **Price the compliance year honestly.** Add state fees, registered agent, Form 5472 preparation and the hours you will spend. Use that number, not a vendor's formation package price.
4. **Compute the break-even, then compare it with your actual MRR.** Below it, the MoR is doing useful work. Above it, the annual gap is real money.
5. **Re-run the model when the mix changes.** A product that shifts from US early adopters to global customers can cross a break-even in the wrong direction. The decision is not permanent.

The calculator on the site implements the formulas above exactly. The `intl` slider sets the international card share from 0% to 100% in 5-point steps, the `fx` switch adds the 1% conversion, and both are written to the URL so a scenario can be shared or bookmarked. The three presets load the three tiers in this article at $8,000 MRR, $40 AOV and $1,000 annual compliance.

- [Tier 2 at $8,000 MRR](https://pay.mybskm.top/?mrr=8000&aov=40&intl=70) — 70% international cards, no FX: break-even $5,376, saving $488 a year.
- [Tier 2 at $20,000 MRR](https://pay.mybskm.top/?mrr=20000&aov=40&intl=70) — the same mix at scale: saving $2,720 a year.
- [Tier 3 at $8,000 MRR](https://pay.mybskm.top/?mrr=8000&aov=40&intl=70&fx=1) — add FX and the MoR becomes $39.33 a month cheaper.

If the numbers say the LLC route is worth it, the formation step is the next decision, not the first one. Firstbase's $399 package is a reasonable starting point for a foreign founder who wants a US entity without assembling the paperwork alone. Compare the state fee, the registered-agent renewal and the 5472 preparation quote before you pay for anything, and keep the annual compliance budget in the model even after the company exists.

## The decision is a threshold, not an identity

The 5% MoR fee is not a scam, and Stripe is not automatically cheaper. Each is a bundle of services with a different cost structure. The MoR bundles processing, billing and indirect-tax handling into a revenue percentage. The LLC route unbundles them: you get a lower variable rate, but you buy compliance, filings and administrative attention separately, and you pay for them whether or not the revenue arrives.

For a non-US founder, the correct sequence is unglamorous. Measure the card mix. Put the real compliance bill in the model. Compute the break-even. Compare it with the revenue you actually have, not the revenue you hope to have next year. Then choose the cheaper bundle for the next twelve months and revisit when the inputs change.

At $8,000 MRR with US cards, that exercise says the LLC saves $1,496 a year. At the same revenue with 70% international cards, it says $488. With a non-USD checkout, it says the MoR wins by $39.33 a month. Three different answers from the same headline rates. The only way to know which one is yours is to stop comparing 2.9% with 5% and start comparing the two complete businesses.

---

**Run your own numbers:** [open the payment calculator](https://pay.mybskm.top/) or start with the [70% international scenario](https://pay.mybskm.top/?mrr=8000&aov=40&intl=70).

**Form a US LLC:** [Firstbase ($399 formation package)](https://go.272738.xyz/firstbase?src=devto_mor_breakeven). State fees and optional add-ons are extra.

**FTC disclosure:** some links above are affiliate links. If you buy through them, I may earn a commission at no extra cost to you. A commission never changes the price you pay and does not buy a ranking. This is a planning model with stated assumptions, not financial, tax or legal advice. Verify current provider pricing and filing duties before you commit.
