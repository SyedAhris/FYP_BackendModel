from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect
from WebSocketConnection import WebSocketConnection
from starlette.responses import StreamingResponse
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

    cap = cv2.VideoCapture('http://46.16.226.181:88/?action=stream')

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

def generate_frames(): #used by http stream
    # Set up RTSP stream capture
    #cap = cv2.VideoCapture('http://46.16.226.181:88/?action=stream')
    # cap = cv2.VideoCapture('http://pendelcam.kip.uni-heidelberg.de/mjpg/video.mjpg')
    cap = cv2.VideoCapture('http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard')
    # cap = cv2.VideoCapture('http://127.0.0.1:8080/')

    while True:
        # Capture frame from RTSP stream
        ret, frame = cap.read()

        if ret:
            # Run inference
            #TODO: Model should return an annotated stream
            img = model.pred_annot(frame=frame)


            #TODO: Convert annoateed frames to a http stream sendable format

            # # Convert frame to JPEG format
            # _, encoded_frame = cv2.imencode('.jpg', img)
            #
            # # Convert JPEG-encoded frame to bytes
            # bytes_frame = encoded_frame.tobytes()
            # return bytes_frame

            # Yield bytes frame to HTTP client
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + bytes_frame + b'\r\n')

        else:
            # If frame capture fails, break the loop and release resources
            cap.release()
            break


# Define HTTP stream route
@app.get('/http_stream/')
async def http_stream():
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')