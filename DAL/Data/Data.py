from DAL.Model.StreamRealtimeData import StreamRealtimeData
from DAL.Repository.MockRepository import MockRepository

from Helpers import get_timestamp


class Data:
    def __init__(self):
        self.repository = MockRepository()
        self.stream_links = self.repository.get_stream_links()
        self.__stream_frames = {}
        self.__stream_counts = {}
        # TODO this needs to be initialized with the data from the database upon fresh start and if it is not present
        #  then it should be initialized with the base values
        self.__stream_realtime_data = {}  # This contains intersection_id as key and StreamRealtimeData as value
        self.__observers = []

    def get_stream_counts(self):
        return self.__stream_counts

    def set_stream_counts(self, intersection_id, count):
        self.__stream_counts[intersection_id] = count

    def set_stream_frames(self, intersection_id, frame):
        self.__stream_frames[intersection_id] = frame
        self.notify_stream_observer()

    def get_stream_frames(self):
        return self.__stream_frames

    def get_frames(self, intersection_id):
        return self.__stream_frames[intersection_id]

    def attach(self, observer):
        from DataObserver.Observer import Observer
        if isinstance(observer, Observer):
            self.__observers.append(observer)
            print(f'Attaching observer of type {type(observer)}')
        else:
            raise TypeError("observer must be an instance of Observer")

    def notify_stream_observer(self):
        from DataObserver.StreamObserver import StreamObserver
        for observer in self.__observers:
            if isinstance(observer, StreamObserver):
                observer.update()

    def notify_stream_realtime_data_observer(self, intersection_id):
        from DataObserver.RealtimeDataObserver import RealtimeDataObserver
        for observer in self.__observers:
            print(f'Checking Observer')
            if isinstance(observer, RealtimeDataObserver):
                print(f'Notifying Observer {observer}')
                observer.update(intersection_id)

    def set_stream_realtime_data(self, intersection_id: str, stream_realtime_data: StreamRealtimeData):
        self.__stream_realtime_data[intersection_id] = stream_realtime_data
        self.notify_stream_realtime_data_observer(intersection_id)

    def get_stream_realtime_data(self):
        return self.__stream_realtime_data

    def get_stream_realtime_data_by_id(self, intersection_id: str):
        return self.__stream_realtime_data[intersection_id]

    def get_stream_links(self):
        return self.stream_links
    # def get_stream_realtime_data_by_id(self, intersection_id: str):
    #     return self.__stream_realtime_data[intersection_id][list(self.__stream_realtime_data)[-1]]


"""
    stream_realtime_data = {
        'intersection_1': {
            'int(time.time() * 1000)': {,
                'signals': [
                    {
                        '_id': 'signal_1',
                        'emergency': 0,
                        'non-emergency': 0,
                        'time_since_green': 0,
                    },
                    {
                        '_id': 'signal_2',
                        'emergency': 0,
                        'non-emergency': 0,
                        'time_since_green': 0,   
                    }
                ]
                curr_green: 'signal_1',
                curr_green_duration_left: 10,
                next_green: 'signal_2',
                next_green_duration: 10,
            }
        }
    }
"""
