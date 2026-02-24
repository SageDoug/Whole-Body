#!/usr/bin/env python3
"""
BioMon Python Server
====================
Run: pip install flask flask-cors && python server.py
Replace the generate_* functions with real DB queries or sensor API calls.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import math, random, time
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

MENSTRUAL_PHASES = {0:"N/A", 1:"Menstrual", 2:"Follicular", 3:"Ovulation", 4:"Luteal"}

def sine(t, period, amp, offset=0):
    return offset + amp * math.sin(2 * math.pi * t / period)

def rnd(lo, hi):
    return lo + random.random() * (hi - lo)

# ============================================================
# FAKE DATA — replace these with real sensor / DB calls
# ============================================================

def generate_hourly_timeline(days=7):
    records = []
    now = datetime.now()
    base = now - timedelta(days=days)
    random.seed(42)  # remove seed for real randomness

    steps_cum = calories_cum = active_min_cum = 0

    for hour in range(days * 24):
        ts = base + timedelta(hours=hour)
        h  = ts.hour
        is_sleep = h >= 22 or h < 6

        step_rate = 0
        if 6 <= h <= 22:
            step_rate = max(0, int(sine(h - 6, 16, 600, 800) + rnd(-200, 200)))
        steps_cum    += step_rate
        calories_cum += step_rate * 0.05 + rnd(40, 70)
        if step_rate > 300:
            active_min_cum += 60

        hr_base = 58 if is_sleep else 75
        hr  = max(45, min(185, int(hr_base + sine(h, 24, 8) + rnd(-5, 5) + step_rate * 0.001)))
        spo2 = round(rnd(95.0, 97.5) if is_sleep else rnd(97.0, 100.0), 1)

        stress_base = 45 if 9 <= h <= 17 else 25
        stress = max(0, min(100, int(stress_base + rnd(-15, 25))))

        sbp = max(90,  min(180, int(120 + rnd(-10, 15))))
        dbp = max(60,  min(120, int(80  + rnd(-5,  10))))

        cycle_day = ts.day % 28
        if cycle_day < 5:    phase = 1
        elif cycle_day < 13: phase = 2
        elif cycle_day < 16: phase = 3
        else:                phase = 4

        energy = max(0, min(100, int(70 + rnd(-20, 20) - stress * 0.2 + (spo2 - 97) * 5)))

        records.append({
            "timestamp":      ts.isoformat(),
            "hour":           h,
            "day":            ts.strftime("%a %b %d"),
            "steps":          steps_cum,
            "calories":       round(calories_cum, 1),
            "active_minutes": active_min_cum,
            "heart_rate":     hr,
            "spo2":           spo2,
            "stress":         stress,
            "sbp":            sbp,
            "dbp":            dbp,
            "menstrual_phase":  phase,
            "menstrual_label":  MENSTRUAL_PHASES[phase],
            "body_fat":       round(18.5 + rnd(-0.3, 0.3), 1),
            "muscle_kg":      round(42.0 + rnd(-0.2, 0.2), 1),
            "bmi":            round(22.4 + rnd(-0.1, 0.1), 1),
            "sleep_deep":     round(rnd(1.0, 2.0) if is_sleep else 0, 2),
            "sleep_light":    round(rnd(3.0, 4.0) if is_sleep else 0, 2),
            "sleep_rem":      round(rnd(1.5, 2.5) if is_sleep else 0, 2),
            "apnea_events":   random.randint(0, 8) if is_sleep else 0,
            "energy":         energy,
            "antioxidant":    random.randint(40, 75),
            "fall_detected":  random.random() < 0.001,
        })

    return records


def generate_ecg_waveform(beats=5):
    """Synthetic PQRST ECG waveform."""
    points = []
    for _ in range(beats):
        for i in range(200):
            p = i / 200
            v = 0.0
            if   p < 0.10: v =  0.05 * math.sin(math.pi * p / 0.10)
            elif p < 0.15: v = -0.10 * math.sin(math.pi * (p - 0.10) / 0.05)
            elif p < 0.20: v =  1.20 * math.sin(math.pi * (p - 0.15) / 0.05)
            elif p < 0.25: v = -0.20 * math.sin(math.pi * (p - 0.20) / 0.05)
            elif p < 0.45: v =  0.30 * math.sin(math.pi * (p - 0.25) / 0.20)
            v += random.uniform(-0.015, 0.015)
            points.append(round(v, 4))
    return points


def generate_summary():
    random.seed(int(time.time() / 3600))  # changes hourly
    phases = {0:"N/A",1:"Menstrual",2:"Follicular",3:"Ovulation",4:"Luteal"}
    cycle_day = datetime.now().day % 28
    phase_idx = 1 if cycle_day < 5 else 2 if cycle_day < 13 else 3 if cycle_day < 16 else 4
    return {
        "steps_today":      random.randint(6500, 12000),
        "calories_today":   random.randint(1800, 2800),
        "active_minutes":   random.randint(30,  90),
        "avg_hr":           random.randint(68,  78),
        "resting_hr":       random.randint(55,  65),
        "spo2_avg":         round(rnd(97.5, 99.5), 1),
        "stress_avg":       random.randint(30,  55),
        "sbp":              random.randint(115, 128),
        "dbp":              random.randint(75,  85),
        "energy_score":     random.randint(60,  90),
        "antioxidant":      random.randint(45,  70),
        "body_fat":         round(18.5 + rnd(-0.5, 0.5), 1),
        "muscle_kg":        round(42.0 + rnd(-0.5, 0.5), 1),
        "bmi":              round(22.4 + rnd(-0.2, 0.2), 1),
        "sleep_total":      round(rnd(6.5, 8.5), 1),
        "sleep_deep":       round(rnd(1.2, 1.8), 1),
        "sleep_light":      round(rnd(3.0, 4.0), 1),
        "sleep_rem":        round(rnd(1.5, 2.5), 1),
        "apnea_events":     random.randint(0, 6),
        "menstrual_phase":  phases[phase_idx],
        "fall_events_today":0,
        "readiness":        random.randint(70, 95),
    }

# ============================================================
# API Routes
# ============================================================

@app.route("/api/summary")
def api_summary():
    return jsonify(generate_summary())

@app.route("/api/timeline")
def api_timeline():
    days = int(request.args.get("days", 7))
    return jsonify(generate_hourly_timeline(days))

@app.route("/api/ecg")
def api_ecg():
    beats = int(request.args.get("beats", 8))
    return jsonify({"waveform": generate_ecg_waveform(beats)})

@app.route("/api/athlete/<athlete_id>")
def api_athlete(athlete_id):
    return jsonify({"id": athlete_id, "name": f"Athlete #{athlete_id}", "summary": generate_summary()})

@app.route("/")
def index():
    return "BioMon API running on port 5000. Open index.html in your browser."

if __name__ == "__main__":
    print("BioMon server → http://localhost:5000")
    app.run(debug=True, port=5000, host="0.0.0.0")
