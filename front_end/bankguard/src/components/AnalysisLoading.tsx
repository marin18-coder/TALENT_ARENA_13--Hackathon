import React from "react";
import { motion } from "framer-motion";
import { Activity } from "lucide-react";
import "./AnalysisLoading.css";

interface AnalysisLoadingProps {
  analysisStep: number;
  steps: string[];
}

export const AnalysisLoading: React.FC<AnalysisLoadingProps> = ({
  analysisStep,
  steps,
}) => {
  return (
    <motion.div
      key="loading"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="analysis-loading"
    >
      <div className="analysis-loading-icon-wrapper">
        <div className="analysis-loading-ring" />

        <div className="analysis-loading-icon-center">
          <Activity className="analysis-loading-icon" />
        </div>
      </div>

      <h2 className="analysis-loading-title">
        Analyzing Risk Vectors
      </h2>

      <p className="analysis-loading-description">
        Cross-referencing global databases and carrier metadata.
      </p>

      <div className="analysis-loading-steps">
        {steps.map((step, i) => {
          const state =
            i < analysisStep
              ? "done"
              : i === analysisStep
              ? "active"
              : "pending";

          return (
            <div key={i} className="analysis-loading-step">
              <div className={`analysis-loading-dot ${state}`} />
              <span className={`analysis-loading-text ${state}`}>
                {step}
              </span>
            </div>
          );
        })}
      </div>
    </motion.div>
  );
};