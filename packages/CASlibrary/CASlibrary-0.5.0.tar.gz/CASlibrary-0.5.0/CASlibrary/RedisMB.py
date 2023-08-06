import json
import os
import uuid

import redis

from . import Logger


class RedisMB:
    def __init__(self, data=None):
        self.logger = Logger.Logger(self.__class__.__name__).getLogger()

        if data is not None:
            host = data["REDIS_HOST"]
            port = data["REDIS_PORT"]
            db = data["REDIS_DB"]
        else:
            host = os.getenv('REDIS_HOST', '127.0.0.1')
            port = os.getenv('REDIS_PORT', 6379)
            db = os.getenv('REDIS_DB', 0)
        self.r = redis.Redis(host,
                             port=port,
                             db=db,
                             health_check_interval=15,
                             socket_connect_timeout=10)
        self.p = self.r.pubsub(ignore_subscribe_messages=True)
        self.subthread = None

        self.logger.info("Connecting to Redis DB on {}:{} DB: {}".format(host, port, db))
        self.r.ping()
        self.logger.info("Connected successfully to Redis DB on {}:{} DB: {}".format(host, port, db))

    def _publish_message(self, queue, message):
        messageToSend = {'uuid': str(uuid.uuid1()),
                         'type': queue,
                         'message': message}
        messageToSend = json.dumps(messageToSend,
                                   separators=(',', ':'),
                                   sort_keys=True,
                                   indent=None)
        self.logger.trace("Sending redis message: {}".format(messageToSend))
        self.r.publish(queue, messageToSend)

    def decodeMessage(self, message):
        return json.loads(message['data'])

    def exit(self):
        self.r.close()

    def input(self, messagetype, data):
        self._publish_message("input", {"type": messagetype, "data": data})

    def alert(self, messagetype, data):
        self._publish_message("alert", {"type": messagetype, "data": data})

    def error(self, messagetype, data):
        self._publish_message("error", {"type": messagetype, "data": data})

    def test(self, messagetype, data):
        self._publish_message("test", {"type": messagetype, "data": data})

    def subscribeToType(self, type, callback):
        self.p.subscribe(**{type: callback})
        if self.subthread is None:
            self.subthread = self.p.run_in_thread(sleep_time=0.01)
        return self.subthread

    def psubscribeToType(self, pattern, callback):
        self.p.psubscribe(**{pattern: callback})
        if self.subthread is None:
            self.subthread = self.p.run_in_thread(sleep_time=0.01)
        return self.subthread
