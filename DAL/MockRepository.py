from DAL.Repository import Repository
from DAL.Intersection_Model import IntersectionModel
from DAL.Signal_Model import SignalModel


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
                    SignalModel(_id='01',
                                link='http://61.211.241.239/nphMotionJpeg?Resolution=640x640&Quality=Standard')
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
