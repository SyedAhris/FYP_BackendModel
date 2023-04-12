from DAL.Repository.Repository import Repository


class Data:
    def __init__(self):
        self.repository = Repository()
        self.stream_links = self.repository.get_stream_links()
        self.stream_threads = []
        self.stream_frames = {}
        self.stream_counts = {}

