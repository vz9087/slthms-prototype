# SLTHMS Prototype

Smart Ladle Tracking & Health Monitoring System — Streamlit demo prototype.

Quick start
1. python -m venv venv
2. source venv/bin/activate   (Windows: venv\Scripts\activate)
3. pip install -r requirements.txt
4. streamlit run app.py

What this repo contains
- sim_engine.py — in-memory simulation engine
- ai_rules.py — deterministic AI reasoning rules
- ui.py — Streamlit UI assembly
- app.py — entrypoint
- requirements.txt — minimal deps

Demo tips
- Use "Run Simulation" then "Force L-02 Overheat" to create a visible Critical alert.
- Record a 30–60s clip showing the alert, recommendation, and alert log for sharing.

Deploy
- Upload this repo to Loveable AI as a Streamlit app. Set `app.py` as entry and include the system prompt provided earlier.

Author
- Duck (assistant)
