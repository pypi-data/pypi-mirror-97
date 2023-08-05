import threading

from .MessageListener import MessageListener
from .MessageProducer import MessageProducer
from hkube_python_wrapper.util.DaemonThread import DaemonThread
from hkube_python_wrapper.util.logger import log


class StreamingManager(DaemonThread):
    threadLocalStorage = threading.local()

    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        self.messageProducer = None
        self._messageListeners = dict()
        self._inputListener = []
        self.listeningToMessages = False
        self.parsedFlows = {}
        self.defaultFlow = None
        self._isActive = True
        self.listenerLock = threading.Lock()
        DaemonThread.__init__(self, "StreamingManager")

    def setParsedFlows(self, flows, defaultFlow):
        self.parsedFlows = flows
        self.defaultFlow = defaultFlow

    def setupStreamingProducer(self, onStatistics, producerConfig, nextNodes, me):
        self.messageProducer = MessageProducer(producerConfig, nextNodes, me)
        self.messageProducer.registerStatisticsListener(onStatistics)
        if (nextNodes):
            self.messageProducer.start()

    def setupStreamingListeners(self, listenerConfig, parents, nodeName):
        self.listenerLock.acquire()
        try:
            log.debug("parents {parents}", parents=str(parents))
            for parent in parents:
                address = parent['address']
                modeType = parent['type']
                parentNodeName = parent['nodeName']

                if(self._messageListeners.get(parentNodeName) is None):
                    self._messageListeners[parentNodeName] = dict()

                remoteAddressUrl = 'tcp://{host}:{port}'.format(host=address['host'], port=address['port'])
                if (modeType== 'Add'):
                    options = {}
                    options.update(listenerConfig)
                    options['remoteAddress'] = remoteAddressUrl
                    options['messageOriginNodeName'] = parentNodeName
                    listener = MessageListener(options, nodeName, self.errorHandler)
                    listener.registerMessageListener(self._onMessage)
                    self._messageListeners[parentNodeName][remoteAddressUrl] = listener
                    if (self.listeningToMessages):
                        listener.start()

                if (modeType == 'Del'):
                    if (self.listeningToMessages):
                        try:
                            self._messageListeners[parentNodeName][remoteAddressUrl].close()
                        except Exception as e:
                            log.error('another Exception: {e}', e=str(e))
                        del self._messageListeners[parentNodeName][remoteAddressUrl]
        finally:
            self.listenerLock.release()

    def registerInputListener(self, onMessage):
        self._inputListener.append(onMessage)

    def run(self):
        while(self._isActive):
            self.listenerLock.acquire()

            for listener in self._messageListeners.values():
                for consumer in listener.values():
                    consumer.fetch()
            
            self.listenerLock.release()

    def _onMessage(self, messageFlowPattern, msg, origin):
        self.threadLocalStorage.messageFlowPattern = messageFlowPattern
        for listener in self._inputListener:
            try:
                listener(msg, origin)
            except Exception as e:
                log.error("hkube_api message listener through exception: {e}", e=str(e))
        self.threadLocalStorage.messageFlowPattern = []

    def startMessageListening(self):
        self.listeningToMessages = True
        self.listenerLock.acquire()
        try:
            for listener in self._messageListeners.values():
                for consumer in listener.values():
                    if not (consumer.is_alive()):
                        consumer.start()
        finally:
            self.listenerLock.release()

    def sendMessage(self, msg, flowName=None):
        if (self.messageProducer is None):
            raise Exception('Trying to send a message from a none stream pipeline or after close had been applied on algorithm')
        if (self.messageProducer.nodeNames):
            parsedFlow = None
            if (flowName is None):
                if hasattr(self.threadLocalStorage, 'messageFlowPattern') and self.threadLocalStorage.messageFlowPattern:
                    parsedFlow = self.threadLocalStorage.messageFlowPattern
                else:
                    if (self.defaultFlow is None):
                        raise Exception("Streaming default flow is None")
                    flowName = self.defaultFlow
            if not (parsedFlow):
                parsedFlow = self.parsedFlows.get(flowName)
            if (parsedFlow is None):
                raise Exception("No such flow " + flowName)
            self.messageProducer.produce(parsedFlow, msg)

    def stopStreaming(self, force=True):
        self._isActive = False
        if (self.listeningToMessages):
            self.listenerLock.acquire()
            try:
                for listener in self._messageListeners.values():
                    for consumer in listener.values():
                        consumer.close()
                self._messageListeners = dict()
            finally:
                self.listeningToMessages = False
                self.listenerLock.release()
        self._inputListener = []
        if (self.messageProducer is not None):
            self.messageProducer.close(force)
            self.messageProducer = None

    def clearMessageListeners(self):
        self.listenerLock.acquire()
        self._messageListeners = dict()
        self.listenerLock.release()
