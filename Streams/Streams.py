from DAL.Repository.MockRepository import MockRepository
from threading import Thread
import cv2

from DAL.Model.Intersection_Model import IntersectionModel
from DAL.Model.Signal_Model import SignalModel
from Model.Model import Model

class Streams:
    def __init__(self):
        self.repository = MockRepository()
        self.stream_links = self.repository.get_stream_links()
        self.stream_threads = []
        self.stream_frames = {}
        self.model = Model()
        # TODO@ahirs : configure for each intersection not for each stream
        for intersection in self.stream_links:
            assert isinstance(intersection, IntersectionModel)
            for signal in intersection.signals:
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                intersection_id = intersection._id
                combined_id = f'{intersection_id}_{signal_id}'
                # create a thread that will run the link function
                t = Thread(target=self.read_stream_link, args=(signal, combined_id, ))
                self.stream_frames[combined_id] = bytes()
                self.stream_threads.append(t)
                t.start()

    def add_stream_link(self, link: str):
        self.stream_links.append(link)

    def read_stream_link(self, signal: SignalModel, combined_id: str):
        cap = cv2.VideoCapture(signal.link)
        # split_link = link.split('/')
        stream_name = combined_id
        print(f'Streaming {stream_name}...')

        while True:
            ret, frame = cap.read()
            if ret:
                pred = self.model.pred_annot(frame=frame)
                img = pred[1]  # returns an annotated frame back
                count = pred[0]  # returns the count of the vehicles

                # TODO: using count of each traffic signal in intersection use an algorithm to determine the traffic
                #  light color

                # create a stream from the annotated frame

                # convert frame to JPEG format
                _, encoded_frame = cv2.imencode('.jpg', img)

                # convert JPEG-encoded frame to bytes
                bytes_frame = encoded_frame.tobytes()

                # print(bytes_frame)
                # store in the stream_frames dictionary that acts a buffer
                self.stream_frames[stream_name] = bytes_frame

            else:
                break
        cap.release()

    def send_frame(self, stream_name):
        while True:
            frame_bytes = self.stream_frames[stream_name]
            # print(self.stream_frames[stream_name])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
