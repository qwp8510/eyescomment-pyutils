import sysv_ipc
import logging


logger = logging.getLogger(__name__)


class MessageHelper():
    def __init__(self, queue_key=8020):
        self._queue_key = queue_key
        self._message_queue = None

    @property
    def message_queue(self):
        try:
            if not self._message_queue:
                self._message_queue = sysv_ipc.MessageQueue(
                    self._queue_key, sysv_ipc.IPC_CREAT, max_message_size=8192)
        except sysv_ipc.ExistentialError:
            logger.warning('IPC message queue exist!')
        except Exception as e:
            logger.error('message_queue Exception: {}'.format(e))

        return self._message_queue

    def publish(self, msg=None):
        if not self.message_queue:
            logger.error('publish message error due to message_queue is None')
            return
        message = msg
        try:
            self.message_queue.send(message)
        except Exception as e:
            logger.error('publish ipc message to queue fail: {}'.format(e))

    def consume(self):
        try:
            (message, priority) = self.message_queue.receive()
            return True, message, priority
        except Exception as e:
            logger.error('consume ipc message from queue fail: {}'.format(e))
            return False, None, None
