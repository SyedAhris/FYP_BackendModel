import Helpers
from DAL.Data.Data import Data
from threading import Thread
import cv2

from DAL.Model.Intersection_Model import IntersectionModel
from DAL.Model.Signal_Model import SignalModel
from DAL.Model.StreamRealtimeData import StreamRealtimeData
from DAL.Model.StreamRealtimeSignalData import StreamRealtimeSignalData
from Model.Model import Model


class Streams:
    def __init__(self, data: Data):
        self.data = data
        self.model = Model()
        self.stream_threads = {}  # key is the combined_id and value is the thread
        print(self.data.stream_links)
        for intersection in self.data.stream_links:
            # First initializing some data
            assert isinstance(intersection, IntersectionModel)
            signals = {}
            intersection_id = intersection._id
            for signal in intersection.signals:
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                signals[signal_id] = StreamRealtimeSignalData(None, None, None)

            srd = StreamRealtimeData(Helpers.get_timestamp(), signals, None, None, None, None)
            self.data.set_stream_realtime_data(intersection_id, srd)

            # Creating threads
            for signal in intersection.signals:
                # Get All ids
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                combined_id = f'{intersection_id}_{signal_id}'

                # create a thread that will run the link function
                t = Thread(target=self.read_stream_link, args=(signal, combined_id,))
                self.data.set_stream_frames(combined_id, bytes())
                self.data.set_stream_counts(combined_id, [0, 0])
                # self.data.stream_counts[combined_id] = [0, 0]  # 1st index is count of non-emergency vehicles,
                # 2nd index is count of emergency vehicles
                self.stream_threads[combined_id] = t
                t.start()

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
                self.data.set_stream_counts(stream_name, count)
                # self.data.stream_counts[stream_name] = count

                # create a stream from the annotated frame

                # convert frame to JPEG format
                _, encoded_frame = cv2.imencode('.jpg', img)

                # convert JPEG-encoded frame to bytes
                bytes_frame = encoded_frame.tobytes()

                # print(bytes_frame)
                # store in the stream_frames dictionary that acts a buffer
                self.data.set_stream_frames(stream_name, bytes_frame)

            else:
                break
        cap.release()
