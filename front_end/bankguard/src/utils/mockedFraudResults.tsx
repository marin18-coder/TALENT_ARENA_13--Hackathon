import { FraudResult } from "../types";

type FactorStatus = "safe" | "warning" | "danger";

function clamp(n: number, min = 0, max = 100) {
  return Math.max(min, Math.min(max, n));
}

function pickRiskLevel(score: number) {
  // Ajusta si tu RiskBadge usa otros valores (p.ej. "LOW", "MEDIUM", "HIGH")
  if (score < 30) return "low";
  if (score < 60) return "medium";
  return "high";
}

function factorStatusFromValue(v: number): FactorStatus {
  if (v < 35) return "safe";
  if (v < 70) return "warning";
  return "danger";
}

export function mockFraudResult(phoneNumber: string): FraudResult {
    const score = Math.floor(Math.random() * 100);
    const blacklist = clamp(score + (Math.random() * 20 - 10));
    const simswap = clamp(score + (Math.random() * 25 - 5));
    const factors = [{ label: "Risk index mean", value: Math.round(blacklist), status: factorStatusFromValue(blacklist) }];

    return {
        id: crypto.randomUUID(),
        phoneNumber,
        score,
        timestamp: Date.now(),
        riskLevel: pickRiskLevel(score),
        details:
        "Mock analysis: cross-referencing carrier metadata, SIM swap signals and VOIP heuristics.",
        location: "Barcelona, ES",
        carrier: "MockTel",
        deviceSwap: Math.random() < 0.25,
        locationAnomaly: Math.random() < 0.20,
        numberRecycling: Math.random() < 0.15,
        kycMatch: Math.random() < 0.75,
        factors,
        simSwapHistory: simswap >= 70,
    }
}