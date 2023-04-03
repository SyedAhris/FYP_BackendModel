from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from WebSocketConnection import WebSocketConnection
import cv2
from Model.Model import Model


app = FastAPI()

#Initialization Phase
model = Model()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.websocket('/rtsp_stream')
async def rtsp_stream(websocket: WebSocket):
    print('Running /rtsp_stream')
    conn = WebSocketConnection(websocket)

    cap = cv2.VideoCapture('http://127.0.0.1:8080/')

    print('CV2 Video Captured')

    while True:
        # Capture frame from RTSP stream
        ret, frame = cap.read()

        if ret:
            # Run inference
            frame = model.pred_annot(frame=frame)

            # Send processed frame to WebSocket client
            await conn.send_frame(frame)

        else:
            # If frame capture fails, break the loop and close connection
            break

        # Release RTSP stream capture
    cap.release()

    # Close WebSocket connection
    await conn.websocket.close()


