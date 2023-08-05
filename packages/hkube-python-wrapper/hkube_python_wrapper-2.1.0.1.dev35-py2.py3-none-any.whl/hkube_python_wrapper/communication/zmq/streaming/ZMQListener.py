import time
import zmq
import uuid
import threading
from hkube_python_wrapper.util.logger import log
from hkube_python_wrapper.communication.zmq.streaming.consts import *

CYCLE_LENGTH_MS = 100
HEARTBEAT_INTERVAL = 5
HEARTBEAT_LIVENESS = HEARTBEAT_INTERVAL * HEARTBEAT_INTERVAL
INTERVAL_INIT = 1
INTERVAL_MAX = 32

lock = threading.Lock()

shouldPrint = False

class ZMQListener(object):

    def __init__(self, remoteAddress, onMessage, encoding, consumerType):
        self._encoding = encoding
        self._onMessage = onMessage
        self._consumerType = self._encoding.encode(consumerType, plainEncode=True)
        self._remoteAddress = remoteAddress
        self._active = False
        self._worker = None
        self._context = None
        self.ready = False

    def _worker_socket(self, remoteAddress, context=None):
        """Helper function that returns a new configured socket
           connected to the Paranoid Pirate queue"""
        if not context:
            context = zmq.Context(1)
        self._context = context
        identity = str(uuid.uuid4()).encode()
        worker = self._context.socket(zmq.DEALER)  # DEALER
        worker.setsockopt(zmq.LINGER, 0)
        worker.setsockopt(zmq.IDENTITY, identity)
        worker.connect(remoteAddress)
        log.info("zmq listener connecting to {addr}", addr=remoteAddress)
        self._send(worker, PPP_INIT)
        return worker

    def _send(self, worker, signal, result=PPP_EMPTY):
        if(worker):
            arr = [signal, self._consumerType, result]
            worker.send_multipart(arr)

    def _handleAMessage(self, frames):
        encodedMessageFlowPattern, header, message = frames  # pylint: disable=unbalanced-tuple-unpacking
        messageFlowPattern = self._encoding.decode(value=encodedMessageFlowPattern, plainEncode=True)
        return self._onMessage(messageFlowPattern, header, message)

    def start(self):
        self._worker = self._worker_socket(self._remoteAddress)
        self._active = True

    def fetch(self):
        try:
            if(self._worker is None):
                return

            if(self.ready is False):
                self.ready = True
                self._send(self._worker, PPP_READY)

            result = self._worker.poll(CYCLE_LENGTH_MS) 

            if result == zmq.POLLIN:
                frames = self._worker.recv_multipart()

                if len(frames) == 3:
                    self._send(self._worker, PPP_READY)
                    result = self._handleAMessage(frames)
                    self._send(self._worker, PPP_DONE, result)
                else:
                    self.ready = False
              

        except Exception as e:
            if (self._active):
                log.error('Error during poll of {addr}, {e}', addr=str(self._remoteAddress), e=str(e))

    def close(self):
        if not (self._active):
            log.warning("Attempting to close inactive ZMQListener")
        else:
            self._active = False
            self._send(self._worker, PPP_DISCONNECT)
            self._worker.close()
            self._context.destroy()
