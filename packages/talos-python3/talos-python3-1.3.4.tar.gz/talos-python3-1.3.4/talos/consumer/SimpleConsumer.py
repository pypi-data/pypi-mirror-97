#
# Copyright 2020, Xiaomi.
# All rights reserved.
# Author: huyumei@xiaomi.com
# 

from talos.client.TalosClientConfig import TalosClientConfig
from talos.client.TalosClientConfig import TalosClientConfigKeys
from talos.thrift.auth.ttypes import Credential
from talos.thrift.topic.ttypes import TopicAndPartition
from talos.utils import Utils
from talos.client.TalosClientFactory import TalosClientFactory
from talos.client.TalosClientFactory import MessageClient
from talos.thrift.topic.TopicService import GetDescribeInfoRequest
from talos.thrift.message.MessageService import GetMessageRequest
from talos.thrift.message.MessageService import GetMessageResponse
from atomic import AtomicLong
from talos.client.compression.Compression import Compression
from talos.thrift.common.ttypes import GalaxyTalosException
from talos.thrift.message.ttypes import MessageOffset
import logging


class SimpleConsumer:
    logger = logging.getLogger("SimpleConsumer")
    consumerConfig = TalosClientConfig
    topicName = str
    partitionId = int
    credential = Credential
    topicAndPartition = TopicAndPartition
    messageClient = MessageClient
    simpleConsumerId = str
    requestId = AtomicLong

    def __init__(self, clientConfig=None, topicName=None, partitionId=None,
                 topicAndPartition=None, credential=None, messageClient=None):
        self.consumerConfig = clientConfig
        if topicName:
            Utils.check_topic_name(topicName)
            self.topicName = topicName
            self.partitionId = partitionId
            self.credential = credential
            talosClientFactory = TalosClientFactory(clientConfig, credential)
            self.messageClient = talosClientFactory.new_message_client()
            self.get_topic_info(talosClientFactory.new_topic_client(), topicName,
                                partitionId)
        else:
            self.messageClient = messageClient
            self.topicAndPartition = topicAndPartition
        self.simpleConsumerId = Utils.generate_client_id(clientConfig.get_client_ip(), "")
        self.requestId = AtomicLong(1)

    def get_topic_info(self, topicClient=None, topicName=None, partitionId=None):
        response = topicClient.get_describe_info(GetDescribeInfoRequest(topicName))
        self.topicAndPartition = TopicAndPartition(topicName,
                                                   response.topicTalosResourceName,
                                                   partitionId)

    def get_topic_talos_resource_name(self):
        return self.topicAndPartition.topicTalosResourceName

    def set_simple_consumer_id(self, simpleConsumerId=None):
        self.simpleConsumerId = simpleConsumerId

    def fetch_message(self, startOffset=None, maxFetchedNumber=None):
        Utils.check_start_offset_validity(startOffset)
        Utils.check_parameter_range(TalosClientConfigKeys.GALAXY_TALOS_CONSUMER_MAX_FETCH_RECORDS,
                                    maxFetchedNumber,
                                    TalosClientConfigKeys.GALAXY_TALOS_CONSUMER_MAX_FETCH_RECORDS_MINIMUM,
                                    TalosClientConfigKeys.GALAXY_TALOS_CONSUMER_MAX_FETCH_RECORDS_MAXIMUM)
        requestSequenceId = Utils.generate_request_sequence_id(self.simpleConsumerId,
                                                               self.requestId)

        # limit the default max fetch bytes 2M
        getMessageRequest = GetMessageRequest(self.topicAndPartition, startOffset)
        getMessageRequest.sequenceId = requestSequenceId
        getMessageRequest.maxGetMessageNumber = maxFetchedNumber
        getMessageRequest.maxGetMessageBytes = self.consumerConfig.get_max_fetch_msg_bytes()
        clientTimeout = self.consumerConfig.get_client_timeout()
        getMessageRequest.timeoutTimestamp = (Utils.current_time_mills() + clientTimeout)

        getMessageResponse = GetMessageResponse(messageBlocks=[])
        try:
            getMessageResponse = self.messageClient.get_message(getMessageRequest)
        except GalaxyTalosException as e:
            self.logger.error("fetch message failed! " + e.details)
            raise e

        messageAndOffsetList = Compression().decompress(getMessageResponse.messageBlocks,
                                                        getMessageResponse.unHandledMessageNumber)

        if len(messageAndOffsetList) <= 0:
            return messageAndOffsetList

        actualStartOffset = messageAndOffsetList[0].messageOffset

        if messageAndOffsetList[0].messageOffset == startOffset or startOffset == \
                MessageOffset.START_OFFSET or startOffset == MessageOffset.LATEST_OFFSET:
            return messageAndOffsetList
        else:
            start = int(startOffset - actualStartOffset)
            assert start > 0
            end = len(messageAndOffsetList)
            return messageAndOffsetList[start:end]



