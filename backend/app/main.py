from fastapi import FastAPI, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import numpy as np
from ultralytics import YOLO
import time
from pydantic import BaseModel
from Adafruit_IO import Client, Data, Feed

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

adafruit_username = None
adafruit_key = None
feed_name = None

class AdafruitCredentials(BaseModel):
    username: str
    key: str
    feedName: str

templates = Jinja2Templates(directory="/code/app/templates")

# Load YOLO model
model = YOLO("/code/app/best.pt")  # Chọn YOLOv8 phiên bản nhỏ

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@app.post("/connect_adafruit")
async def connect_adafruit(credentials: AdafruitCredentials):
    global adafruit_username, adafruit_key, feed_name
    adafruit_username = credentials.username
    adafruit_key = credentials.key
    feed_name = credentials.feedName
    return {"message": "Connected to Adafruit IO"}

@app.post("/upload_frame")
async def upload_frame(file: UploadFile):
    global adafruit_username, adafruit_key, feed_name

    if not adafruit_username or not adafruit_key or not feed_name:
        return {"error": "Adafruit IO credentials not set"}

    # Đọc dữ liệu hình ảnh
    image_data = await file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Dùng YOLO để phát hiện đối tượng trên frame
    results = model(frame)
    logs = []
    # Connect to Adafruit IO and send logs
    aio = Client(adafruit_username, adafruit_key)
    for result in results:
        for box in result.boxes:
            # Vẽ các bounding boxes
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw box
            label = f"{int(box.cls)} {float(box.conf):.2f}"  # Chuyển sang int và float
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            aio.send_data(feed_name, f"Fire: ({x1}, {y1}) ({x2}, {y2})")

    time.sleep(3)
    return {"message": "Frame processed and logs sent to Adafruit IO"}