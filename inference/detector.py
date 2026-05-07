import os
from ultralytics import YOLO

# ======================================================
# PATH
# ======================================================
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

# ======================================================
# AUTO LOAD MODEL
# ======================================================
MODEL = None

MODEL_LIST = [
    "best.pt",
    "yolov8n.pt"
]

for model_name in MODEL_LIST:

    model_path = os.path.join(MODELS_DIR, model_name)

    if os.path.exists(model_path):

        print(f"[INFO] USING MODEL: {model_path}")

        MODEL = YOLO(model_path)

        break

if MODEL is None:
    raise FileNotFoundError(
        "No model found in project/models/"
    )

# ======================================================
# DETECT
# ======================================================
def detect(frame):

    detections = []

    try:

        results = MODEL(frame, verbose=False)[0]

        for box in results.boxes:

            cls_id = int(box.cls[0])

            conf = float(box.conf[0])

            label = MODEL.names[cls_id]

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            detections.append(
                (
                    label,
                    conf,
                    (x1, y1, x2, y2)
                )
            )

    except Exception as e:

        print("DETECT ERROR:", e)

    return detections