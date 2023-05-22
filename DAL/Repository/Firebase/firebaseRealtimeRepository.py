import DAL.Repository.Firebase.config as cf
import pyrebase


class FirebaseRealtimeRepository:
    def __init__(self):
        config = cf.get_config()
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()

    def push_realtime_data(self, intersection_id, data_dict):
        print(data_dict)
        print(f'Pushing data to Firebase for intersection {intersection_id}')
        self.db.child("realtime_data").child(intersection_id).push(data_dict)
