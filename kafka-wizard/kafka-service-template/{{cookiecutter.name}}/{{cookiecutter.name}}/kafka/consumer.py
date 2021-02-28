# Copyright {% now 'local', '%Y' %} {{ cookiecutter.author }}
# See LICENSE for details.

import json
from typing import List, Any
from confluent_kafka import Consumer, Message


class KafkaConsumer:

    def __init__(self, topics: str, settings: dict, poll_timeout: float = 1.0):
        self._consumer = None
        self._topics = topics
        self._settings = settings
        self._poll_timeout = poll_timeout
        self.start()

    def start(self):
        self._consumer = Consumer(self._settings)
        self._consumer.subscribe(self._topics)

    def stop(self):
        self._consumer.close()

    def consume(self, min_messages: int = 1) -> List[dict]:
        messages = []
        while len(messages) < min_messages:
            msg = self._read_one()
            if msg is not None:
                messages.append(json.loads(msg.value().decode('UTF-8')))
        return messages

    def _read_one(self) -> Message:
        while True:
            try:
                msg = self._consumer.poll(self._poll_timeout)
                if msg is not None:
                    if not msg.error():
                        return msg
            except Exception as ex:
                return None