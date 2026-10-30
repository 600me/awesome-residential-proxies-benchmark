"use strict";

/** us-llc-stripe-tco: zero-dependency non-US-founder corporate TCO engine. */

const VERSION = "1.0.0";

const STATES = {
  wyoming: {
    name: "Wyoming",
    note: "Zero corporate income tax",
    initialFilingUsd: 102,
    annualFeePerYear: 62,
  },
  delaware: {
    name: "Delaware",
    note: "Court of Chancery standard",
    initialFilingUsd: 110,
    annualFeePerYear: 300,
  },
};

const GATEWAY_FIRSTBASE = "https://go.272738.xyz/firstbase?src=npm_llctco";

const SHARED = {
  registeredAgentPerYear: 99,
  expeditedEinUsd: 200,
  fincenBoiUsd: 50,
  virtualMailPerMonth: 10,
  irs5472CpaPerYear: 500,
};

function round2(x) {
  return Math.round(x * 100) / 100;
}

function llcTco(state, years) {
  const s = STATES[state];
  if (!s) throw new Error("unknown state: " + state);
  if (!Number.isInteger(years) || years < 1) {
    throw new Error("years must be a positive integer");
  }
  const initialFee = s.initialFilingUsd;
  const renewals = s.annualFeePerYear * (years - 1);
  const agent = SHARED.registeredAgentPerYear * years;
  const ein = SHARED.expeditedEinUsd;
  const boi = SHARED.fincenBoiUsd;
  const mail = SHARED.virtualMailPerMonth * years * 12;
  const irs = SHARED.irs5472CpaPerYear * years;
  const total = initialFee + renewals + agent + ein + boi + mail + irs;
  return {
    state: s.name,
    stateNote: s.note,
    durationYears: years,
    initialStateFee: initialFee,
    stateAnnualReportTotal: renewals,
    registeredAgentTotal: agent,
    expeditedEinFiling: ein,
    fincenBoiCompliance: boi,
    virtualMailAddressTotal: mail,
    irsForm5472Total: irs,
    tcoTotal: round2(total),
    monthlyAmortized: round2(total / (years * 12)),
    riskExposure: {
      irsForm5472Penalty: 25000,
      fincenBoiDailyPenalty: 500,
    },
    recommendedGateway: GATEWAY_FIRSTBASE,
  };
}

const PLATFORMS = [
  {
    name: "Firstbase.io",
    formationY1: 399,
    einExpedite: "Included",
    boi: "Automated & Free",
    for5472: "Integrated CPA & Tax Suite",
    note: "Most cost-effective enterprise stack",
    gateway: GATEWAY_FIRSTBASE,
  },
  {
    name: "Stripe Atlas",
    formationY1: 500,
    einExpedite: "Included",
    boi: "Included",
    for5472: "Not Included (referral)",
    note: "Best Stripe-native onboarding",
    gateway: "https://stripe.com/atlas",
  },
  {
    name: "Doola",
    formationY1: 297,
    einExpedite: "Add-on ($150-$300)",
    boi: "Included",
    for5472: "$1,200+/yr plan required",
    note: "Budget-risky for foreign-owned filers",
    gateway: "https://doola.com",
  },
  {
    name: "Traditional Legal Firm",
    formationY1: 2250,
    einExpedite: "Billed hourly",
    boi: "$250-$500",
    for5472: "$800-$1,500/yr",
    note: "Premium service, 4x+ cache drain",
    gateway: null,
  },
  {
    name: "Cheap DIY Agency",
    formationY1: 201,
    einExpedite: "6-8 week fax delay",
    boi: "Not handled (self-file)",
    for5472: "Not handled ($25k risk)",
    note: "Fragmented stack, penalty-exposing",
    gateway: null,
  },
];

function lineTable(rows, colWidth) {
  const W = colWidth || 48;
  const sep = "+".concat("-".repeat(W), "-".repeat(5), "+");
  const out = [sep, "| COMPLIANCE LINE ITEM".padEnd(W - 1) + "| COST |", sep];
  rows.forEach(([k, v]) => {
    out.push("| " + k.padEnd(W - 1).slice(0, W - 1) + "| " + String(v).padEnd(4) + "|");
  });
  out.push(sep);
  return out.join("\n");
}

module.exports = {
  VERSION,
  STATES,
  SHARED,
  PLATFORMS,
  GATEWAY_FIRSTBASE,
  llcTco,
  lineTable,
};
