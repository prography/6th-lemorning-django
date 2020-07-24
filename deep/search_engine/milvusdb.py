import os
import numpy as np

from milvus import Milvus, IndexType, MetricType, Status


class SearchEngine:
    def __init__(self, host, port):
        self.host = os.environ.get('MILVUS_HOST', host)
        self.port = os.environ.get('MILVUS_PORT', str(port))
        self.engine = Milvus(host=self.host, port=self.port)
        self.collection_name = None

#################################################
# HANDLE COLLECTION
#################################################

    def create_collection(self, collection_name, dimension):
        # collection 생성

        param = {'collection_name': collection_name,
                 'dimension': dimension,
                 'index_file_size': 1000,
                 'metric_type': MetricType.IP}

        self.engine.create_collection(param)

        print('[INFO] collection {}을 생성했습니다.'.format(collection_name))

    def drop_collection(self, collection_name):
        # collection 삭제

        self.engine.drop_collection(collection_name=collection_name)

        print('[INFO] collection {}을 삭제했습니다.'.format(collection_name))

    def get_collection_stats(self, collection_name):
        # collection 정보 출력

        print(self.engine.get_collection_info(collection_name))
        print(self.engine.get_collection_stats(collection_name))

    def set_collection(self, collection_name):
        # 쿼리 조작을 하기 위한 collection 지정

        self.collection_name = collection_name
        print('[INFO] setting collection {}'.format(self.collection_name))

#################################################
# UTILS
#################################################
    def check_set_collection(self):
        # 쿼리 조작을 위한 collection 지정이 되어있는 지 체크

        assert self.collection_name is not None, '[ERROR] collection을 setting해 주십시오!!'

    def check_exist_data_by_key(self, key):
        # collection에 정해진 key가 존재하는 지 확인

        self.check_set_collection()

        _, vector = self.engine.get_entity_by_id(
            collection_name=self.collection_name, ids=key)

        vector = vector if vector else [vector]

        return True if vector[0] else False

    def convert_key_format(self, key):
        return [key] if isinstance(key, int) else key

    def convert_value_format(self, value):
        rank = len(value.shape)

        assert rank < 2, '[ERROR] value의 dim을 2 미만으로 입력해 주세요!!'
        return value.reshape(1, -1) if rank == 1 else value

#################################################
# INSERT
#################################################

    def insert_data(self, key, value):
        # 데이터를 collection에 입력

        key = self.convert_key_format(key)
        value = self.convert_value_format(value)

        if self.check_exist_data_by_key(key):
            print("[ERROR] 이미 collection에 데이터가 존재합니다.")
            return

        self.engine.insert(
            collection_name=self.collection_name, records=value, ids=key)
        self.engine.flush([self.collection_name])

        print('[INFO] insert key {}'.format(key))

#################################################
# DELELTE
#################################################

    def delete_data(self, key):
        # 데이터를 collection에서 제거

        key = self.convert_key_format(key)

        if not self.check_exist_data_by_key(key):
            print("[ERROR] collection에 데이터가 존재하지 않습니다.")
            return

        self.engine.delete_entity_by_id(self.collection_name, key)
        self.engine.flush([self.collection_name])

        print('[INFO] delete key {}'.format(key))


#################################################
# UPDATE
#################################################

    def update_data(self, key, value):
        # 데이터를 업데이트

        key = self.convert_key_format(key)
        value = self.convert_value_format(value)

        if not self.check_exist_data_by_key(key):
            print("[ERROR] collection에 데이터가 존재하지 않습니다.")
            return

        self.engine.delete_entity_by_id(self.collection_name, key)
        self.engine.flush([self.collection_name])

        self.engine.insert(
            collection_name=self.collection_name, records=value, ids=key)
        self.engine.flush([self.collection_name])

        print('[INFO] update key {}'.format(key))

#################################################
# SEARCH
#################################################

    def search_by_feature(self, feature, top_k):
        # feature를 이용해서 데이터를 검색

        self.check_set_collection()

        feature = self.convert_value_format(feature)

        _, result = self.engine.search(
            collection_name=self.collection_name, query_records=feature, top_k=top_k)

        li_id = [list(map(lambda x: x.id, result[0]))
                 for i in range(len(result))]
        li_dist = [list(map(lambda x: x.distance, result[0]))
                   for i in range(len(result))]

        return li_id, li_dist

    def search_by_key(self, key, top_k):
        # key를 이용해서 데이터를 검색

        self.check_set_collection()
        key = self.convert_key_format(key)

        if not self.check_exist_data_by_key(key):
            print("[ERROR] collection에 데이터가 존재하지 않습니다.")
            return

        _, vector = self.engine.get_entity_by_id(
            collection_name=self.collection_name, ids=key)
        _, result = self.engine.search(
            collection_name=self.collection_name, query_records=vector, top_k=top_k+1)

        li_id = [list(map(lambda x: x.id, result[0][1:]))
                 for i in range(len(result))]
        li_dist = [list(map(lambda x: x.distance, result[0][1:]))
                   for i in range(len(result))]

        return li_id, li_dist