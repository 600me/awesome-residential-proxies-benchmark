"use strict";

// Outbound links. The query string is a counting key for our own relay
// (go.272738.xyz). It is not forwarded to the merchant, so it cannot be used
// to attribute sales in the affiliate dashboard.
const LINKS = Object.freeze({
  smartproxy: "https://go.272738.xyz/smartproxy?utm_source=chrome_extension&utm_medium=popup&utm_campaign=v101",
  benchmark: "https://proxy.mybskm.top/?utm_source=chrome_extension&utm_medium=popup&utm_campaign=v101"
});

// Copy is keyed by the classification actually returned by the API.
// No score thresholds: the API reports 0/20 in practice and has no usable
// numeric cutoff for "high risk".
const COPY = Object.freeze({
  hosting: {
    kicker: "WHAT THIS MEANS",
    title: "This exit IP belongs to a hosting provider.",
    body: "Anti-bot systems often treat hosting ranges as higher risk. That can contribute to 403 or 429 responses, but it does not prove you were blocked.",
    cta: "See Decodo proxy options ↗",
    note: "Decodo (formerly Smartproxy) lists code TAKE5 for 5% off the first month on eligible plans, plus a 3-day trial.",
    disclosure: "Paid link: we may earn a commission if you subscribe. The result above is not affected."
  },
  anonymity: {
    kicker: "WHAT THIS MEANS",
    title: "This exit is flagged as a VPN, proxy or Tor node.",
    body: "Some sites restrict these networks more aggressively. If requests are failing, this is one plausible factor, not a diagnosis.",
    cta: "See Decodo proxy options ↗",
    note: "Decodo (formerly Smartproxy) lists code TAKE5 for 5% off the first month on eligible plans, plus a 3-day trial.",
    disclosure: "Paid link: we may earn a commission if you subscribe. The result above is not affected."
  },
  isp: {
    kicker: "WHAT THIS MEANS",
    title: "This exit looks like a normal ISP address.",
    body: "If your crawler runs on a server or proxy, this is not the IP your target site sees. Check that machine’s exit address before changing anything.",
    cta: null,
    note: "No paid link is shown for this result.",
    disclosure: null
  },
  unknown: {
    kicker: "WHAT THIS MEANS",
    title: "Not enough signal to classify this exit.",
    body: "The lookup returned partial data. The result above is what the API reported; no recommendation is made from it.",
    cta: null,
    note: "No paid link is shown for this result.",
    disclosure: null
  }
});

const BENCHMARK_LABEL = {
  hosting: "How we test proxy providers ↗",
  anonymity: "How we test proxy providers ↗",
  isp: "How to test the IP your crawler actually uses ↗",
  unknown: "Read the benchmark methodology ↗"
};

const FLAGS = { is_vpn: "VPN", is_proxy: "Proxy", is_tor: "Tor", is_datacenter: "Hosting" };

function classify(risk) {
  if (!risk || typeof risk !== "object") return "unknown";
  if (risk.is_datacenter === true) return "hosting";
  if (risk.is_vpn === true || risk.is_proxy === true || risk.is_tor === true) return "anonymity";
  const complete = Object.keys(FLAGS).every((key) => typeof risk[key] === "boolean");
  return complete ? "isp" : "unknown";
}

function describeNetwork(risk) {
  const flags = risk && typeof risk === "object" ? risk : {};
  const network = flags.is_datacenter === true ? "Hosting / datacenter"
    : flags.is_datacenter === false ? "ISP / non-hosting candidate" : "Unknown";
  const detected = Object.entries(FLAGS).filter(([key]) => flags[key] === true).map(([, name]) => name);
  const complete = Object.keys(FLAGS).every((key) => typeof flags[key] === "boolean");
  const score = typeof flags.risk_score === "number" && Number.isFinite(flags.risk_score)
    && flags.risk_score >= 0 && flags.risk_score <= 100 ? flags.risk_score : null;
  const scoreText = score === null ? "" : ` · ${score}/100`;
  const riskText = detected.length ? `Flagged: ${detected.join(", ")}${scoreText}`
    : complete ? `No listed flags detected${scoreText}` : "Unknown / incomplete data";
  return { network, risk: riskText };
}

