import datetime
import time
from urllib.parse import urlparse
import logging
import threading
import json

import grpc
from grpc._cython import cygrpc

from ..grpc_gen import common_pb2 as common_types
from ..grpc_gen import milvus_pb2_grpc
from ..grpc_gen import milvus_pb2 as milvus_types
from .abstract import QueryResult, CollectionSchema
from .prepare import Prepare
from .types import Status
from .check import (
    int_or_str,
    is_legal_host,
    is_legal_port,
)

from .abs_client import AbsMilvus
from .asynch import SearchFuture, InsertFuture, CreateIndexFuture, FlushFuture, LoadCollectionFuture, LoadPartitionsFuture

from .hooks import BaseSearchHook
from .client_hooks import SearchHook, HybridSearchHook
from .exceptions import *
from ..settings import DefaultConfig as config
from . import __version__

LOGGER = logging.getLogger(__name__)


def error_handler(*rargs):
    def wrapper(func):
        def handler(self, *args, **kwargs):
            record_dict = {}
            try:
                record_dict["API start"] = str(datetime.datetime.now())
                if self._pre_ping:
                    self.ping()
                record_dict["RPC start"] = str(datetime.datetime.now())
                return func(self, *args, **kwargs)
            except BaseException as e:
                LOGGER.error("Error: {}".format(e))
                if e.code == Status.ILLEGAL_COLLECTION_NAME:
                    raise IllegalCollectionNameException(e.code, e.message)
                if e.code == Status.COLLECTION_NOT_EXISTS:
                    raise CollectionNotExistException(e.code, e.message)

                raise e

            except grpc.FutureTimeoutError as e:
                record_dict["RPC timeout"] = str(datetime.datetime.now())
                LOGGER.error("\nAddr [{}] {}\nRequest timeout: {}\n\t{}".format(self.server_address, func.__name__, e,
                                                                                record_dict))
                raise e
            except grpc.RpcError as e:
                record_dict["RPC error"] = str(datetime.datetime.now())
                LOGGER.error(
                    "\nAddr [{}] {}\nRPC error: {}\n\t{}".format(self.server_address, func.__name__, e, record_dict))
                raise e
            except Exception as e:
                record_dict["Exception"] = str(datetime.datetime.now())
                LOGGER.error("\nAddr [{}] {}\nExcepted error: {}\n\t{}".format(self.server_address, func.__name__, e,
                                                                               record_dict))
                raise e

        return handler

    return wrapper


def set_uri(host, port, uri):
    if host is not None:
        _port = port if port is not None else config.GRPC_PORT
        _host = host
    elif port is None:
        try:
            _uri = urlparse(uri) if uri else urlparse(config.GRPC_URI)
            _host = _uri.hostname
            _port = _uri.port
        except (AttributeError, ValueError, TypeError) as e:
            raise ParamError("uri is illegal: {}".format(e))
    else:
        raise ParamError("Param is not complete. Please invoke as follow:\n"
                         "\t(host = ${HOST}, port = ${PORT})\n"
                         "\t(uri = ${URI})\n")

    if not is_legal_host(_host) or not is_legal_port(_port):
        raise ParamError("host or port is illeagl")

    return "{}:{}".format(str(_host), str(_port))


