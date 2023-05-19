
class Observer:
    def __init__(self, subject):
        from DAL.Data.Data import Data
        if isinstance(subject, Data):
            self.subject = subject
            print(self)
            self.subject.attach(self)
        else:
            raise TypeError("subject must be an instance of Data")

    def update(self):
        pass

    def update(self, intersection_id):
        pass
