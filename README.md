# BioMon — Whole Body Monitoring System

A web-based biometric monitoring dashboard with role-based access control,
real-time charts, and a fake data layer ready to replace with live sensors.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Full frontend dashboard (open directly in browser) |
| `server.py` | Python/Flask REST API backend |
| `data_generator.cpp` | C++ fake sensor data engine → outputs JSON |

## Quick Start

### Frontend only (no server needed)
Just open `index.html` in any browser. Fake data runs entirely in JavaScript.

### With Python backend
```bash
pip install flask flask-cors
python server.py
# API available at http://localhost:5000
```
Then in `index.html`, replace the `genSummary()` / `genTimeline()` / `genECG()`
calls with `fetch('/api/summary')` etc.

### C++ data generator
```bash
g++ -o data_generator data_generator.cpp -std=c++17
./data_generator > biometric_data.json
```

## Role Access Matrix

| Metric | Athlete | Doctor | Trainer | Coach |
|--------|:-------:|:------:|:-------:|:-----:|
| Steps | ✅ | ✅ | ✅ | ✅ |
| Calories | ✅ | ✅ | ✅ | ✅ |
| Active Minutes | ✅ | ✅ | ✅ | ✅ |
| Heart Rate | ✅ | ✅ | ✅ | ✅ |
| Energy Score | ✅ | ✅ | ✅ | ✅ |
| Readiness | ✅ | ✅ | ✅ | ✅ |
| Blood Oxygen (SpO2) | ✅ | ✅ | ✅ | ❌ |
| Stress Level | ✅ | ✅ | ✅ | ❌ |
| Blood Pressure | ✅ | ✅ | ✅ | ❌ |
| Sleep Stages | ✅ | ✅ | ✅ | ❌ |
| Sleep Apnea | ✅ | ✅ | ✅ | ❌ |
| Body Composition | ✅ | ✅ | ✅ | ❌ |
| ECG | ✅ | ✅ | ❌ | ❌ |
| Menstrual Cycle | ✅ | ✅ | ❌ | ❌ |
| Antioxidant Index | ✅ | ✅ | ❌ | ❌ |

## Replacing Fake Data

All fake data is isolated in clearly marked functions:
- **JS**: `genSummary()`, `genTimeline()`, `genECG()` in `index.html`
- **Python**: `generate_summary()`, `generate_hourly_timeline()`, `generate_ecg_waveform()` in `server.py`
- **C++**: `generate_day_data()` in `data_generator.cpp`
