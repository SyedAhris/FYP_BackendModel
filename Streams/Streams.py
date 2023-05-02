from DAL.Data.Data import Data
from DAL.Repository.MockRepository import MockRepository
from threading import Thread
import cv2

from DAL.Model.Intersection_Model import IntersectionModel
from DAL.Model.Signal_Model import SignalModel
from Model.Model import Model


class Streams:
    def __init__(self):
        self.data = Data()
        self.model = Model()
        print(self.data.stream_links)
        for intersection in self.data.stream_links:
            assert isinstance(intersection, IntersectionModel)
            print(intersection)
            for signal in intersection.signals:
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                intersection_id = intersection._id
                combined_id = f'{intersection_id}_{signal_id}'
                # create a thread that will run the link function
                t = Thread(target=self.read_stream_link, args=(signal, combined_id,))
                self.data.stream_frames[combined_id] = bytes()
                self.data.stream_counts[combined_id] = [0, 0]  # 1st index is count of non-emergency vehicles,
                # 2nd index is count of emergency vehicles
                self.data.stream_threads.append(t)
                t.start()

            t = Thread(target=self.calculate_lights, args=(intersection,))
            t.start()

    def calculate_lights(self, intersection: IntersectionModel):
        while True:

            # example counts =  [[1, 0], [2, 0], [3, 0], [4, 0]]
            counts = []

            for signal in intersection.signals:
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                intersection_id = intersection._id
                combined_id = f'{intersection_id}_{signal_id}'
                counts.append(self.data.stream_counts[combined_id])

            # print(f'id: {intersection._id} counts: {counts}')

            # TODO create an algorithm that will calculate the traffic light color based on the counts of each signal
            #   @Irtiza check this out take help from GPT too and also the methods that I sent you


            # TODO send the traffic light color to the signals

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
                self.data.stream_counts[stream_name] = count

                # create a stream from the annotated frame

                # convert frame to JPEG format
                _, encoded_frame = cv2.imencode('.jpg', img)

                # convert JPEG-encoded frame to bytes
                bytes_frame = encoded_frame.tobytes()

                # print(bytes_frame)
                # store in the stream_frames dictionary that acts a buffer
                self.data.stream_frames[stream_name] = bytes_frame

            else:
                break
        cap.release()

    def send_frame(self, stream_name):
        while True:
            frame_bytes = self.data.stream_frames[stream_name]
            # print(self.stream_frames[stream_name])
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
