#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from talos.client.TalosClientConfig import TalosClientConfig
from talos.thrift.auth.ttypes import Credential
from talos.thrift.common.ttypes import Version
from talos.thrift.topic import TopicService
from talos.thrift.message import MessageService
from talos.thrift.consumer import ConsumerService
from talos.thrift.quota import QuotaService
from talos.client.TalosErrors import InvalidArgumentError
from talos.client.Constants import Constants
from talos.thrift.protocol.TCompactProtocol import TCompactProtocol
from talos.client.TalosHttpClient import TalosHttpClient
import logging
import platform
import http.client
import http


class ConsumerClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def renew(self, request=None):
        self.talosHttpClient.set_query_string("type=renew")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).renew(request)

    def lock_worker(self, request=None):
        self.talosHttpClient.set_query_string("type=lockWorker")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).lockWorker(request)

    def query_worker(self, request=None):
        self.talosHttpClient.set_query_string("type=queryWorker")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).queryWorker(request)

    def lock_partition(self, request=None):
        self.talosHttpClient.set_query_string("type=lockPartition")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).lockPartition(request)

    def unlock_partition(self, request=None):
        self.talosHttpClient.set_query_string("type=unlockPartition")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).unlockPartition(request)

    def query_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=queryOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).queryOffset(request)

    def update_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=updateOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).updateOffset(request)

    def get_worker_id(self, request=None):
        self.talosHttpClient.set_query_string("type=getWorkerId")
        iprot = TCompactProtocol(self.talosHttpClient)
        return ConsumerService.Client(iprot).getWorkerId(request).workerId


class TopicClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def create_topic(self, request=None):
        self.talosHttpClient.set_query_string("type=createTopic")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).createTopic(request)

    def get_describe_info(self, request=None):
        self.talosHttpClient.set_query_string("type=getDescribeInfo")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).getDescribeInfo(request)

    def get_topic_attribute(self, request=None):
        self.talosHttpClient.set_query_string("type=getTopicAttribute")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).getTopicAttribute(request)

    def delete_topic(self, request=None):
        self.talosHttpClient.set_query_string("type=deleteTopic")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).deleteTopic(request)

    def change_topic_attribute(self, request=None):
        self.talosHttpClient.set_query_string("type=changeTopicAttribute")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).changeTopicAttribute(request)

    def list_topics(self):
        self.talosHttpClient.set_query_string("type=listTopics")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).listTopics().topicInfos

    def set_permission(self, request=None):
        assert request.permission > 0
        self.talosHttpClient.set_query_string("type=setPermission")
        iprot = TCompactProtocol(self.talosHttpClient)
        TopicService.Client(iprot).setPermission(request)

    def revoke_permission(self, request=None):
        self.talosHttpClient.set_query_string("type=revokePermission")
        iprot = TCompactProtocol(self.talosHttpClient)
        TopicService.Client(iprot).setPermission(request)

    def list_permission(self, request=None):
        self.talosHttpClient.set_query_string("type=listPermission")
        iprot = TCompactProtocol(self.talosHttpClient)
        return TopicService.Client(iprot).listPermission(request).permissions


class MessageClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def get_message(self, request=None):
        self.talosHttpClient.set_query_string("type=getMessage")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).getMessage(request)

    def put_message(self, request=None):
        self.talosHttpClient.set_query_string("type=putMessage")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).putMessage(request)

    def get_topic_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=getTopicOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).getTopicOffset(request).offsetInfoList

    def get_partition_offset(self, request=None):
        self.talosHttpClient.set_query_string("type=getPartitionOffset")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).getPartitionOffset(request).offsetInfo

    def get_schedule_info(self, request=None):
        self.talosHttpClient.set_query_string("type=getScheduleInfo")
        iprot = TCompactProtocol(self.talosHttpClient)
        return MessageService.Client(iprot).getScheduleInfo(request).scheduleInfo


class QuotaClient:
    talosHttpClient = TalosHttpClient

    def __init__(self, talosHttpClient=None):
        self.talosHttpClient = talosHttpClient

    def apply_quota(self, request=None):
        self.talosHttpClient.set_query_string("type=applyQuota")
        iprot = TCompactProtocol(self.talosHttpClient)
        QuotaService.Client(iprot).applyQuota(request)

    def revoke_quota(self, request=None):
        self.talosHttpClient.set_query_string("type=revokeQuota")
        iprot = TCompactProtocol(self.talosHttpClient)
        return QuotaService.Client(iprot).revokeQuota(request)

    def list_quota(self):
        self.talosHttpClient.set_query_string("type=listQuota")
        iprot = TCompactProtocol(self.talosHttpClient)
        return QuotaService.Client(iprot).listQuota()


class TalosClientFactory:
    logger = logging.getLogger("TalosClientFactory")
    _USER_AGENT_HEADER = "User-Agent"
    _SID = "galaxytalos"
    _DEFAULT_CLIENT_CONN_TIMEOUT = 5000

    _version = Version
    _talosClientConfig = TalosClientConfig
    _credential = Credential
    _customHeaders = dict
    _httpClient = http.client.HTTPConnection
    _agent = str
    _clockOffset = int

    def __init__(self, clientConfig=None, credential=None):
        self._talosClientConfig = clientConfig
        self._credential = credential
        self._customHeaders = None
        self._version = Version()
        self._clockOffset = 0

    def new_topic_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_TOPIC_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return TopicClient(talosHttpClient)

    def new_consumer_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_CONSUMER_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return ConsumerClient(talosHttpClient)

    def set_custom_headers(self, customHeaders=None):
        self._customHeaders = customHeaders

    def new_message_client(self):
        headers = dict()
        headers[self._USER_AGENT_HEADER] = self.create_user_agent_header()
        if self._customHeaders:
            for k in self._customHeaders:
                headers[k] = self._customHeaders[k]
        # setting 'supportAccountKey' to true for using Galaxy-V3 auth
        talosHttpClient = TalosHttpClient(self._talosClientConfig.get_service_endpoint()
                                          + Constants.TALOS_MESSAGE_SERVICE_PATH,
                                          self._credential, self._clockOffset, True)
        talosHttpClient.set_custom_headers(headers)
        talosHttpClient.set_timeout(self._talosClientConfig.get_client_conn_timeout())
        return MessageClient(talosHttpClient)

    def check_credential(self):
        if not self._credential:
            raise InvalidArgumentError("Credential is not set")

    def create_user_agent_header(self):
        return "Python-SDK/" + str(self._version.major) + "." + str(self._version.minor) + "." + str(self._version.revision) + " Python/" + platform.python_version()


