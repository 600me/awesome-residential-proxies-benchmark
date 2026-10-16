"use strict";

// Stable redirects; affiliate destinations are managed on the server.
const REFERRALS = Object.freeze({
  smartproxy: "https://go.272738.xyz/smartproxy",
  brightdata: "https://go.272738.xyz/brightdata"
});

for (const [id, url] of Object.entries(REFERRALS)) {
  document.getElementById(id).href = url;
}

function describeNetwork(data) {
  const flags = data.risk && typeof data.risk === "object" ? data.risk : {};
  const network = flags.is_datacenter === true ? "Hosting / datacenter"
    : flags.is_datacenter === false ? "ISP / non-hosting candidate" : "Unknown";
  const names = { is_vpn: "VPN", is_proxy: "Proxy", is_tor: "Tor", is_datacenter: "Hosting" };
  const detected = Object.entries(names).filter(([key]) => flags[key] === true).map(([, name]) => name);
  const complete = Object.keys(names).every((key) => typeof flags[key] === "boolean");
  const score = typeof flags.risk_score === "number" && Number.isFinite(flags.risk_score)
    && flags.risk_score >= 0 && flags.risk_score <= 100 ? flags.risk_score : null;
  const risk = detected.length ? `Flagged: ${detected.join(", ")}`
    : score !== null && score > 0 ? "Risk score reported"
    : complete ? "No listed flags detected" : "Unknown / incomplete data";
  return { network, risk: risk + (score === null ? "" : ` · ${score}/100`),
    tone: detected.length || (score !== null && score > 0) ? "warning" : "neutral" };
}

async function checkIP() {
  const result = document.getElementById("result");
  const refresh = document.getElementById("refresh");
  const status = document.getElementById("status");
  refresh.disabled = true;
  result.setAttribute("aria-busy", "true");
  for (const id of ["ip", "network", "risk", "provider"]) document.getElementById(id).textContent = "Checking…";
  document.getElementById("risk").dataset.tone = "neutral";
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
    const info = describeNetwork(data);
    document.getElementById("ip").textContent = data.ip;
    document.getElementById("network").textContent = info.network;
    document.getElementById("risk").textContent = info.risk;
    document.getElementById("risk").dataset.tone = info.tone;
    const isp = data.isp && typeof data.isp === "object" ? data.isp : {};
    document.getElementById("provider").textContent = [isp.isp || isp.org, isp.asn]
      .filter((value) => typeof value === "string" && value.length > 0).join(" · ") || "Unknown";
    status.textContent = `Checked ${new Date().toLocaleTimeString()}. Third-party signals; no guarantee of IP cleanliness or 403 avoidance.`;
  } catch (error) {
    document.getElementById("ip").textContent = "Unavailable";
    for (const id of ["network", "risk", "provider"]) document.getElementById(id).textContent = "Unknown";
    status.textContent = error.name === "AbortError" ? "IP lookup timed out. Try again."
      : `Lookup failed: ${error.message}. Try again.`;
  } finally {
    clearTimeout(timeout);
    refresh.disabled = false;
    result.setAttribute("aria-busy", "false");
  }
}

document.getElementById("refresh").addEventListener("click", checkIP);
checkIP();
