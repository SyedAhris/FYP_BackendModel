"""
    stream_realtime_data = {
        'intersection_1': {
            'timestamp': '2021-04-01 12:00:00',
            [
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
"""
from DAL.Model.StreamRealtimeSignalData import StreamRealtimeSignalData


class StreamRealtimeData:
    def __init__(self):
        self.__intersection_id = None
        self.__timestamp = None
        # signals should be an array of type StreamRealtimeSignalData
        self.__signals = []
        self.__curr_green = None
        self.__curr_green_duration_left = None
        self.__next_green = None
        self.__next_green_duration = None

    # Setter and getter methods for intersection_id
    def set_intersection_id(self, intersection_id):
        self.__intersection_id = intersection_id

    def get_intersection_id(self):
        return self.__intersection_id

    # Setter and getter methods for timestamp
    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_timestamp(self):
        return self.__timestamp

    # Setter and getter methods for signals
    def add_signal(self, realtimestreamsignaldata : StreamRealtimeSignalData):
        self.__signals.append(realtimestreamsignaldata)

    def get_signals(self):
        return self.__signals

    # Setter and getter methods for curr_green
    def set_curr_green(self, curr_green):
        self.__curr_green = curr_green

    def get_curr_green(self):
        return self.__curr_green

    # Setter and getter methods for curr_green_duration_left
    def set_curr_green_duration_left(self, curr_green_duration_left):
        self.__curr_green_duration_left = curr_green_duration_left

    def get_curr_green_duration_left(self):
        return self.__curr_green_duration_left

    # Setter and getter methods for next_green
    def set_next_green(self, next_green):
        self.__next_green = next_green

    def get_next_green(self):
        return self.__next_green

    # Setter and getter methods for next_green_duration
    def set_next_green_duration(self, next_green_duration):
        self.__next_green_duration = next_green_duration

    def get_next_green_duration(self):
        return self.__next_green_duration

    def __str__(self):
        return f"Intersection ID: {self.__intersection_id}\nTimestamp: {self.__timestamp}\nSignals: {self.__signals}\nCurrent Green: {self.__curr_green}\nCurrent Green Duration Left: {self.__curr_green_duration_left}\nNext Green: {self.__next_green}\nNext Green Duration: {self.__next_green_duration}"