function renderOffer(state) {
  const copy = COPY[state];
  if (!copy) return;
  const offer = document.getElementById("offer");
  document.getElementById("offer-kicker").textContent = copy.kicker;
  document.getElementById("offer-title").textContent = copy.title;
  document.getElementById("offer-body").textContent = copy.body;

  const cta = document.getElementById("cta");
  const tag = document.getElementById("offer-tag");
  const note = document.getElementById("offer-note");
  const disclosure = document.getElementById("offer-disclosure");
  const benchmark = document.getElementById("benchmark");

  if (copy.cta) {
    cta.textContent = copy.cta;
    cta.hidden = false;
    tag.hidden = false;
  } else {
    cta.hidden = true;
    tag.hidden = true;
  }
  note.textContent = copy.note;
  note.hidden = !copy.note;
  if (copy.disclosure) {
    disclosure.textContent = copy.disclosure;
    disclosure.hidden = false;
  } else {
    disclosure.hidden = true;
  }
  // One action per state: the money states use the CTA, the neutral states
  // use the benchmark link (also present in the footer).
  benchmark.textContent = BENCHMARK_LABEL[state];
  benchmark.hidden = Boolean(copy.cta);
  offer.dataset.state = state;
  offer.hidden = false;
}

async function checkIP() {
  const result = document.getElementById("result");
  const offer = document.getElementById("offer");
  const refresh = document.getElementById("refresh");
  const status = document.getElementById("status");
  refresh.disabled = true;
  result.setAttribute("aria-busy", "true");
  // A recommendation from the previous check may not match the new result.
  offer.hidden = true;
  for (const id of ["ip", "network", "risk", "provider"]) document.getElementById(id).textContent = "Checking…";
  status.textContent = "Requesting your browser’s current public exit IP…";
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10000);
  try {
    const response = await fetch("https://api.ipquery.io/?format=json", {
      signal: controller.signal, credentials: "omit", cache: "no-store", referrerPolicy: "no-referrer"
    });
    if (!response.ok) throw new Error(`IP service returned HTTP ${response.status}`);
    const data = await response.json();
    // Validate before displaying; never render API strings as markup.
    if (!data || typeof data.ip !== "string" || data.ip.length > 45
      || !/^[0-9a-fA-F:.]+$/.test(data.ip)) throw new Error("IP service returned invalid data");
    const info = describeNetwork(data.risk);
    document.getElementById("ip").textContent = data.ip;
    document.getElementById("network").textContent = info.network;
    document.getElementById("risk").textContent = info.risk;
    const isp = data.isp && typeof data.isp === "object" ? data.isp : {};
    document.getElementById("provider").textContent = [isp.isp || isp.org, isp.asn]
      .filter((value) => typeof value === "string" && value.length > 0).join(" · ") || "Unknown";
    status.textContent = `Checked ${new Date().toLocaleTimeString()}. Third-party signals; no guarantee of IP cleanliness or 403 avoidance.`;
    renderOffer(classify(data.risk));
  } catch (error) {
    document.getElementById("ip").textContent = "Unavailable";
    for (const id of ["network", "risk", "provider"]) document.getElementById(id).textContent = "Unknown";
    status.textContent = error.name === "AbortError" ? "IP lookup timed out. Try again."
      : `Lookup failed: ${error.message}. Try again.`;
    // No diagnosis, so no recommendation.
    offer.hidden = true;
  } finally {
    clearTimeout(timeout);
    refresh.disabled = false;
    result.setAttribute("aria-busy", "false");
  }
}

document.getElementById("cta").href = LINKS.smartproxy;
document.getElementById("benchmark").href = LINKS.benchmark;
document.getElementById("refresh").addEventListener("click", checkIP);
checkIP();
