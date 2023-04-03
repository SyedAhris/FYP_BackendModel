from fastapi import WebSocket
import cv2
import numpy as np

class WebSocketConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def send_frame(self, frame: np.ndarray):
        # Encode frame to JPEG format
        _, encoded_frame = cv2.imencode('.jpg', frame)

        # Convert JPEG-encoded frame to bytes
        bytes_frame = encoded_frame.tobytes()

        # Send bytes frame to WebSocket client
        await self.websocket.send_bytes(bytes_frame)