def get_workflow(appliance, issue):
    workflows = {
        "fan": {
            "bearing_issue": {
                "title": "Fan Bearing Problem",
                "steps": [
                    "Turn OFF power supply",
                    "Remove fan cover",
                    "Apply bearing oil or grease",
                    "Rotate shaft manually",
                    "Reassemble and test"
                ],
                "risk": "medium"
            },
            "vibration": {
                "title": "Fan Imbalance",
                "steps": [
                    "Turn OFF fan",
                    "Tighten mounting screws",
                    "Check blade alignment",
                    "Clean dust from blades"
                ],
                "risk": "low"
            }
        },

        "tv": {
            "no_signal": {
                "title": "TV No Signal",
                "steps": [
                    "Check HDMI cable connection",
                    "Select correct HDMI input",
                    "Restart TV",
                    "Restart connected device"
                ],
                "risk": "low"
            }
        },

        "mixer": {
            "motor_noise": {
                "title": "Mixer Motor Noise",
                "steps": [
                    "Unplug mixer",
                    "Open bottom panel",
                    "Check carbon brushes",
                    "Replace if worn"
                ],
                "risk": "high"
            }
        }
    }

    return workflows.get(appliance, {}).get(issue, {
        "title": "General Inspection",
        "steps": ["Consult technician if unsure"],
        "risk": "unknown"
    })
