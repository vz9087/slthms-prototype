# Deterministic AI rules & analysis helpers
def analyze_ladle_snapshot(ladle):
    temp = ladle["temperature"]
    stress = ladle["stress"]
    vib = ladle["vibration"]
    issues = []
    if temp > 1600:
        issues.append("Overheating")
    elif 1580 <= temp <= 1600:
        issues.append("Temp Approaching Limit")
    if stress > 80:
        issues.append("High Stress (crack risk)")
    elif 75 <= stress <= 80:
        issues.append("Stress Approaching Limit")
    if vib > 0.7:
        issues.append("Vibration Anomaly")
    elif 0.6 <= vib <= 0.7:
        issues.append("Vibration Approaching Limit")
    status = "Normal"
    if any(i in ["Overheating", "High Stress (crack risk)", "Vibration Anomaly"] for i in issues):
        status = "Critical"
    elif len(issues) > 0:
        status = "Warning"
    if status == "Normal":
        rec = "Normal operation — continue monitoring."
    else:
        parts = []
        if "Overheating" in issues:
            parts.append("Immediate cooling required")
        if "High Stress (crack risk)" in issues:
            parts.append("Inspect refractory lining / route to maintenance")
        if "Vibration Anomaly" in issues:
            parts.append("Check structural balance and mounting")
        if any("Approaching" in s for s in issues):
            parts.append("Increase monitoring frequency")
        rec = " + ".join(parts)
    explanation = f"Issues detected: {', '.join(issues) if issues else 'None'}. Status: {status}."
    return {"status": status, "recommendation": rec, "explanation": explanation}