class RegistryHandler:
    def __init__(self, host=None, port=None, pre_ping=True, **kwargs):
        self._channel = None
        self._stub = None
        self._uri = None
        self.status = None
        self._connected = False
        self._pre_ping = pre_ping
        # if self._pre_ping:
        self._max_retry = kwargs.get("max_retry", 5)

        # record
        self._id = kwargs.get("conn_id", 0)

        # condition
        self._condition = threading.Condition()
        self._request_id = 0

        # set server uri if object is initialized with parameter
        _uri = kwargs.get("uri", None)
        self._setup(host, port, _uri, pre_ping)

    def __str__(self):
        attr_list = ['%s=%r' % (key, value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<Milvus: {}>'.format(', '.join(attr_list))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self._channel.close()
        pass

    def _setup(self, host, port, uri, pre_ping=False):
        """
        Create a grpc channel and a stub

        :raises: NotConnectError

        """
        self._uri = set_uri(host, port, uri)
        self._channel = grpc.insecure_channel(
            self._uri,
            options=[(cygrpc.ChannelArgKey.max_send_message_length, -1),
                     (cygrpc.ChannelArgKey.max_receive_message_length, -1),
                     ('grpc.enable_retries', 1),
                     ('grpc.keepalive_time_ms', 55000)]
        )
        # self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self._stub = milvus_pb2_grpc.ProxyServiceStub(self._channel)
        self.status = Status()

    def _pre_request(self):
        if self._pre_ping:
            self.ping()

    def _get_request_id(self):
        with self._condition:
            _id = self._request_id
            self._request_id += 1
            return _id

    def ping(self):
        begin_timeout = 1
        timeout = begin_timeout
        ft = grpc.channel_ready_future(self._channel)
        retry = self._max_retry
        try:
            while retry > 0:
                try:
                    ft.result(timeout=timeout)
                    return True
                except:
                    retry -= 1
                    LOGGER.debug("Retry connect addr <{}> {} times".format(self._uri, self._max_retry - retry))
                    if retry > 0:
                        timeout *= 2
                        continue
                    else:
                        LOGGER.error("Retry to connect server {} failed.".format(self._uri))
                        raise
        except grpc.FutureTimeoutError:
            raise NotConnectError('Fail connecting to server on {}. Timeout'.format(self._uri))
        except grpc.RpcError as e:
            raise NotConnectError("Connect error: <{}>".format(e))
        # Unexpected error
        except Exception as e:
            raise NotConnectError("Error occurred when trying to connect server:\n"
                                  "\t<{}>".format(str(e)))

    @property
    def server_address(self):
        """
        Server network address
        """
        return self._uri

    @error_handler(None)
    def register_link(self, timeout=20):
        request = common_types.Empty()
        rf = self._stub.RegisterLink.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.status.error_code != 0:
            LOGGER.error(response.status)
            raise BaseException(response.status.error_code, response.status.reason)
        return response.address.ip, response.address.port


class GrpcHandler(AbsMilvus):
    def __init__(self, host=None, port=None, pre_ping=True, **kwargs):
        self._channel = None
        self._stub = None
        self._uri = None
        self.status = None
        self._connected = False
        self._pre_ping = pre_ping
        # if self._pre_ping:
        self._max_retry = kwargs.get("max_retry", 5)

        # record
        self._id = kwargs.get("conn_id", 0)

        # condition
        self._condition = threading.Condition()
        self._request_id = 0

        # client hook
        self._search_hook = SearchHook()
        self._hybrid_search_hook = HybridSearchHook()
        self._search_file_hook = SearchHook()

        # set server uri if object is initialized with parameter
        _uri = kwargs.get("uri", None)
        self._setup(host, port, _uri, pre_ping)

    def __str__(self):
        attr_list = ['%s=%r' % (key, value)
                     for key, value in self.__dict__.items() if not key.startswith('_')]
        return '<Milvus: {}>'.format(', '.join(attr_list))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _setup(self, host, port, uri, pre_ping=False):
        """
        Create a grpc channel and a stub

        :raises: NotConnectError

        """
        self._uri = set_uri(host, port, uri)
        self._channel = grpc.insecure_channel(
            self._uri,
            options=[(cygrpc.ChannelArgKey.max_send_message_length, -1),
                     (cygrpc.ChannelArgKey.max_receive_message_length, -1),
                     ('grpc.enable_retries', 1),
                     ('grpc.keepalive_time_ms', 55000)]
        )
        # self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self._stub = milvus_pb2_grpc.MilvusServiceStub(self._channel)
        self.status = Status()

    def _pre_request(self):
        if self._pre_ping:
            self.ping()

    def _get_request_id(self):
        with self._condition:
            _id = self._request_id
            self._request_id += 1
            return _id

    def set_hook(self, **kwargs):
        """
        specify client hooks.
        The client hooks are used in methods which interact with server.
        Use key-value method to set hooks. Supported hook setting currently is as follow.

            search hook,
            search-in-file hook

        """

        # config search hook
        _search_hook = kwargs.get('search', None)
        if _search_hook:
            if not isinstance(_search_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_hook = _search_hook

        _search_file_hook = kwargs.get('search_in_file', None)
        if _search_file_hook:
            if not isinstance(_search_file_hook, BaseSearchHook):
                raise ParamError("search hook must be a subclass of `BaseSearchHook`")

            self._search_file_hook = _search_file_hook

    def ping(self):
        begin_timeout = 1
        timeout = begin_timeout
        ft = grpc.channel_ready_future(self._channel)
        retry = self._max_retry
        try:
            while retry > 0:
                try:
                    ft.result(timeout=timeout)
                    return True
                except:
                    retry -= 1
                    LOGGER.debug("Retry connect addr <{}> {} times".format(self._uri, self._max_retry - retry))
                    if retry > 0:
                        timeout *= 2
                        continue
                    else:
                        LOGGER.error("Retry to connect server {} failed.".format(self._uri))
                        raise
        except grpc.FutureTimeoutError:
            raise NotConnectError('Fail connecting to server on {}. Timeout'.format(self._uri))
        except grpc.RpcError as e:
            raise NotConnectError("Connect error: <{}>".format(e))
        # Unexpected error
        except Exception as e:
            raise NotConnectError("Error occurred when trying to connect server:\n"
                                  "\t<{}>".format(str(e)))

    @property
    def server_address(self):
        """
        Server network address
        """
        return self._uri

    @error_handler()
    def create_collection(self, collection_name, fields, timeout=30):
        request = Prepare.create_collection_request(collection_name, fields)

        rf = self._stub.CreateCollection.future(request, wait_for_ready=True, timeout=timeout)
        status = rf.result()
        if status.error_code != 0:
            LOGGER.error(status)
            raise BaseException(status.error_code, status.reason)

        # self.load_collection("", collection_name)

        # return Status(status.error_code, status.reason)

    @error_handler()
    def drop_collection(self, collection_name, timeout=20):
        request = Prepare.drop_collection_request(collection_name)

        rf = self._stub.DropCollection.future(request, wait_for_ready=True, timeout=timeout)
        status = rf.result()
        if status.error_code != 0:
            raise BaseException(status.error_code, status.reason)

        # return Status(status.error_code, status.reason)

    @error_handler(False)
    def has_collection(self, collection_name, timeout=30, **kwargs):
        request = Prepare.has_collection_request(collection_name)

        rf = self._stub.HasCollection.future(request, wait_for_ready=True, timeout=timeout)
        reply = rf.result()
        if reply.status.error_code == 0:
            # return Status(reply.status.error_code, reply.status.reason), reply.value
            return reply.value

        raise BaseException(reply.status.error_code, reply.status.reason)

    @error_handler(None)
    def describe_collection(self, collection_name, timeout=30, **kwargs):
        # TODO: which request
        request = Prepare.describe_collection_request(collection_name)
        rf = self._stub.DescribeCollection.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status

        if status.error_code == 0:
            # return Status(status.error_code, status.reason), CollectionSchema(raw=response).dict()
            return CollectionSchema(raw=response).dict()

        LOGGER.error(status)
        raise BaseException(status.error_code, status.reason)
        # return Status(status.error_code, status.reason), CollectionSchema(None)

    @error_handler([])
    def list_collections(self, timeout=30):
        request = Prepare.show_collection_request()
        rf = self._stub.ShowCollections.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if response.status.error_code == 0:
            # return Status(status.error_code, status.reason), [name for name in response.values if len(name) > 0]
            return list(response.collection_names)
        raise BaseException(status.error_code, status.reason)

    @error_handler()
    def create_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.create_partition_request(collection_name, partition_tag)
        rf = self._stub.CreatePartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
        # self.load_partitions("", collection_name, [partition_tag], timeout=timeout)
        # return Status(response.status.error_code, response.status.reason)

    @error_handler()
    def drop_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.drop_partition_request(collection_name, partition_tag)

        rf = self._stub.DropPartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()

        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

        # return Status(response.error_code, response.reason)

    @error_handler(False)
    def has_partition(self, collection_name, partition_tag, timeout=30):
        request = Prepare.has_partition_request(collection_name, partition_tag)
        rf = self._stub.HasPartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            return response.value

        raise BaseException(status.error_code, status.reason)

    @error_handler(None)
    def get_partition_info(self, collection_name, partition_tag, timeout=30):
        request = Prepare.partition_stats_request(collection_name, partition_tag)
        rf = self._stub.DescribePartition.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            statistics = response.statistics
            info_dict = dict()
            for kv in statistics:
                info_dict[kv.key] = kv.value
            return info_dict
        raise BaseException(status.error_code, status.reason)

    @error_handler([])
    def list_partitions(self, collection_name, timeout=30):
        request = Prepare.show_partition_request(collection_name)

        rf = self._stub.ShowPartitions.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            return list(response.partition_names)

        raise BaseException(status.error_code, status.reason)

    @error_handler([])
    def bulk_insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        insert_param = kwargs.get('insert_param', None)

        # if insert_param and not isinstance(insert_param, grpc_types.InsertParam):
        #     raise ParamError("The value of key 'insert_param' is invalid")
        if insert_param and not isinstance(insert_param, milvus_types.RowBatch):
            raise ParamError("The value of key 'insert_param' is invalid")

        collection_request = Prepare.describe_collection_request(collection_name)
        rf = self._stub.DescribeCollection.future(collection_request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)
        collection_schema = CollectionSchema(raw=response).dict()

        auto_id = collection_schema["auto_id"]
        fields_name = list()
        for i in range(len(entities)):
            if "name" in entities[i]:
                fields_name.append(entities[i]["name"])
        if not auto_id and ids is None and "_id" not in fields_name:
            raise ParamError("You should specify the ids of entities!")

        if not auto_id and ids is not None and "_id" in fields_name:
            raise ParamError("You should specify the ids of entities!")

        fields_info = collection_schema["fields"]

        if (auto_id and len(entities) != len(fields_info)) \
                or (not auto_id and ids is not None and len(entities) == len(fields_info)):
            raise ParamError("The length of entities must be equal to the number of fields!")

        if ids is None:
            ids = []
            for entity in entities:
                if "_id" in entity:
                    ids.append(entity["_id"])
            if not ids:
                ids = None

        requset = insert_param if insert_param \
            else Prepare.bulk_insert_param(collection_name, entities, partition_tag, ids, params, fields_info,
                                           auto_id=auto_id)

        rf = self._stub.Insert.future(requset, wait_for_ready=True, timeout=timeout)
        if kwargs.get("_async", False) is True:
            cb = kwargs.get("_callback", None)
            return InsertFuture(rf, cb)

        response = rf.result()
        if response.status.error_code == 0:
            if auto_id:
                return list(range(response.rowID_begin, response.rowID_end))
            return list(ids)

        raise BaseException(response.status.error_code, response.status.reason)

    @error_handler([])
    def insert(self, collection_name, entities, ids=None, partition_tag=None, params=None, timeout=None, **kwargs):
        insert_param = kwargs.get('insert_param', None)

        # if insert_param and not isinstance(insert_param, grpc_types.InsertParam):
        #     raise ParamError("The value of key 'insert_param' is invalid")
        if insert_param and not isinstance(insert_param, milvus_types.RowBatch):
            raise ParamError("The value of key 'insert_param' is invalid")

        collection = Prepare.describe_collection_request(collection_name)
        rf = self._stub.DescribeCollection.future(collection, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)
        collection_schema = CollectionSchema(raw=response).dict()

        auto_id = collection_schema["auto_id"]
        fields_name = list()
        entity = entities[0]
        for key, value in entity.items():
            if key in fields_name:
                raise ParamError("duplicated field name in entity")
            fields_name.append(key)

        if not auto_id and ids is None and "_id" not in fields_name:
            raise ParamError("You should specify the ids of entities!")

        if not auto_id and ids is not None and "_id" in fields_name:
            raise ParamError("You should specify the ids of entities!")

        fields_info = collection_schema["fields"]

        if (auto_id and len(entities[0]) != len(fields_info)) \
                or (not auto_id and ids is not None and len(entities[0]) == len(fields_info)):
            raise ParamError("The length of entities must be equal to the number of fields!")

        if ids is None:
            ids = []
            for entity in entities:
                if "_id" in entity:
                    ids.append(entity["_id"])
            if not ids:
                ids = None

        body = insert_param if insert_param \
            else Prepare.insert_param(collection_name, entities, partition_tag, ids, params, fields_info,
                                      auto_id=auto_id)

        rf = self._stub.Insert.future(body, wait_for_ready=True, timeout=timeout)
        if kwargs.get("_async", False) is True:
            cb = kwargs.get("_callback", None)
            return InsertFuture(rf, cb)

        response = rf.result()
        if response.status.error_code == 0:
            if auto_id:
                return list(range(response.rowID_begin, response.rowID_end))
            return list(ids)

        raise BaseException(response.status.error_code, response.status.reason)

    @error_handler(None)
    def search(self, collection_name, query_entities, partition_tags=None, fields=None, **kwargs):
        to = kwargs.get("timeout", None)
        rf = self._stub.HasCollection.future(Prepare.has_collection_request(collection_name), wait_for_ready=True,
                                             timeout=to)
        reply = rf.result()
        if reply.status.error_code != 0 or not reply.value:
            raise BaseException(reply.status.error_code, "collection not exists")

        request = Prepare.search_request(collection_name, query_entities, partition_tags, fields)
        self._search_hook.pre_search()
        ft = self._stub.Search.future(request, wait_for_ready=True, timeout=to)
        if kwargs.get("_async", False) is True:
            func = kwargs.get("_callback", None)
            return SearchFuture(ft, func)

        response = ft.result()
        self._search_hook.aft_search()

        if self._search_hook.on_response():
            return response

        if response.status.error_code != 0:
            raise BaseException(response.status.error_code, response.status.reason)

        collection_schema = self.describe_collection(collection_name=collection_name)
        auto_id = collection_schema["auto_id"]

        # TODO: handler response
        # resutls = self._search_hook.handle_response(response)

        return QueryResult(response, auto_id)

    @error_handler(None)
    def get_query_segment_infos(self, collection_name, timeout=30, **kwargs):
        req = milvus_types.QuerySegmentInfoRequest(collectionName=collection_name)
        future = self._stub.GetQuerySegmentInfo.future(req, wait_for_ready=True, timeout=timeout)
        response = future.result()
        status = response.status
        if status.error_code == 0:
            return response.infos  # todo: A wrapper class of QuerySegmentInfo
        raise BaseException(status.error_code, status.reason)

    @error_handler()
    def wait_for_load_index_done(self, collection_name, timeout=30, **kwargs):
        def load_index_done():
            query_segment_infos = self.get_query_segment_infos(collection_name)
            persistent_segment_infos = self.get_persistent_segment_infos(collection_name)

            query_segment_ids = [info.segmentID for info in query_segment_infos]
            persistent_segment_ids = [info.segmentID for info in persistent_segment_infos]

            if len(persistent_segment_ids) != len(query_segment_ids):
                return False

            if len(query_segment_ids) == 0:
                return True

            query_segment_ids.sort()
            persistent_segment_ids.sort()
            if query_segment_ids != persistent_segment_ids:
                return False

            filtered_query_segment_info = list(filter(lambda info : info.index_name == "_default_idx", query_segment_infos))
            filtered_query_segment_index_ids = list(map(lambda info : info.indexID, filtered_query_segment_info))
            return len(set(filtered_query_segment_index_ids)) == 1

        while True:
            time.sleep(0.5)
            print("\n***********  waiting for load index done ***********\n")
            if load_index_done():
                return

    @error_handler()
    def create_index(self, collection_name, field_name, params, timeout=None, **kwargs):
        # sync flush
        _async = kwargs.get("_async", False)
        kwargs["_async"] = False
        self.flush([collection_name], timeout, **kwargs)

        index_param = Prepare.create_index__request(collection_name, field_name, params)
        future = self._stub.CreateIndex.future(index_param, wait_for_ready=True, timeout=timeout)

        if _async:
            def _check():
                if kwargs.get("sync", True):
                    if not self.wait_for_creating_index(collection_name=collection_name, field_name=field_name):
                        raise BaseException(Status.UNEXPECTED_ERROR, "create index failed")

            index_future = CreateIndexFuture(future)
            index_future.add_callback(_check)
            user_cb = kwargs.get("_callback", None)
            if user_cb:
                index_future.add_callback(user_cb)
            return index_future

        status = future.result()

        if status.error_code != 0:
            raise BaseException(status.error_code, status.reason)

        if kwargs.get("sync", True):
            if not self.wait_for_creating_index(collection_name=collection_name, field_name=field_name):
                raise BaseException(Status.UNEXPECTED_ERROR, "create index failed")

        return Status(status.error_code, status.reason)

    @error_handler(None)
    def describe_index(self, collection_name, field_name, timeout=None, **kwargs):
        request = Prepare.describe_index_request(collection_name, field_name)

        rf = self._stub.DescribeIndex.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            index_descriptions = response.index_descriptions
            if not index_descriptions:
                raise BaseException(status.error_code, status.reason)
            else:
                info_dict = dict()
                for kv in index_descriptions[0].params:
                    value = kv.value
                    if kv.key == 'params':
                        value = json.loads(kv.value)
                    info_dict[kv.key] = value
                return info_dict
        raise BaseException(status.error_code, status.reason)

    @error_handler(common_types.IndexState.FAILED)
    def get_index_state(self, collection_name, field_name, timeout=None, **kwargs):
        request = Prepare.get_index_state_request(collection_name, field_name)
        rf = self._stub.GetIndexState.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code == 0:
            return response.state
        raise BaseException(status.error_code, status.reason)

    @error_handler(False)
    def wait_for_creating_index(self, collection_name, field_name, timeout=30, **kwargs):
        while True:
            time.sleep(0.5)
            print("\n***********  waiting for building index ***********\n")
            try:
                state = self.get_index_state(collection_name, field_name, timeout, **kwargs)
                if state == common_types.IndexState.FINISHED:
                    return True
                if state == common_types.IndexState.FAILED:
                    return False
            except BaseException:
                return False

    @error_handler()
    def load_collection(self, db_name, collection_name, timeout=None, **kwargs):
        request = Prepare.load_collection(db_name, collection_name)
        rf = self._stub.LoadCollection.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
        sync = kwargs.get("sync", True)
        if sync:
            self.wait_for_loading_collection(collection_name)

    @error_handler()
    def wait_for_loading_collection(self, collection_name, timeout=30):
        """
        Block until load collection complete.
        """

        unloaded_segments = {info.segmentID: info.num_rows for info in
                                self.get_persistent_segment_infos(collection_name, timeout)}
        print("unloaded segment numbers: {}".format(len(unloaded_segments)))

        while len(unloaded_segments) > 0:
            print("\n***********  waiting for load collection ***********\n")
            time.sleep(0.5)

            for info in self.get_query_segment_infos(collection_name, timeout):
                if 0 < unloaded_segments.get(info.segmentID, 0) <= info.num_rows:
                    unloaded_segments.pop(info.segmentID)

    @error_handler()
    def release_collection(self, db_name, collection_name, timeout=30):
        request = Prepare.release_collection(db_name, collection_name)
        rf = self._stub.ReleaseCollection.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

    @error_handler()
    def load_partitions(self, db_name, collection_name, partition_names, timeout=30, **kwargs):
        request = Prepare.load_partitions(db_name=db_name, collection_name=collection_name,
                                          partition_names=partition_names)
        future = self._stub.LoadPartitions.future(request, wait_for_ready=True, timeout=timeout)

        if kwargs.get("_async", False):
            def _check():
                if kwargs.get("sync", True):
                    self.wait_for_loading_partitions(collection_name, partition_names)

            load_partitions_future = LoadPartitionsFuture(future)
            load_partitions_future.add_callback(_check)

            user_cb = kwargs.get("_callback", None)
            if user_cb:
                load_partitions_future.add_callback(user_cb)

            return load_partitions_future

        response = future.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
        sync = kwargs.get("sync", True)
        if sync:
            self.wait_for_loading_partitions(collection_name, partition_names)

    @error_handler()
    def wait_for_loading_partitions(self, collection_name, partition_names, timeout=30):
        """
        Block until load partition complete.
        """
        request = Prepare.show_partition_request(collection_name)
        rf = self._stub.ShowPartitions.future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        status = response.status
        if status.error_code != 0:
            raise BaseException(status.error_code, status.reason)

        pIDs = [response.partitionIDs[index] for index, p_name in enumerate(response.partition_names)
                if p_name in partition_names]

        unloaded_segments = {info.segmentID: info.num_rows for info in
                             self.get_persistent_segment_infos(collection_name, timeout)
                             if info.partitionID in pIDs}

        print("unloaded segment numbers: {}".format(len(unloaded_segments)))

        while len(unloaded_segments) > 0:
            print("\n***********  waiting for load collection ***********\n")
            time.sleep(0.5)

            for info in self.get_query_segment_infos(collection_name, timeout):
                if  0 < unloaded_segments.get(info.segmentID, 0) <= info.num_rows:
                    unloaded_segments.pop(info.segmentID)

    @error_handler()
    def release_partitions(self, db_name, collection_name, partition_names, timeout=30):
        request = Prepare.release_partitions(db_name, collection_name,
                                             partition_names)
        rf = self._stub.ReleasePartions().future(request, wait_for_ready=True, timeout=timeout)
        response = rf.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

    @error_handler(None)
    def get_collection_stats(self, collection_name, timeout=None, **kwargs):
        index_param = Prepare.get_collection_stats_request(collection_name)
        future = self._stub.GetCollectionStatistics.future(index_param, wait_for_ready=True, timeout=timeout)
        response = future.result()
        status = response.status
        if status.error_code == 0:
            return response.stats

    @error_handler(None)
    def get_persistent_segment_infos(self, collection_name, timeout=30, **kwargs):
        req = milvus_types.PersistentSegmentInfoRequest(collectionName=collection_name)
        future = self._stub.GetPersistentSegmentInfo.future(req, wait_for_ready=True, timeout=timeout)
        response = future.result()
        status = response.status
        if status.error_code == 0:
            return response.infos  # todo: A wrapper class of PersistentSegmentInfo
        raise BaseException(status.error_code, status.reason)

    @error_handler()
    def wait_for_flushed(self, collection_name, timeout=30, **kwargs):
        def flushed():
            try:
                infos = self.get_persistent_segment_infos(collection_name, timeout, **kwargs)
                for info in infos:
                    print("info.state: ", info.state)
                    if info.state != common_types.SegmentState.SegmentFlushed:
                        return False
                return True
            except BaseException:
                return False

        while True:
            time.sleep(0.5)
            print("\n***********  waiting for flushed ***********\n")
            if flushed():
                return

    @error_handler()
    def flush(self, collection_name_array: list, timeout=None, **kwargs):
        print("CZS::::::::::::::::::::::::::::", collection_name_array)
        request = Prepare.flush_param(collection_name_array)
        future = self._stub.Flush.future(request, wait_for_ready=True, timeout=timeout)

        if kwargs.get("_async", False):
            def _check():
                if kwargs.get("sync", True):
                    for collection_name in collection_name_array:
                        self.wait_for_flushed(collection_name)

            flush_future = FlushFuture(future)
            flush_future.add_callback(_check)

            user_cb = kwargs.get("_callback", None)
            if user_cb:
                flush_future.add_callback(user_cb)

            return flush_future

        response = future.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
        sync = kwargs.get("sync", True)
        if sync:
            for collection_name in collection_name_array:
                self.wait_for_flushed(collection_name)

    @error_handler()
    def drop_index(self, collection_name, field_name, index_name, timeout=30, **kwargs):
        request = Prepare.drop_index_request(collection_name, field_name, index_name)
        future = self._stub.DropIndex.future(request, wait_for_ready=True, timeout=timeout)
        response = future.result()
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

    @error_handler(False)
    def fake_register_link(self, timeout=30):
        request = Prepare.empty()
        future = self._stub.RegisterLink.future(request, wait_for_ready=True, timeout=timeout)
        return future.result().status.error_code == 0
