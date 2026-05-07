import os
import shutil
import torch
from ultralytics import YOLO

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(BASE, "data.yaml")
RUNS = os.path.join(BASE, "runs")
MODELS = os.path.join(BASE, "models")

os.makedirs(MODELS, exist_ok=True)

device = 0 if torch.cuda.is_available() else "cpu"

model = YOLO("yolov8n.pt")

model.train(
    data=DATA,
    epochs=50,
    imgsz=640,
    batch=2 if device == "cpu" else 8,
    device=device,
    project=RUNS,
    name="train",
    workers=0
)

# copy best.pt
for root, _, files in os.walk(RUNS):
    if "best.pt" in files:
        shutil.copy(os.path.join(root, "best.pt"),
                    os.path.join(MODELS, "best.pt"))
        print("MODEL READY")