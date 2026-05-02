from ultralytics import YOLO

# 1. Khởi tạo mô hình YOLOv8 (dùng file weight bạn đang có)
model = YOLO('yolov8n.pt')

# 2. Chạy lệnh train
# Bạn có thể điều chỉnh các thông số này theo ý muốn
results = model.train(
    data='data.yaml',   # File cấu hình dataset của bạn
    epochs=100,         # Số vòng lặp train
    imgsz=640,          # Kích thước hình ảnh
    device=0,           # Chạy bằng GPU (nếu máy có GPU)
    name='priority_vehicle_model' # Tên thư mục lưu kết quả
)