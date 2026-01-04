def generate_actions(analysis):
    if "vibration" in " ".join(analysis.get("issues", [])):
        return {
            "overlay_type": "AR-guidance",
            "steps": [
                "🔩 Tighten mounting screws",
                "⚖️ Balance rotating parts",
                "🧰 Inspect bearings"
            ]
        }

    return {
        "overlay_type": "AR-guidance",
        "steps": ["✅ No action required"]
    }
