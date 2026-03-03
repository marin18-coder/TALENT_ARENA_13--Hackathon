export type RiskLevel = "low" | "medium" | "high" | "critical";

export type FactorStatus = "safe" | "warning" | "danger";

export interface FraudFactor {
  label: string;
  value: number; // 0..100
  status: FactorStatus;
}

export interface FraudResult {
  id: string;
  timestamp: number;
  phoneNumber: string;

  // Main score
  score: number; // 0..100
  riskLevel: RiskLevel;

  // UI content
  factors: FraudFactor[];
  details: string;
  carrier: string;
  location: string;

  // Flags used in UI checks
  isVoip: boolean;
  simSwapHistory: boolean;

  // Extra checks (optional for now)
  deviceSwap?: boolean;
  locationAnomaly?: boolean;
  numberRecycling?: boolean;
  kycMatch?: boolean;

  // Keep raw payloads for debugging / future agent scoring
  scanRaw?: any;
  locationRaw?: any;
  simSwapRaw?: any;
  deviceSwapRaw?: any;
  numberRecyclingRaw?: any;
}