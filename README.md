# 🛡️ BankGuard – AI-Driven Telecom Fraud Intelligence (Talent Arena Hackathon - TEAM 13)

BankGuard is an AI-powered anti-fraud middleware that combines verifiable telecom signals (CAMARA / Open Gateway) with real-time AI decision intelligence to detect high-risk mobile transactions.

## Overview

The fraud detection market is projected to grow from $19.5B in 2025 to $37.0B by 2030 (CAGR ≈ 13.7%).

BankGuard addresses this opportunity by merging:

+ Telecom network signals (Nokia Network-as-Code APIs)

+ Historical behavioral data (Supabase)

+ Agentic AI risk scoring

+ Real-time fraud risk evaluation

## Architecture

``` 
Frontend (React)
      ↓
Backend (Django)
      ↓
1️⃣ Nokia Telecom APIs (SIM swap, device swap, recycling, location)
2️⃣ Historical DB (Supabase)
      ↓
AI Agent (LLM scoring engine)
      ↓
Fraud Score + Risk Level + Explainability
```

## Key Features

+ SIM Swap Detection

+ Device Change Monitoring

+ Number Recycling Risk

+ Telecom-based Geolocation Signals

+ KYC Cross-Verification

+ AI Risk Scoring (0–100)

+ Explainable Fraud Factors

+ Risk Level Classification (Low / Medium / High / Critical)
 
## Tech Stack

### Frontend

React + TypeScript, Vite ,Framer Motion
### Backend

Django ,Nokia Network-as-Code APIs, Supabase (PostgreSQL), OpenAI / Google AI (Agent scoring)


 ## Running the Project

### Frontend
```
cd front_end
npm install
npm run dev
```

### Backend
```
cd back_end
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py runserver
```
