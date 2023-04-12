from DAL.Repository.MockRepository import MockRepository


class Data:
    def __init__(self):
        self.repository = MockRepository()
        self.stream_links = self.repository.get_stream_links()
        self.stream_threads = []
        self.stream_frames = {}
        self.stream_counts = {}

