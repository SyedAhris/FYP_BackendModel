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
        # self.__intersection_id = None
        self.__timestamp = None
        # signals should be an array of type StreamRealtimeSignalData
        self.__signals = {}
        self.__curr_green = None  # contains current green signal's ID
        self.__curr_green_duration_left = None
        self.__next_green = None  # contains next green signal's ID
        self.__next_green_duration = None

    def __init__(self, timestamp, signals, curr_green, curr_green_duration_left, next_green, next_green_duration):
        # self.__intersection_id = intersection_id
        self.__timestamp = timestamp
        self.__signals = signals
        self.__curr_green = curr_green
        self.__curr_green_duration_left = curr_green_duration_left
        self.__next_green = next_green
        self.__next_green_duration = next_green_duration

    # Setter and getter methods for intersection_id
    # def set_intersection_id(self, intersection_id):
    #     self.__intersection_id = intersection_id
    #
    # def get_intersection_id(self):
    #     return self.__intersection_id

    # Setter and getter methods for timestamp
    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_timestamp(self):
        return self.__timestamp

    # Setter and getter methods for signals
    def set_signal(self, id: str, emergency: int, non_emergency: int, time_since_green: int):
        self.__signals[id] = StreamRealtimeSignalData(emergency, non_emergency, time_since_green)

    def set_signals(self, signals):
        self.__signals = signals

    def get_signals(self):
        return self.__signals

    def get_signal_by_id(self, id: str):
        return self.__signals[id]

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

    def convert_to_dict(self):
        return {
            # 'intersection_id': self.__intersection_id,
            'timestamp': self.__timestamp,
            'signals': self.get_signals_dict(),
            'curr_green': self.__curr_green,
            'curr_green_duration_left': self.__curr_green_duration_left,
            'next_green': self.__next_green,
            'next_green_duration': self.__next_green_duration
        }

    def get_signals_dict(self):
        signals_dict = {}
        for signal_id in self.__signals:
            signals_dict[signal_id] = self.__signals[signal_id].convert_to_dict()
        return signals_dict

    def __str__(self):
        return f"Timestamp: {self.__timestamp}\nSignals: {self.__signals}\nCurrent Green: {self.__curr_green}\nCurrent Green Duration Left: {self.__curr_green_duration_left}\nNext Green: {self.__next_green}\nNext Green Duration: {self.__next_green_duration}"
