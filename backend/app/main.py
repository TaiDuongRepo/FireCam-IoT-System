from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from ultralytics import YOLO

app = FastAPI()

# CORS để hỗ trợ client
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="/code/app/templates")

# Load YOLO model
model = YOLO("yolov8n.pt")  # Chọn YOLOv8 phiên bản nhỏ

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/upload_frame")
async def upload_frame(file: UploadFile):
    # Đọc dữ liệu hình ảnh
    image_data = await file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Dùng YOLO để phát hiện đối tượng trên frame
    results = model(frame)
    for result in results:
        for box in result.boxes:
            # Vẽ các bounding boxes
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw box
            label = f"{int(box.cls)} {float(box.conf):.2f}"  # Chuyển sang int và float
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return {"message": "Frame processed"}