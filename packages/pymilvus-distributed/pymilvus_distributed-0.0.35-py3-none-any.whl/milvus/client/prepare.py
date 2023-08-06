import abc
import copy
import struct
import ujson

from .exceptions import ParamError

from ..grpc_gen import milvus_pb2 as grpc_types

# for milvus-distributed
from ..grpc_gen import common_pb2 as common_types
from ..grpc_gen import schema_pb2 as schema_types
from ..grpc_gen import milvus_pb2 as milvus_types

from . import blob

from .types import RangeType, DataType, MetricType, IndexType


class Prepare:

    @classmethod
    def create_collection_request(cls, collection_name, fields):
        """
        :type param: dict
        :param param: (Required)

            ` {"fields": [
                    {"field": "A", "type": DataType.INT32}
                    {"field": "B", "type": DataType.INT64},
                    {"field": "C", "type": DataType.FLOAT},
                    {"field": "Vec", "type": DataType.FLOAT_VECTOR,
                     "params": {"dim": 128}}
                ],
            "auto_id": True}`

        :return: ttypes.TableSchema object
        """

        if not isinstance(fields, dict):
            raise ParamError("Param fields must be a dict")

        if "fields" not in fields:
            raise ParamError("Param fields must contains key 'fields'")

        schema = schema_types.CollectionSchema(name=collection_name)

        auto_id = fields.get('auto_id', True)
        schema.autoID = auto_id

        if not auto_id:
            field_schema = schema_types.FieldSchema()

            field_schema.name = "_id"
            field_schema.is_primary_key = True
            field_schema.description = "this is _id field"
            field_schema.data_type = DataType.INT64
            schema.fields.append(field_schema)

        for fk, fv in fields.items():
            if fk != 'fields':
                # TODO: add extra_params
                continue

            for field in fv:
                field_schema = schema_types.FieldSchema()

                field_name = field.get('name')
                if field_name is None:
                    raise ParamError("You should specify the name of field!")
                field_schema.name = field_name

                is_primary_key = field.get('is_primary_key', False)
                if is_primary_key and auto_id:
                    raise ParamError("primary key is not supported when auto_id is True")
                field_schema.is_primary_key = is_primary_key

                field_schema.description = field.get('description', "")

                data_type = field.get('type')
                if data_type is None:
                    raise ParamError("You should specify the data type of field!")
                if not isinstance(data_type, (int, DataType)):
                    raise ParamError("Field type must be of DataType!")
                field_schema.data_type = data_type

                type_params = field.get('params')
                if isinstance(type_params, dict):
                    for tk, tv in type_params.items():
                        if tk == "dim":
                            if not tv or not isinstance(tv, int):
                                raise ParamError("dim must be of int!")
                        kv_pair = common_types.KeyValuePair(key=str(tk), value=str(tv))
                        field_schema.type_params.append(kv_pair)

                index_params = field.get('indexes')
                if isinstance(index_params, list):
                    for index_param in index_params:
                        if not isinstance(index_param, dict):
                            raise ParamError("Every index param must be of dict type!")
                        for ik, iv in index_param.items():
                            if ik == "metric_type":
                                if not isinstance(iv, MetricType) and not isinstance(iv, str):
                                    raise ParamError("metric_type must be of Milvus.MetricType or str!")
                            kv_pair = common_types.KeyValuePair(key=str(ik), value=str(iv))
                            field_schema.index_params.append(kv_pair)

                schema.fields.append(field_schema)

        return milvus_types.CreateCollectionRequest(collection_name=collection_name, schema=bytes(schema.SerializeToString()))

    @classmethod
    def drop_collection_request(cls, collection_name):
        return milvus_types.DropCollectionRequest(collection_name=collection_name)

    @classmethod
    def has_collection_request(cls, collection_name):
        return milvus_types.HasCollectionRequest(collection_name=collection_name)

    @classmethod
    def describe_collection_request(cls, collection_name):
        return milvus_types.DescribeCollectionRequest(collection_name=collection_name)

    @classmethod
    def collection_stats_request(cls, collection_name):
        return milvus_types.CollectionStatsRequest(collection_name=collection_name)

    @classmethod
    def show_collection_request(cls):
        return milvus_types.ShowCollectionRequest()

    @classmethod
    def create_partition_request(cls, collection_name, partition_name):
        return milvus_types.CreatePartitionRequest(collection_name=collection_name, partition_name=partition_name)

    @classmethod
    def drop_partition_request(cls, collection_name, partition_name):
        return milvus_types.DropPartitionRequest(collection_name=collection_name, partition_name=partition_name)

    @classmethod
    def has_partition_request(cls, collection_name, partition_name):
        return milvus_types.HasPartitionRequest(collection_name=collection_name, partition_name=partition_name)

    @classmethod
    def partition_stats_request(cls, collection_name, partition_name):
        return milvus_types.PartitionStatsRequest(collection_name=collection_name, partition_name=partition_name)

    @classmethod
    def show_partition_request(cls, collection_name):
        return milvus_types.ShowPartitionRequest(collection_name=collection_name)

    @classmethod
    def empty(cls):
        return common_types.Empty()

    @classmethod
    def partition_name(cls, collection_name, partition_tag):
        if not isinstance(collection_name, str):
            raise ParamError("collection_name must be of str type")
        if not isinstance(partition_tag, str):
            raise ParamError("partition_tag must be of str type")
        return milvus_types.PartitionName(collection_name=collection_name,
                                               tag=partition_tag)

    @classmethod
    def bulk_insert_param(cls, collection_name, entities, partition_tag, ids=None, params=None, fields_info=None,
                          **kwargs):
        default_partition_tag = "_default"  # should here?
        tag = partition_tag or default_partition_tag
        insert_request = milvus_types.InsertRequest(collection_name=collection_name, partition_name=tag)

        row_data = list()
        fields_name = list()
        fields_type = list()
        fields_len = len(entities)
        for i in range(fields_len):
            fields_name.append(entities[i]["name"])

        row_num = len(entities[0]["values"]) if fields_len > 0 else 0

        auto_id = kwargs.get("auto_id", True)

        if fields_info is None:
            # this case, we assume the order of entities is same to schema
            for i in range(row_num):
                row = []
                for j in range(fields_len):
                    row.append(entities[j]["values"][i])
                row_data.append(row)
        else:
            # field name & type must match fields info
            location = dict()

            for i, field in enumerate(fields_info):
                match_flag = False
                for j in range(fields_len):
                    # if field["name"] == entities[j]["name"] and field["type"] == entities[j]["type"]:
                    if not auto_id and "_id" not in fields_name:
                        if field["name"] == "_id":
                            match_flag = True
                            break
                        if field["name"] == entities[j]["name"]:
                            location[field["name"]] = j
                            fields_type.append(entities[j]["type"])
                            match_flag = True
                            break

                    else:
                        if field["name"] == entities[j]["name"]:
                            location[field["name"]] = j
                            fields_type.append(entities[j]["type"])
                            match_flag = True
                            break
                if not match_flag:
                    raise ParamError("Field {} don't match in entities".format(field["name"]))
            for i in range(row_num):
                row = []
                for j in range(len(fields_info)):
                    field_name = fields_info[j]["name"]
                    if not auto_id and "_id" not in fields_name and field_name == "_id":
                        continue
                    else:
                        loc = location[field_name]
                        row.append(entities[loc]["values"][i])
                row_data.append(row)

        # fill row_data in bytes format
        if not auto_id and "_id" not in fields_name:
            id_type = DataType.INT64  # int64_t is supported by default
            fields_type.insert(0, id_type)
            for i in range(row_num):
                row_data[i].insert(0, ids[i])  # fill id

        for i in range(row_num):
            blob_row_data = common_types.Blob()
            blob_row_data.value = bytes()
            for field_value, field_type in zip(row_data[i], fields_type):
                if field_type in (DataType.BOOL,):
                    blob_row_data.value += blob.boolToBytes(field_value)
                elif field_type in (DataType.INT8,):
                    blob_row_data.value += blob.int8ToBytes(field_value)
                elif field_type in (DataType.INT16,):
                    blob_row_data.value += blob.int16ToBytes(field_value)
                elif field_type in (DataType.INT32,):
                    blob_row_data.value += blob.int32ToBytes(field_value)
                elif field_type in (DataType.INT64,):
                    blob_row_data.value += blob.int64ToBytes(field_value)
                elif field_type in (DataType.FLOAT,):
                    blob_row_data.value += blob.floatToBytes(field_value)
                elif field_type in (DataType.DOUBLE,):
                    blob_row_data.value += blob.doubleToBytes(field_value)
                elif field_type in (DataType.STRING,):
                    blob_row_data.value += blob.stringToBytes(field_value)
                elif field_type in (DataType.BINARY_VECTOR,):
                    blob_row_data.value += blob.vectorBinaryToBytes(field_value)
                elif field_type in (DataType.FLOAT_VECTOR,):
                    blob_row_data.value += blob.vectorFloatToBytes(field_value)
                else:
                    raise ParamError("Unsupported data type!")
            insert_request.row_data.append(blob_row_data)

        # generate hash keys, TODO: better hash function
        if ids is not None:
            hash_keys = [len(str(e)) for e in ids]
            insert_request.hash_keys.extend(hash_keys)

        return insert_request

    @classmethod
    def insert_param(cls, collection_name, entities, partition_tag, ids=None, params=None, fields_info=None, **kwargs):
        row_batch = milvus_types.InsertRequest()
        row_batch.collection_name = collection_name
        default_partition_tag = "_default"  # should here?
        row_batch.partition_name = partition_tag or default_partition_tag

        row_data = list()
        fields_type = list()
        row_num = len(entities)
        fields_len = len(entities[0]) if row_num > 0 else 0

        if row_num <= 0 or fields_len <= 0:
            return ParamError("insert empty entity is unnecessary")

        def get_fields_by_schema():
            if fields_info is None:
                return None
            names = [field["name"] for field in fields_info]
            if not kwargs.get("auto_id", True):
                names.insert(0, "_id")
            return names

        # this case, we assume the order of entities is same to schema
        fields_name = list()
        entity = entities[0]
        for key, value in entity.items():
            if key in fields_name:
                raise ParamError("duplicated field name in entity")
            fields_name.append(key)

        auto_id = kwargs.get("auto_id", True)

        if fields_info is None:
            # this case, we assume the order of entities is same to schema
            for key, value in entity.items():
                if isinstance(value, bool):
                    fields_type.append(DataType.BOOL)
                elif isinstance(value, int):
                    fields_type.append(DataType.INT64)  # or int32?
                elif isinstance(value, float):
                    fields_type.append(DataType.FLOAT)  # or double?
                elif isinstance(value, str):
                    fields_type.append(DataType.STRING)
                elif isinstance(value, list):
                    if len(value) <= 0:
                        raise ParamError("the dim of vectors must greater than zero")
                    if isinstance(value[0], float):
                        fields_type.append(DataType.FLOAT_VECTOR)
                    # TODO: BINARY_VECTOR
                elif isinstance(value, bytes):
                    fields_type.append(DataType.BINARY_VECTOR)
                else:
                    raise ParamError("unsupported data type")
            # row_data = [[value for _, value in entity.items()]
            #             for entity in entities]

            schema_field_names = get_fields_by_schema() or fields_name
            for entity in entities:
                row = list()
                for key, value in entity.items():
                    if key not in fields_name:
                        raise ParamError("entities has different field name")
                    if key not in schema_field_names:
                        raise ParamError("field name must be in schema")
                    row.append(value)
                row_data.append(row)
        else:
            # field name & type must match fields info
            for j in range(len(fields_info)):
                field_name = fields_info[j]["name"]
                if not auto_id and "_id" not in fields_name and field_name == "_id":
                    continue
                elif field_name not in fields_name:
                    raise ParamError("Field {} don't match in entities".format(field_name))
                fields_type.append(fields_info[j]["type"])

            for i in range(row_num):
                row = list()
                for j in range(len(fields_info)):
                    field_name = fields_info[j]["name"]
                    row.append(entities[i][field_name])
                row_data.append(row)

        # fill row_data in bytes format
        if not auto_id and "_id" not in fields_name:
            id_type = DataType.INT64  # int64_t is supported by default
            fields_type.insert(0, id_type)
            for i in range(row_num):
                row_data[i].insert(0, ids[i])  # fill id

        for i in range(row_num):
            blob_row_data = common_types.Blob()
            blob_row_data.value = bytes()
            for field_value, field_type in zip(row_data[i], fields_type):
                if field_type in (DataType.BOOL,):
                    blob_row_data.value += blob.boolToBytes(field_value)
                elif field_type in (DataType.INT8,):
                    blob_row_data.value += blob.int8ToBytes(field_value)
                elif field_type in (DataType.INT16,):
                    blob_row_data.value += blob.int16ToBytes(field_value)
                elif field_type in (DataType.INT32,):
                    blob_row_data.value += blob.int32ToBytes(field_value)
                elif field_type in (DataType.INT64,):
                    blob_row_data.value += blob.int64ToBytes(field_value)
                elif field_type in (DataType.FLOAT,):
                    blob_row_data.value += blob.floatToBytes(field_value)
                elif field_type in (DataType.DOUBLE,):
                    blob_row_data.value += blob.doubleToBytes(field_value)
                elif field_type in (DataType.STRING,):
                    blob_row_data.value += blob.stringToBytes(field_value)
                elif field_type in (DataType.BINARY_VECTOR,):
                    blob_row_data.value += blob.vectorBinaryToBytes(field_value)
                elif field_type in (DataType.FLOAT_VECTOR,):
                    blob_row_data.value += blob.vectorFloatToBytes(field_value)
                else:
                    raise ParamError("Unsupported data type!")
            row_batch.row_data.append(blob_row_data)

        # generate hash keys, TODO: better hash function
        if ids is not None:
            hash_keys = [len(str(e)) for e in ids]
            row_batch.hash_keys.extend(hash_keys)

        return row_batch

    @classmethod
    def search_request(cls, collection_name, query_entities, partition_tags=None, fields=None, **kwargs):
        if not isinstance(query_entities, (dict,)):
            raise ParamError("Invalid query format. 'query_entities' must be a dict")

        request = milvus_types.SearchRequest(
            collection_name=collection_name,
            partition_names=partition_tags,
        )

        duplicated_entities = copy.deepcopy(query_entities)
        vector_placeholders = dict()

        def extract_vectors_param(param, placeholders):
            if not isinstance(param, (dict, list)):
                return

            if isinstance(param, dict):
                if "vector" in param:
                    # TODO: Here may not replace ph
                    ph = "$" + str(len(placeholders))

                    for pk, pv in param["vector"].items():
                        if "query" not in pv:
                            raise ParamError("param vector must contain 'query'")
                        placeholders[ph] = pv["query"]
                        param["vector"][pk]["query"] = ph

                    return
                else:
                    for _, v in param.items():
                        extract_vectors_param(v, placeholders)

            if isinstance(param, list):
                for item in param:
                    extract_vectors_param(item, placeholders)

        extract_vectors_param(duplicated_entities, vector_placeholders)
        request.dsl = ujson.dumps(duplicated_entities)

        plg = milvus_types.PlaceholderGroup()
        for tag, vectors in vector_placeholders.items():
            if len(vectors) <= 0:
                continue
            pl = milvus_types.PlaceholderValue(tag=tag)

            if isinstance(vectors[0], bytes):
                pl.type = milvus_types.PlaceholderType.VECTOR_BINARY
                for vector in vectors:
                    pl.values.append(blob.vectorBinaryToBytes(vector))
            else:
                pl.type = milvus_types.PlaceholderType.VECTOR_FLOAT
                for vector in vectors:
                    pl.values.append(blob.vectorFloatToBytes(vector))
            # vector_values_bytes = service_msg_types.VectorValues.SerializeToString(vector_values)

            plg.placeholders.append(pl)
        plg_str = milvus_types.PlaceholderGroup.SerializeToString(plg)
        request.placeholder_group = plg_str

        return request

    @classmethod
    def create_index__request(cls, collection_name, field_name, params):
        index_params = milvus_types.CreateIndexRequest(collection_name=collection_name, field_name=field_name)
        # index_params.collection_name = collection_name
        # index_params.field_name = field_name

        def dump(tv):
            if isinstance(tv, dict):
                import json
                return json.dumps(tv)
            return str(tv)
        if isinstance(params, dict):
            for tk, tv in params.items():
                if tk == "dim":
                    if not tv or not isinstance(tv, int):
                        raise ParamError("dim must be of int!")
                kv_pair = common_types.KeyValuePair(key=str(tk), value=dump(tv))
                index_params.extra_params.append(kv_pair)

        return index_params

    @classmethod
    def describe_index_request(cls, collection_name, field_name):
        return milvus_types.DescribeIndexRequest(collection_name=collection_name, field_name=field_name)

    @classmethod
    def describe_index_progress_request(cls, collection_name, field_name):
        return milvus_types.DescribeIndexProgressRequest(collection_name=collection_name, field_name=field_name)

    @classmethod
    def get_index_state_request(cls, collection_name, field_name):
        return milvus_types.IndexStateRequest(collection_name=collection_name, field_name=field_name)

    @classmethod
    def load_collection(cls, db_name, collection_name):
        return milvus_types.LoadCollectionRequest(db_name=db_name, collection_name=collection_name)

    @classmethod
    def release_collection(cls, db_name, collection_name):
        return milvus_types.ReleaseCollectionRequest(db_name=db_name, collection_name=collection_name)

    @classmethod
    def load_partitions(cls, db_name, collection_name, partition_names):
        return milvus_types.LoadPartitonRequest(db_name=db_name, collection_name=collection_name, partition_names= partition_names)

    @classmethod
    def release_partitions(cls, db_name, collection_name, partition_names):
        return milvus_types.ReleasePartitionRequest(db_name=db_name, collection_name=collection_name, partition_names=partition_names)

    @classmethod
    def get_collection_stats_request(cls, collection_name):
        return milvus_types.CollectionStatsRequest(collection_name=collection_name)

    @classmethod
    def flush_param(cls, collection_names):
        return milvus_types.FlushRequest(collection_names=collection_names)

    @classmethod
    def drop_index_request(cls, collection_name, field_name, index_name):
        return milvus_types.DropIndexRequest(db_name="", collection_name=collection_name, field_name=field_name, index_name=index_name)
