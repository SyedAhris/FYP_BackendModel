from DAL.Repository.Repository import Repository
from DAL.Model.Intersection_Model import IntersectionModel
from DAL.Model.Signal_Model import SignalModel


class MockRepository(Repository):
    def get_stream_links(self) -> list:
        # return [{
        #     '_id': 'intersection_1',
        #     'signals': {
        #         '_id': '01',
        #         'link': 'http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard'
        #         # 'link': 'http://127.0.0.1:8080/117512546'
        #     },
        # },
        # {
        #     '_id': 'intersection_1',
        #     'signals': {
        #         '_id': '02',
        #         'link': 'http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard'
        #         # 'link': 'http://127.0.0.1:8080/117512546'
        #     },
        # }]
        return [
            IntersectionModel(
                _id='intersection_1',
                signals=[
                    SignalModel(_id='signal_1',
                                #link='http://61.211.241.239/nphMotionJpeg?Resolution=640x640&Quality=Standard'
                                #link='http://100.120.50.250:5000'
#                                 link='https://vlc.ahris.ninja/01'
                                link='http://192.168.0.100:8002/01'
                                ),
                    SignalModel(_id='signal_2',
                                # link='http://61.211.241.239/nphMotionJpeg?Resolution=640x640&Quality=Standard'
                                # link='http://100.120.50.250:5000'
#                                 link='https://vlc.ahris.ninja/02'
                                link='http://192.168.0.100:8002/02'
                                )
                ]
            ),
            # IntersectionModel(
            #     _id='intersection_2',
            #     signals=[
            #         SignalModel(_id='01',
            #                     link='http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard')
            #     ]
            # )
        ]
