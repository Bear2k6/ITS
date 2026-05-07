from fastapi import FastAPI, UploadFile
import cv2, numpy as np
from inference.detector import detect

app = FastAPI()

@app.post("/detect")
async def detect_api(file: UploadFile):
    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

    detections = detect(img)

    return {
        "detections": [
            {"label": d[0], "conf": float(d[1])}
            for d in detections
        ]
    }