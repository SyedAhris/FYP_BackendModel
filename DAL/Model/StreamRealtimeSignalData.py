class StreamRealtimeSignalData:
    def __init__(self):
        # self.__signal_id = None
        self.__emergency = None
        self.__non_emergency = None
        self.__time_since_green = None

    def __init__(self, emergency, non_emergency, time_since_green):
        # self.__signal_id = None
        self.__emergency = emergency
        self.__non_emergency = non_emergency
        self.__time_since_green = time_since_green

    # def set__signal_id(self, signal_id):
    #     self.__signal_id = signal_id
    #
    # def get__signal_id(self):
    #     return self.__signal_id

    def set__emergency(self, emergency):
        self.__emergency = emergency

    def get__emergency(self):
        return self.__emergency

    def set__non_emergency(self, non_emergency):
        self.__non_emergency = non_emergency

    def get__non_emergency(self):
        return self.__non_emergency

    def set__time_since_green(self, time_since_green):
        self.__time_since_green = time_since_green

    def get__time_since_green(self):
        return self.__time_since_green

    def convert_to_dict(self):
        return {
            # 'signal_id': self.__signal_id,
            'emergency': self.__emergency,
            'non_emergency': self.__non_emergency,
            'time_since_green': self.__time_since_green
        }

    def __str__(self):
        return f"Signal ID: {self.__signal_id}\nEmergency: {self.__emergency}\nNon-Emergency: {self.__non_emergency}\nTime Since Green: {self.__time_since_green}"

