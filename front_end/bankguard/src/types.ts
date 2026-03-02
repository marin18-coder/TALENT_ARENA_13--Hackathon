export interface FraudFactor {
  label: string;
  value: number;
  status: 'safe' | 'warning' | 'danger';
}

export interface FraudResult {
  id: string;
  timestamp: number;
  phoneNumber: string;
  score: number;
  riskLevel: 'Low' | 'Medium' | 'High' | 'Critical';
  factors: FraudFactor[];
  details: string;
  carrier: string;
  location: string;
  isVoip: boolean;
  simSwapHistory: boolean;
}
