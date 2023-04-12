class IntersectionModel:
    def __init__(self, _id: str, signals: list):
        self._id = _id
        self.signals = signals


class SignalModel:
    def __init__(self, _id: str, link: str):
        self._id = _id
        self.link = link
        self.curr_count = 0

    @property
    def id(self):
        return self._id