from DataObserver.Observer import Observer
from DAL.Repository.Firebase.firebaseRealtimeRepository import FirebaseRealtimeRepository

class RealtimeDataObserver(Observer):

    def __init__(self, subject):
        super().__init__(subject)
        self.firebase_realtime_repository = FirebaseRealtimeRepository()
        self.stream_realtime_data = self.subject.get_stream_realtime_data()

    def update(self, intersection_id):
        # print(f'RealtimeDataObserver: Updating {intersection_id}')
        self.stream_realtime_data = self.subject.get_stream_realtime_data_by_id(intersection_id)
        self.firebase_realtime_repository.push_realtime_data(intersection_id, self.stream_realtime_data.convert_to_dict())
