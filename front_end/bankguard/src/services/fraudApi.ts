import { GoogleGenAI } from "@google/genai";
import { FraudResult } from "../types";

const API_BASE =
  (import.meta as any)?.env?.VITE_API_BASE_URL ?? "http://localhost:8000";


type ApiErrorPayload = {
    detail?: string;
    error?: string;
    message?: string;
  };
  

async function parseError(res: Response): Promise<string> {
    // intenta JSON
    try {
      const j = (await res.json()) as ApiErrorPayload;
      return j.detail ?? j.error ?? j.message ?? `Request failed (${res.status})`;
    } catch {
      // fallback texto plano
      try {
        const t = await res.text();
        return t || `Request failed (${res.status})`;
      } catch {
        return `Request failed (${res.status})`;
      }
    }
  }
  
  export async function scanFraudByPhone(phoneNumber: string): Promise<FraudResult> {
    console.log("🌍 scanFraudByPhone called with:", phoneNumber);
  
    const res = await fetch(`${API_BASE}/fraud/scan`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone_number: phoneNumber }),
    });
  
    console.log("📥 Raw response:", res);
  
    if (!res.ok) {
      console.log("❌ Response not OK:", res.status);
      throw new Error(`Request failed (${res.status})`);
    }
  
    const data = await res.json();
    console.log("📦 JSON received:", data);
  
    return {
      id: data.id ?? crypto.randomUUID(),
      phoneNumber: data.phoneNumber ?? phoneNumber,
      score: data.score ?? 0,
      timestamp: data.timestamp ?? Date.now(),
      ...data,
    };
  }