import { useState, useEffect } from "react";

import UpperBar from "./components/ui/UpperBar";
import InputTelephone from "./components/InputTelephone";
import { ScanHistoric } from "./components/ScanHistoric";

import "./App.css";
import { FraudResult } from "./types";

export default function App() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);


  const [history, setHistory] = useState<FraudResult[]>([]);
  const [selected, setSelected] = useState<FraudResult | null>(null);

  // Load history from localStorage once
  useEffect(() => {
    const saved = localStorage.getItem("fraud_history");
    if (!saved) return;
    try {
      setHistory(JSON.parse(saved));
    } catch (e) {
      console.error("Failed to parse fraud_history", e);
    }
  }, []);
  

  // Persist history
  useEffect(() => {
    localStorage.setItem("fraud_history", JSON.stringify(history));
  }, [history]);

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {setPhoneNumber(e.target.value)};

  const handleScan = (e: React.FormEvent) => {
    e.preventDefault();

    if (phoneNumber.replace(/[^\d+]/g, "").length < 8) {
      setError("Enter a valid phone number");
      return;
    }

    setError(null);
    setIsAnalyzing(true);

    // Fake scan result for now (replace later with real API call)
    const newResult: FraudResult = {
      id: crypto.randomUUID(),
      phoneNumber,
      score: Math.floor(Math.random() * 100),
      timestamp: Date.now(),
    } as FraudResult;

    setTimeout(() => {
      setIsAnalyzing(false);
      setSelected(newResult);
      setHistory((prev) => [newResult, ...prev].slice(0, 10));
    }, 900);
  };

  const clearHistory = () => {
    if (window.confirm("Are you sure you want to clear your scan history?")) {
      setHistory([]);
      setSelected(null);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <UpperBar />

      <main className="app-main">
        <div className="app-grid">

          {/* LEFT SIDE */}
          <div className="app-body-left">
            <h1 className="app-body-title">
              Advanced <span className="app-body-highlight">Fraud</span> Intelligence.
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
                onSelect={setSelected}
                onClear={clearHistory}
              />
            </div>

          </div>
          {/* RIGHT SIDE */}
          <div/>
        </div>
      </main>
    </div>
  );
}





