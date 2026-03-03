import React from "react";
import { History as HistoryIcon, Trash2, Clock } from "lucide-react";
import { FraudResult } from "../types";
import "./ScanHistoric.css";

interface ScanHistoricProps {
  history: FraudResult[];
  currentResultId?: string;
  onSelect: (item: FraudResult) => void;
  onClear: () => void;
}

export const ScanHistoric: React.FC<ScanHistoricProps> = ({history, currentResultId, onSelect, onClear}) => {
  return (
    <div className="scan-historic">
      <div className="scan-historic-header">
        <h3 className="scan-historic-title">
          <HistoryIcon className="scan-historic-title-icon" />
          Recent Scans
        </h3>

        {history.length > 0 && (
          <button className="scan-historic-clear" onClick={onClear} type="button">
            <Trash2 className="scan-historic-clear-icon" />
            CLEAR
          </button>
        )}
      </div>

      <div className="scan-historic-list">
        {history.length === 0 ? (
          <div className="scan-historic-empty">
            <p>No recent activity</p>
          </div>
        ) : (
          history.map((item) => {
            const isActive = currentResultId === item.id;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onSelect(item)}
                className={`scan-historic-item ${isActive ? "is-active" : ""}`}
              >
                <div className="scan-historic-left">
                  <span
                    className={`scan-historic-dot ${
                      item.score < 30
                        ? "is-low"
                        : item.score < 60
                        ? "is-medium"
                        : "is-high"
                    }`}
                  />
                  <div className="scan-historic-meta">
                    <div className="scan-historic-phone">{item.phoneNumber}</div>
                    <div className="scan-historic-time">
                      <Clock className="scan-historic-time-icon" />
                      {new Date(item.timestamp).toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </div>
                  </div>
                </div>

                <div className="scan-historic-score">SCORE: {item.score}</div>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
};