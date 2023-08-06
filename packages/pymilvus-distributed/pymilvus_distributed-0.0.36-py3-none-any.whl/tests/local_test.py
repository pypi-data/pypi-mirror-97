import pytest
from .utils import *


def test_insert_auto_id_false():
    milvus = Milvus()
    collection_name = gen_unique_str("test")
    dim = 8
    schema = {
        "fields": [
            {"name": "float_vector", "type": DataType.FLOAT_VECTOR,
             "params": {"dim": dim},
             "indexes": [{"metric_type": "L2"}]},
        ],
        "auto_id": False
    }
    milvus.create_collection(collection_name, schema)
    entities = [
        {
            "name": "float_vector",
            "type": DataType.FLOAT_VECTOR,
            "values": [[1 for _ in range(dim)]]
        }
    ]
    ids = milvus.bulk_insert(collection_name, entities, [1])
    print(ids[0])
    query_parm = {
        "bool": {
            "must": [
                {
                    "vector": {
                        "float_vector": {
                            "topk": 1,
                            "query": [[1 for _ in range(dim)]],
                            "params": {"nprobe": 10},
                            "metric_type": "L2"
                        }
                    }
                }
            ]
        }
    }
    res = milvus.search(collection_name, query_parm)
    print(res)
    for entity in res[0]:
        print(entity.id)
    has = milvus.has_collection(collection_name)
    print(has)
    milvus.drop_collection(collection_name)
    milvus.describe_collection


def test_insert_auto_id_true():
    milvus = Milvus()
    collection_name = gen_unique_str("test")
    dim = 8
    schema = {
        "fields": [
            {"name": "float_vector", "type": DataType.FLOAT_VECTOR,
             "params": {"dim": dim},
             "indexes": [{"metric_type": "L2"}]},
        ],
    }
    milvus.create_collection(collection_name, schema)
    entities = [
        {
            "name": "float_vector",
            "type": DataType.FLOAT_VECTOR,
            "values": [[1 for _ in range(dim)]]
        }
    ]
    ids = milvus.bulk_insert(collection_name, entities)
    print(ids[0])
    query_parm = {
        "bool": {
            "must": [
                {
                    "vector": {
                        "float_vector": {
                            "topk": 1,
                            "query": [[1 for _ in range(dim)]],
                            "params": {"nprobe": 10},
                            "metric_type": "L2"
                        }
                    }
                }
            ]
        }
    }
    res = milvus.search(collection_name, query_parm)
    print(res)
    for entity in res[0]:
        print(entity.id)