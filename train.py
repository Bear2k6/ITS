from ultralytics import YOLO

# 1. Khởi tạo mô hình YOLOv
model = YOLO('yolov8n.pt')

# 2. Chạy lệnh train
results = model.train(
    data='data.yaml',   
    epochs=100,         
    imgsz=640,          
    device=0,          
    name='priority_vehicle_model' 
)
