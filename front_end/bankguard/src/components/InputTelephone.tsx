import React from "react";
import { Phone, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";
import "./InputTelephone.css";

type InputTelephoneProps = {
  phoneNumber: string;
  error: string | null;
  isAnalyzing: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
};

const InputTelephone: React.FC<InputTelephoneProps> = ({phoneNumber, error, isAnalyzing, onChange, onSubmit}) => {
  return (
    <div className="telephone">
      <form onSubmit={onSubmit} className="telephone-form">
        <div className="telephone-field">
          <label className="telephone-label">
            Mobile Number
          </label>

          <div className="telephone-wrapper">
            <Phone className="telephone-icon" />

            <input
              type="tel"
              value={phoneNumber}
              onChange={onChange}
              placeholder="+1 555 000 0000"
              className="telephone-input"
            />
          </div>

          {error && (
            <motion.p
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="telephone-error"
            >
              <AlertCircle size={14} />
              {error}
            </motion.p>
          )}
        </div>

        <button
          disabled={isAnalyzing}
          className="telephone-button"
        >
          {isAnalyzing ? "Processing..." : "Run Fraud Scan"}
        </button>
      </form>
    </div>
  );
};

export default InputTelephone;