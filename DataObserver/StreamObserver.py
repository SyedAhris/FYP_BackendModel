from DataObserver.Observer import Observer


class StreamObserver(Observer):
    def __init__(self, subject, intersection_id):
        super().__init__(subject)
        self.intersection_id = intersection_id
        self.frames = self.subject.get_frames(self.intersection_id)

    def update(self):
        self.frames = self.subject.get_frames(self.intersection_id)
    def send_frame(self, stream_name):
        while True:
            frame_bytes = self.frames
            # print(self.stream_frames[stream_name])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
