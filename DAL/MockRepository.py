from DAL.Repository import Repository


class MockRepository(Repository):
    def get_stream_links(self) -> list:
        return [{
            '_id': 117512546,
            'link': 'http://61.211.241.239/nphMotionJpeg?Resolution=320x240&Quality=Standard'
            # 'link': 'http://127.0.0.1:8080/117512546'
        }]
