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

    #function to find the next green light
    def findNextGreen(self, last_data):
        #prioritize green light to signal with most emergency vehicles
        next_green = -1
        maximum_emergency_vehicles = 0
        signal_with_maximum_emergency_vehicles = -1
        for key, value in last_data.get_signals().items():
            print(f"keys {key}")
            if (last_data.get_curr_green() == key): continue   #continue if checking same signal
            if(value.get__emergency() > maximum_emergency_vehicles):
                maximum_emergency_vehicles = value.get__emergency()
                signal_with_maximum_emergency_vehicles = key
            print(f"maximum_emergency_vehicles {maximum_emergency_vehicles}")
            print(f"emergency {value.get__emergency()}")
            print(f"non emergency {value.get__non_emergency()}")
        if(maximum_emergency_vehicles > 0 and signal_with_maximum_emergency_vehicles != -1):
            next_green = signal_with_maximum_emergency_vehicles
            print(f"next green due to emergency vehicles {signal_with_maximum_emergency_vehicles}")
        
        #otherwise go to signal with largest wait cost
        if(next_green == -1):
            maximum_wait_cost = 0
            signal_with_maximum_wait_cost = -1
            #calculate wait costs for each signal and find signal with largest wait cost
            for key, value in last_data.get_signals().items():
                if (last_data.get_curr_green() == key): continue
                wait_cost = (value.get__time_since_green() ** 1.2)  * value.get__non_emergency()
                if(wait_cost > maximum_wait_cost):
                    maximum_wait_cost = wait_cost
                    signal_with_maximum_wait_cost = key
            if(maximum_wait_cost > 0 and signal_with_maximum_wait_cost != -1):
                next_green = signal_with_maximum_wait_cost
                print(f"next green due to wait cost {signal_with_maximum_wait_cost}")
        return next_green

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
                print(f"emergency: {signal_realtime.get__emergency()}")
                print(f"non emergency: {signal_realtime.get__non_emergency()}")
                signal_realtime.set__time_since_green(
                    (Helpers.get_timestamp() - last_data.get_timestamp()) + signal_realtime.get__time_since_green())
                # print(f"signal_realtime.get__time_since_green(): {signal_realtime.get__time_since_green()}")
                # print(f"interval correct: {Helpers.get_timestamp() - last_data.get_timestamp()}")
                if signal_id == last_data.get_curr_green():
                    signal_realtime.set__time_since_green(0)
                signal_realtime_signals[signal_id] = signal_realtime

            # update the last data for current time and curr count

            last_data.set_signals(signal_realtime_signals)
            last_data.set_curr_green_duration_left(
                last_data.get_curr_green_duration_left() - (Helpers.get_timestamp() - last_data.get_timestamp()))
            print(f"last_data_curr_green_duration_left: {last_data.get_curr_green_duration_left()}")
            # print(f"interval {Helpers.get_timestamp() - last_data.get_timestamp()}")
            print(f"signal id {last_data.get_curr_green()}")
            last_data.set_timestamp(Helpers.get_timestamp())
            if last_data.get_curr_green_duration_left() <= 0:
                last_data.set_curr_green_duration_left(last_data.get_next_green_duration())
                last_data.set_curr_green(last_data.get_next_green())
                last_data.set_next_green_duration(-1)  # -1 means not set
                last_data.set_next_green(-1)  # -1 means not set
            if last_data.get_next_green_duration() <= 5:  # when 5s left figure our next green and duration
                next_green = -1
                next_green_duration = -1

                if (last_data.get_next_green() == -1):
                    # pass
                    # TODO: @Ibrahim algo for next green and duration
                    # next_green = 1
                    # last_data.set_next_green(func("some data"))
                    #reset the max emergency vehicles count
                    next_green = self.findNextGreen(last_data) 
                    if(next_green != -1):
                        print("not 1")
                        max_throughput = 0.7  #max volume of cars that can pass a signal per second
                        #set next green duration to the number of total vehicles in that signal divided by the number of vehicles that can pass through in 1 second
                        next_green_duration = (last_data.get_signals()[next_green].get__emergency() + last_data.get_signals()[next_green].get__non_emergency()) / max_throughput
                        print(f"next green duration {next_green_duration}")


                last_data.set_next_green(next_green)
                last_data.set_next_green_duration(next_green_duration)

            self.subject.set_stream_realtime_data(intersection._id, last_data)


            # TODO send the traffic light color to the signals