# -*- coding:utf8 -*-
#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from talos.client.TalosClientConfig import TalosClientConfig
from talos.client.compression.Compression import Compression
from talos.client.TalosClientFactory import TalosClientFactory
from talos.thrift.topic.ttypes import TopicAndPartition
from talos.thrift.topic.TopicService import GetDescribeInfoRequest
from talos.thrift.message import MessageService
from talos.thrift.message.ttypes import MessageType
from talos.thrift.message.ttypes import PutMessageRequest
from atomic import AtomicLong
from talos.utils import Utils
import logging
import traceback


class SimpleProducer(object):
    logger = logging.getLogger("SimpleConsumer")

    producerConfig = TalosClientConfig
    topicAndPartition = TopicAndPartition
    messageClient = MessageService.Iface
    requestId = AtomicLong
    clientId = str
    isActive = bool

    def __init__(self, producerConfig=None, topicName=None, topicAndPartition=None,
                 partitionId=None, credential=None, talosClientFactory=None,
                 messageClient=None, clientId=None, requestId=None):
        if talosClientFactory:
            self.talosClientFactory = talosClientFactory
        elif credential:
            self.talosClientFactory = TalosClientFactory(producerConfig, credential)
        if topicName:
            Utils.check_topic_name(topicName)
            self.get_topic_info(self.talosClientFactory.new_topic_client(), topicName,
                                partitionId)
        else:
            self.topicAndPartition = topicAndPartition
        self.producerConfig = producerConfig
        if messageClient:
            self.messageClient = messageClient
        else:
            self.messageClient = self.talosClientFactory.new_message_client()
        if clientId:
            self.clientId = clientId
        else:
            self.clientId = Utils.generate_client_id('SimpleProducer', '')
        if requestId:
            self.requestId = requestId
        else:
            self.requestId = AtomicLong(1)
        self.isActive = True

    def get_topic_info(self, topicClient=None, topicName=None, partitionId=None):
        response = topicClient.get_describe_info(GetDescribeInfoRequest(topicName))
        self.topicAndPartition = TopicAndPartition(topicName=topicName,
                                                   topicTalosResourceName=response.topicTalosResourceName,
                                                   partitionId=partitionId)

    def put_message(self, msgList=None):
        if (not msgList) or len(msgList) == 0:
            return True

        try:
            self.put_message_list(msgList)
            return True
        except Exception as e:
            self.logger.error("putMessage error， please try to put again"
                              + str(traceback.format_exc()))

        return False

    def put_message_list(self, msgList=None):
        if (not msgList) or len(msgList) == 0:
            return

        # check data validity
        for message in msgList:
            # set timestamp and messageType if not set
            Utils.update_message(message, MessageType.BINARY)

        # check data validity
        Utils.check_message_list_validity(msgList)

        self.do_put(msgList)

    def do_put(self, msgList=None):
        messageBlock = self._compress_message_list(msgList)
        messageBlockList = [messageBlock]

        requestSequenceId = Utils.generate_request_sequence_id(self.clientId,
                                                               self.requestId)
        putMessageRequest = PutMessageRequest(self.topicAndPartition, messageBlockList,
                                              len(msgList), requestSequenceId)
        try:
            putMessageResponse = self.messageClient.put_message(putMessageRequest)
        except Exception as e:
            self.logger.error("put message request failed." + str(traceback.format_exc()))
            raise e

    def _compress_message_list(self, msgList=None):
        return Compression().compress(msgList, self.producerConfig.get_compression_type())




