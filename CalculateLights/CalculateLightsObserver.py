from threading import Thread

import Helpers
from DAL.Model.Intersection_Model import IntersectionModel
from DAL.Model.Signal_Model import SignalModel
from DAL.Model.StreamRealtimeData import StreamRealtimeData
from DAL.Model.StreamRealtimeSignalData import StreamRealtimeSignalData
from DataObserver.Observer import Observer


class CalculateLightsObserver(Observer):
    def __init__(self, subject):
        super().__init__(subject)
        self.stream_counts = self.subject.get_stream_counts()
        self.realtime_data = self.subject.get_stream_realtime_data()
        self.stream_links = self.subject.get_stream_links()
        self.calculate_lights_threads = {}
        for intersection in self.stream_links:
            assert isinstance(intersection, IntersectionModel)
            intersection_id = intersection._id
            t = Thread(target=self.calculate_lights, args=(intersection,))
            self.calculate_lights_threads[intersection_id] = t
            t.start()


    def update(self):
        # TODO URGENT: Implement this
        self.stream_counts = self.subject.get_stream_counts()
        self.realtime_data = self.subject.get_stream_realtime_data()

    def calculate_lights(self, intersection: IntersectionModel):
        while True:

            # example counts =  [[1, 0], [2, 0], [3, 0], [4, 0]]
            counts = []

            last_data: StreamRealtimeData = self.realtime_data[intersection._id]
            signal_realtime_signals = None
            for signal in intersection.signals:
                assert isinstance(signal, SignalModel)
                signal_id = signal._id
                intersection_id = intersection._id
                combined_id = f'{intersection_id}_{signal_id}'
                signal_realtime_signals = last_data.get_signals()
                signal_realtime: StreamRealtimeSignalData = signal_realtime_signals[signal_id]
                signal_realtime.set__emergency(self.stream_counts[combined_id][0])
                signal_realtime.set__non_emergency(self.stream_counts[combined_id][1])
                signal_realtime.set__time_since_green(
                    (Helpers.get_timestamp() - last_data.get_timestamp()) + signal_realtime.get__time_since_green())
                if signal_id == last_data.get_curr_green():
                    signal_realtime.set__time_since_green(0)
                signal_realtime_signals[signal_id] = signal_realtime

            # update the last data for current time and curr count

            last_data.set_timestamp(Helpers.get_timestamp())
            last_data.set_signals(signal_realtime_signals)
            last_data.set_curr_green_duration_left(
                last_data.get_curr_green_duration_left() - (Helpers.get_timestamp() - last_data.get_timestamp()))
            if last_data.get_curr_green_duration_left() <= 0:
                last_data.set_curr_green_duration_left(last_data.get_next_green_duration())
                last_data.set_curr_green(last_data.get_next_green())
                last_data.set_next_green_duration(-1)  # -1 means not set
                last_data.set_next_green(-1)  # -1 means not set

            if last_data.get_next_green_duration() <= 5:  # when 5s left figure our next green and duration
                next_green = -1
                next_green_duration = -1

                if (last_data.get_next_green() == -1):
                    pass
                    # TODO: @Ibrahim algo for next green and duration

                last_data.set_next_green(next_green)
                last_data.set_next_green_duration(next_green_duration)

            self.subject.set_stream_realtime_data(intersection._id, last_data)


            # TODO send the traffic light color to the signals
