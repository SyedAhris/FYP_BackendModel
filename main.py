from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from CalculateLights.CalculateLightsObserver import CalculateLightsObserver
from DAL.Data.Data import Data
from DataObserver.RealtimeDataObserver import RealtimeDataObserver
from DataObserver.StreamObserver import StreamObserver
from Streams.Streams import Streams
from starlette.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

data = Data()
# Initialization Phase
streams = Streams(data)

rdo = RealtimeDataObserver(data)

calc_light = CalculateLightsObserver(data)

@app.get("/")
async def root():
    return {"message": "The Server is up and running"}


@app.post("/stream/notify_change")
def notify_change():
    # TODO: notify the addition or deletion in the stream links
    pass
    # loads the stream_link from mongo again
    # and then creates a new thread for each new link or remove the old ones
    # and then starts the threads


@app.get("/streams/{stream_name_input}")
async def video_feed(stream_name_input: str):
    stream_observer = StreamObserver(data, stream_name_input)
    print(f'Running /{stream_name_input}')
    return StreamingResponse(stream_observer.send_frame(stream_name_input),
                             media_type="multipart/x-mixed-replace; boundary=frame")
