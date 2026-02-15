import numpy as np

def predict_risk(missed_week, late_count):
    """
    Simple AI-like risk predictor
    """
    score = (missed_week * 0.6) + (late_count * 0.4)

    if score < 1:
        return "LOW"
    elif score < 3:
        return "MEDIUM"
    else:
        return "HIGH"
