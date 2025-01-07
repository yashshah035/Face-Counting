from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
import mediapipe as mp
import asyncio

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount a static directory for serving the frontend
# app.mount("/static", StaticFiles(directory="frontend/build"), name="static")

face_detection = mp.solutions.face_detection.FaceDetection(0.4)

async def detect_faces(frame):
    height, width, _ = frame.shape
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(imgRGB)
    count = 0

    if result.detections:
        for detection in result.detections:
            box = detection.location_data.relative_bounding_box
            x, y, w, h = int(box.xmin * width), int(box.ymin * height), int(box.width * width), int(box.height * height)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, str(round(detection.score[0] * 100, 2)), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            count += 1

    return count, frame

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            count, processed_frame = await detect_faces(frame)
            _, buffer = cv2.imencode('.jpg', processed_frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)