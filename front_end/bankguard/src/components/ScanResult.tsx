import React from "react";
import { motion } from "framer-motion";
import { Globe, Activity, CheckCircle2, AlertCircle, Zap, History as HistoryIcon,
Smartphone, MapPin, RefreshCcw, UserCheck} from "lucide-react";
import { FraudResult } from "../types";
import { GaugeChart } from "./ui/GaugeChart";
import { RiskBadge } from "./ui/RiskBadge";
import "./ScanResult.css";

interface ScanResultProps {
  result: FraudResult;
}

export const ScanResult: React.FC<ScanResultProps> = ({ result}) => {
  const factors = result.factors ?? [];

  const checks = [
    {
      title: "SIM Swap Detection",
      subtitle: "Checks for recent carrier porting",
      icon: Zap,
      flag: !!result.simSwapHistory,
      goodLabel: "Stable",
      badLabel: "High Activity",
      badTone: "bad" as const,
    },
    {
      title: "Device Swap Detection",
      subtitle: "Detects sudden device changes",
      icon: Smartphone,
      flag: !!(result as any).deviceSwap, 
      goodLabel: "Stable",
      badLabel: "Detected",
      badTone: "warn" as const,
    },
    {
      title: "Location Anomaly",
      subtitle: "Checks improbable geo changes",
      icon: MapPin,
      flag: !!(result as any).locationAnomaly,
      goodLabel: "Stable",
      badLabel: "High location Variance",
      badTone: "warn" as const,
    },
    {
      title: "Number Recycling",
      subtitle: "Detects recently high rate of recycled numbers",
      icon: RefreshCcw,
      flag: !!(result as any).numberRecycling,
      goodLabel: "Stable",
      badLabel: "High Recycling Activity",
      badTone: "warn" as const,
    },
    {
      title: "KYC Match",
      subtitle: "Matches identity and account signals",
      icon: UserCheck,
      invert: true,
      flag: !!(result as any).kycMatch,
      goodLabel: "Match",
      badLabel: "No Match",
      badTone: "bad" as const,
    },
  ];

  return (
    <motion.div
      key="result"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="scan-result"
    >
      {/* Main Score Card */}
      <div className="scan-result-card">
        <div className="scan-result-id">ID: {result.id.slice(0, 8)}</div>

        <div className="scan-result-card-row">
          <GaugeChart score={result.score} />

          <div className="scan-result-card-content">
            <div className="scan-result-headline-block">
              <RiskBadge level={(result as any).riskLevel ?? "low"} />
              <h2>Analysis Complete</h2>
            </div>

            <p className="scan-result-quote">
              "{(result as any).details ?? "Mock analysis completed successfully."}"
            </p>

            <div className="scan-result-meta">
              <div className="scan-result-pill">
                <Globe className="scan-result-pill-icon" />
                {(result as any).location ?? "Unknown"}
              </div>

              <div className="scan-result-pill">
                <Activity className="scan-result-pill-icon" />
                {(result as any).carrier ?? "Unknown"}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Factors + Trend */}
      <div className="scan-result-mid">
        <div className="scan-result-mid-left">
          <div className="scan-result-grid">
            {factors.map((factor, i) => {
              const status =
                factor.status === "safe"
                  ? "safe"
                  : factor.status === "warning"
                  ? "warning"
                  : "danger";

              return (
                <div key={i} className="scan-result-factor">
                  <div className="scan-result-factor-header">
                    <span className="scan-result-factor-label">{factor.label}</span>

                    {factor.status === "safe" ? (
                      <CheckCircle2 className="scan-result-status-icon safe" />
                    ) : (
                      <AlertCircle className="scan-result-status-icon warning" />
                    )}
                  </div>

                  <div className="scan-result-value">{factor.value}%</div>

                  <div className="scan-result-bar">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${factor.value}%` }}
                      transition={{ duration: 1, delay: 0.2 }}
                      className={`scan-result-bar-fill ${status}`}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Advanced Security Checks */}
      <div className="scan-result-advanced">
        <h3 className="scan-result-advanced-title">
          <HistoryIcon className="scan-result-advanced-title-icon" />
          Advanced Security Checks
        </h3>

        <div className="scan-result-checks">
          {checks.map((c, idx) => {
            const Icon = c.icon;
            const isGood = c.invert ? c.flag : !c.flag;
            const badgeClass = isGood ? "good" : c.badTone;
            const badgeText = isGood ? c.goodLabel : c.badLabel;

            return (
              <div key={idx} className="scan-result-check">
                <div className="scan-result-check-left">
                  <div className="scan-result-check-icon-box">
                    <Icon className="scan-result-check-icon" />
                  </div>
                  <div>
                    <p className="scan-result-check-title">{c.title}</p>
                    <p className="scan-result-check-subtitle">{c.subtitle}</p>
                  </div>
                </div>

                <div className={`scan-result-badge ${badgeClass}`}>{badgeText}</div>
              </div>
            );
          })}
        </div>
      </div>
    </motion.div>
  );
};