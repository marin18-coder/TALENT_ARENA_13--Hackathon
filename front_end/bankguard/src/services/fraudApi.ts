import { FraudFactor, FraudResult } from "../types";

const API_BASE =
  (import.meta as any)?.env?.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

// ----------------------------
// Types
// ----------------------------

type ApiErrorPayload = {
  detail?: string;
  error?: string;
  message?: string;
};

export type NokiaFullScanResponse = {
  ok?: boolean;
  phoneNumber?: string;
  error?: string;
  scan?: {
    simSwap?: { swapped?: boolean };
    simSwapDate?: { latestSimChange?: string };

    deviceSwap?: { swapped?: boolean };
    deviceSwapDate?: { latestDeviceChange?: string };

    numberRecycling?: { phoneNumberRecycled?: boolean };

    location?: {
      lastLocationTime?: string;
      area?: {
        areaType?: string;
        radius?: number;
        center?: { latitude?: number; longitude?: number };
      };
    };

    // Future (agent-provided)
    score?: number;
    riskLevel?: "low" | "medium" | "high" | "critical";
    factors?: FraudFactor[];
    details?: string;
    carrier?: string;
    locationName?: string;

    // Optional future flags
    isVoip?: boolean;
    locationAnomaly?: boolean;
    kycMatch?: boolean;

    // Optional ids/timestamps if backend adds them
    id?: string;
    timestamp?: number;
  };
};

// ----------------------------
// Helpers
// ----------------------------

async function parseError(res: Response): Promise<string> {
  try {
    const j = (await res.json()) as ApiErrorPayload;
    return j.detail ?? j.error ?? j.message ?? `Request failed (${res.status})`;
  } catch {
    try {
      const t = await res.text();
      return t || `Request failed (${res.status})`;
    } catch {
      return `Request failed (${res.status})`;
    }
  }
}

function deriveRiskLevel(score: number): FraudResult["riskLevel"] {
  if (score < 30) return "low";
  if (score < 60) return "medium";
  if (score < 85) return "high";
  return "critical";
}

function defaultFactors(flags: {
  simSwap: boolean;
  deviceSwap: boolean;
  numberRecycling: boolean;
}): FraudFactor[] {
  return [
    {
      label: "SIM Swap Risk",
      value: flags.simSwap ? 85 : 10,
      status: flags.simSwap ? "danger" : "safe",
    },
    {
      label: "Device Swap Risk",
      value: flags.deviceSwap ? 75 : 10,
      status: flags.deviceSwap ? "warning" : "safe",
    },
    {
      label: "Number Recycling Risk",
      value: flags.numberRecycling ? 65 : 10,
      status: flags.numberRecycling ? "warning" : "safe",
    },
  ];
}

function formatLocation(scan: NokiaFullScanResponse["scan"]): string {
  if (typeof scan?.locationName === "string" && scan.locationName.trim()) {
    return scan.locationName;
  }

  const lat = scan?.location?.area?.center?.latitude;
  const lng = scan?.location?.area?.center?.longitude;

  if (typeof lat === "number" && typeof lng === "number") {
    return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  }

  return "Unknown";
}

/**
 * Convert Nokia "full-scan" response into a UI-friendly FraudResult.
 * Defensive mapping: always returns safe fields so UI never crashes.
 * NOTE: score/riskLevel are mocked until agent scoring is enabled.
 */
export function mapNokiaScanToFraudResult(
  phoneNumber: string,
  res: NokiaFullScanResponse
): FraudResult {
  const scan = res.scan ?? {};

  const simSwapHistory = !!scan.simSwap?.swapped;
  const deviceSwap = !!scan.deviceSwap?.swapped;
  const numberRecycling = !!scan.numberRecycling?.phoneNumberRecycled;

  const score =
    typeof scan.score === "number" ? scan.score : Math.floor(Math.random() * 100);

  const riskLevel = scan.riskLevel ?? deriveRiskLevel(score);

  const factors = Array.isArray(scan.factors)
    ? scan.factors
    : defaultFactors({ simSwap: simSwapHistory, deviceSwap, numberRecycling });

  return {
    id: scan.id ?? crypto.randomUUID(),
    phoneNumber: res.phoneNumber ?? phoneNumber,
    score,
    timestamp: scan.timestamp ?? Date.now(),

    riskLevel,
    factors,

    details:
      scan.details ??
      "Signals collected from Nokia Network-as-Code. Agent scoring not enabled yet.",

    carrier: scan.carrier ?? "Unknown",
    location: formatLocation(scan),

    // Flags used by your Advanced Security Checks UI
    isVoip: !!scan.isVoip,
    simSwapHistory,
    deviceSwap,
    locationAnomaly: !!scan.locationAnomaly,
    numberRecycling,
    kycMatch: typeof scan.kycMatch === "boolean" ? scan.kycMatch : true,

    // Raw payloads (useful for debugging + agent pipeline later)
    scanRaw: scan,
    locationRaw: scan.location,
    simSwapRaw: scan.simSwap,
    deviceSwapRaw: scan.deviceSwap,
    numberRecyclingRaw: scan.numberRecycling,
  } as FraudResult;
}

// ----------------------------
// API
// ----------------------------

/**
 * 1) Call backend to retrieve Nokia signals (full-scan).
 * 2) Map to FraudResult with safe fallbacks.
 * 3) (Later) send result.scanRaw to your agent backend.
 */
export async function scanFraudByPhone(phoneNumber: string): Promise<FraudResult> {
  const res = await fetch(`${API_BASE}/api/nokia/full-scan/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phoneNumber }),
  });

  if (!res.ok) throw new Error(await parseError(res));

  const data = (await res.json()) as NokiaFullScanResponse;

  if (data.ok === false) {
    throw new Error(data.error ?? "Scan failed");
  }

  return mapNokiaScanToFraudResult(phoneNumber, data);
}

/**
 * Agent backend (stub for now).
 * Later: POST /api/agent/score/ with { phoneNumber, scan: <raw_nokia_scan> }.
 */
export async function scoreWithAgent(_: {
  phoneNumber: string;
  scan: unknown;
}): Promise<Partial<FraudResult>> {
  return { details: "Agent scoring not enabled yet (stub)." };
}