from fastapi import FastAPI

from Streams.Streams import Streams
from starlette.responses import StreamingResponse

app = FastAPI()

# Initialization Phase
streams = Streams()


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
    print(f'Running /{stream_name_input}')
    return StreamingResponse(streams.send_frame(stream_name_input),
                             media_type="multipart/x-mixed-replace; boundary=frame")
