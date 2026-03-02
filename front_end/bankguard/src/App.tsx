import { useState } from "react";

import UpperBar from "./components/ui/UpperBar";
import InputTelephone from "./components/InputTelephone";
import "./App.css";


export default function App() {
  const [phoneNumber, setPhoneNumber] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handlePhoneChange = (e: React.ChangeEvent<HTMLInputElement>) => {setPhoneNumber(e.target.value)};

  const handleScan = (e: React.FormEvent) => {
    e.preventDefault();

    if (phoneNumber.length < 8) {
      setError("Enter a valid phone number");
      return;
    }

    setError(null);
    setIsAnalyzing(true);

    setTimeout(() => {
      setIsAnalyzing(false);
    }, 1500);
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
          </div>


          {/* RIGHT SIDE */}
          <div />
        </div>
      </main>
    </div>
  );
}





