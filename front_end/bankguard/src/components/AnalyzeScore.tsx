import React from "react";
import { AnimatePresence } from "framer-motion";
import { Lock, Shield } from "lucide-react";
import { FraudResult } from "../types";
import { AnalysisLoading } from "./AnalysisLoading";
import { ScanResult } from "./ScanResult";

import "./AnalyzeScore.css";

type AnalyzeUserScore = {
  isAnalyzing: boolean;
  analysisStep: number;
  steps: string[];
  result: FraudResult | null;  
};

const AnalyzeUserScore: React.FC<AnalyzeUserScore> = ({isAnalyzing, analysisStep, steps, result}) => {
  return (
    <div className="analyze-score">
      <AnimatePresence mode="wait">
        {isAnalyzing ? (
          <AnalysisLoading analysisStep={analysisStep} steps={steps} />
        ) : result ? (
          <ScanResult result={result} />
        ) : (
          <div className="analyze-score-card">
            <div className="analyze-score-accent" />

            <div className="analyze-score-icon-wrapper">
              <Shield className="analyze-score-icon" />
            </div>

            <h2 className="analyze-score-title">
              Ready for Verification
            </h2>

            <p className="analyze-score-description">
              Enter a mobile number to begin the fraud analysis and risk scoring
              process.
            </p>

            <div className="analyze-score-security">
              <Lock className="analyze-score-security-icon" />
            </div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AnalyzeUserScore;