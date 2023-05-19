# import Helpers
# from DAL.Model.Intersection_Model import IntersectionModel
# from DAL.Model.Signal_Model import SignalModel
# from DAL.Model.StreamRealtimeData import StreamRealtimeData
# from DAL.Model.StreamRealtimeSignalData import StreamRealtimeSignalData
# from DataObserver.Observer import Observer
#
#
# class CalculateLightsObserver(Observer):
#     def __init__(self, subject):
#         super().__init__(subject)
#         self.stream_counts = self.subject.get_stream_counts()
#         self.realtime_data = self.subject.get_stream_realtime_data()
#
#     def update(self):
#         # TODO URGENT: Implement this
#         self.stream_counts = self.subject.get_stream_counts()
#         self.realtime_data = self.subject.get_stream_realtime_data()
#
#     def calculate_lights(self, intersection: IntersectionModel):
#         while True:
#
#             # example counts =  [[1, 0], [2, 0], [3, 0], [4, 0]]
#             counts = []
#
#             last_data : StreamRealtimeData = self.realtime_data(intersection._id)
#
#             for signal in intersection.signals:
#                 assert isinstance(signal, SignalModel)
#                 signal_id = signal._id
#                 intersection_id = intersection._id
#                 combined_id = f'{intersection_id}_{signal_id}'
#                 signals = last_data.get_signals()
#                 signal_realtime : StreamRealtimeSignalData = [signal for signal in signals if signal['_id'] == signal_id]
#                 signal_realtime.set__emergency(self.stream_counts[combined_id][0])
#                 signal_realtime.set__non_emergency(self.stream_counts[combined_id][1])
#                 signal_realtime.set__time_since_green(Helpers.get_curr_time()+signal_realtime.get__time_since_green())
#
#             # get the last data for the intersection from the dict
#
#
#             # update the last data for current time and curr count
#             for signals in last_data.get_signals():
#
#                 if signals['_id'] == signal[0]:
#                     signals['non-emergency'] = signal[1]
#                     signals['emergency'] = signal[2]
#                     # current time + time since green
#                     signals['time_since_green'] = signals['time_since_green'] + Helpers.get_curr_time()
#
#
#             # do the calculations for light
#             # update the last data for next time and next count
#             # update the dict
#             # send the light to the signals
#             # send data to the database
#
#             # print(f'id: {intersection._id} counts: {counts}')
#
#             # TODO create an algorithm that will calculate the traffic light color based on the counts of each signal
#             #   @Irtiza check this out take help from GPT too and also the methods that I sent you
#
#
#             # TODO send the traffic light color to the signals