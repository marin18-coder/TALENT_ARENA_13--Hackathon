import React from "react";
import { Shield, Activity } from "lucide-react";
import "./UpperBar.css";

const UpperBar: React.FC = () => {
  return (
    <header className="upperbar">
      
      {/* LEFT */}
      <div className="upperbar-left">
        <Shield className="upperbar-logo" />
        <span className="upperbar-title">BankGuard</span>
      </div>

      {/* RIGHT */}
      <div className="upperbar-right">
        <Activity className="upperbar-status-icon" />
        <span>Secure Session</span>
      </div>

    </header>
  );
};

export default UpperBar;