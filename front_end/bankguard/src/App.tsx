import { useEffect, useMemo, useState } from "react";
import UpperBar from "./components/ui/UpperBar";
import InputTelephone from "./components/InputTelephone";
import { ScanHistoric } from "./components/ScanHistoric";
import AnalyzeUserScore from "./components/AnalyzeScore";
import "./App.css";
import { FraudResult } from "./types";
import { scanFraudByPhone } from "./services/fraudApi";

export default function App() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const [history, setHistory] = useState<FraudResult[]>([]);
  const [selected, setSelected] = useState<FraudResult | null>(null);
  const [result, setResult] = useState<FraudResult | null>(null);

  const [analysisStep, setAnalysisStep] = useState(0);

  const steps = useMemo(
    () => [
      "Verifying carrier metadata...",
      "Checking global blacklist databases...",
      "Analyzing SIM swap history...",
      "Detecting VOIP/Virtual number patterns...",
      "Calculating behavioral risk score...",
    ],
    []
  );

  // Load history from localStorage once
  useEffect(() => {
    const saved = localStorage.getItem("fraud_history");
    if (!saved) return;
    try {
      const parsed: FraudResult[] = JSON.parse(saved);
      setHistory(parsed);
    } catch (e) {
      console.error("Failed to parse fraud_history", e);
    }
  }, []);

  // Persist history
  useEffect(() => {
    localStorage.setItem("fraud_history", JSON.stringify(history));
  }, [history]);

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPhoneNumber(e.target.value);
    if (error) setError(null);
  };

  const handleScan = async (e: React.FormEvent) => {
    console.log("🚀 handleScan triggered");
    e.preventDefault();

    const normalized = phoneNumber.trim();
    const digitsLen = normalized.replace(/[^\d]/g, "").length;
    console.log("📞 Phone entered:", normalized);
    console.log("🔢 Digits length:", digitsLen);
  
    if (digitsLen < 8) {
      setError("Enter a valid phone number");
      return;
    }
    console.log("✅ Validation passed");

    setError(null);
    setIsAnalyzing(true);
    setResult(null);
    setAnalysisStep(0);

    // UX step simulation
    const stepInterval = window.setInterval(() => {
      setAnalysisStep((prev) => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 600);

    try {
      console.log("📡 Calling backend...");
      const newResult = await scanFraudByPhone(normalized);
      console.log("✅ Backend responded:", newResult);

      setSelected(newResult);
      setResult(newResult);
      setHistory((prev) => [newResult, ...prev].slice(0, 10));
    } catch (err: any) {
      setError(err?.message ?? "Unexpected error");
    } finally {
      window.clearInterval(stepInterval);
      setIsAnalyzing(false);
    }
  };

  const clearHistory = () => {
    if (window.confirm("Are you sure you want to clear your scan history?")) {
      setHistory([]);
      setSelected(null);
      setResult(null);
    }
  };

  // When user selects an old scan from history, show it on the right panel
  const handleSelectFromHistory = (item: FraudResult) => {
    setSelected(item);
    setResult(item);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <UpperBar />

      <main className="app-main">
        <div className="app-grid">
          <div className="app-body-left">
            <h1 className="app-body-title">
              Advanced <span className="app-body-highlight">Fraud</span>{" "}
              Intelligence.
            </h1>

            <p className="app-body-description">
              Protect your platform with instant risk scoring for any mobile
              number worldwide.
            </p>

            <div className="app-body-telephone">
              <InputTelephone
                phoneNumber={phoneNumber}
                error={error}
                isAnalyzing={isAnalyzing}
                onChange={handlePhoneChange}
                onSubmit={handleScan}
              />
            </div>

            <div className="app-body-history">
              <ScanHistoric
                history={history}
                currentResultId={selected?.id}
                onSelect={handleSelectFromHistory}
                onClear={clearHistory}
              />
            </div>
          </div>

          {/* RIGHT SIDE */}
          <div className="app-body-right">
            <AnalyzeUserScore
              isAnalyzing={isAnalyzing}
              analysisStep={analysisStep}
              steps={steps}
              result={result}
            />
          </div>
        </div>
      </main>
    </div>
  );
}