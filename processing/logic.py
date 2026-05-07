EMERGENCY_CLASSES = [
    "ambulance",
    "police",
    "pompier",
    "fire truck",
    "fire_truck",
    "firetruck"
]


class DecisionSystem:

    def __init__(self):
        self.last_alert = False

    def check(self, detections):

        """
        detections:
        [
            ("ambulance", 0.91),
            ("police", 0.77)
        ]
        """

        for name, conf in detections:

            try:

                name = str(name).lower().strip()

                if name in EMERGENCY_CLASSES and conf >= 0.30:
                    self.last_alert = True
                    return True

            except Exception as e:
                print("LOGIC ERROR:", e)

        self.last_alert = False
        return False