def generate_actions(detection):
    if detection["issue"] == "loose_screw":
        return {
            "overlay_type": "arrow",
            "x": detection["x"],
            "y": detection["y"],
            "text": "Tighten this screw"
        }

    if detection["issue"] == "burnt_capacitor":
        return {
            "overlay_type": "circle",
            "x": detection["x"],
            "y": detection["y"],
            "text": "Replace capacitor"
        }

    return {
        "overlay_type": "none",
        "text": "No action required"
    }
