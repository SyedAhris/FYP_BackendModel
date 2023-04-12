from DAL.Model.Signal_Model import SignalModel


class IntersectionModel:
    def __init__(self, _id: str, signals: list):
        self._id = _id
        self.signals = signals

