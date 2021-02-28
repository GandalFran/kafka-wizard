# Copyright {% now 'local', '%Y' %} {{ cookiecutter.author }}
# See LICENSE for details.

import json
from typing import List, Any
from confluent_kafka import Producer


class KafkaProducer:

    def __init__(self, topics: str, settings: dict):
        self._producer = None
        self._topics = topics
        self._settings = settings
        self.start()

    def delivery_report(self, err: Exception, msg: Any):
        if err is not None:
            print(f"[delivery_report] error occurred during a message send {err}")

    def start(self):
        self._settings['on_delivery'] = self.delivery_report
        self._producer = Producer(self._settings)

    def stop(self):
        self._producer.flush()

    def produce(self, data: dict):
        try:
            data = json.dumps(data)
            for t in self._topics:
                self._producer.produce(t, value=data)
            self._producer.flush()
        except Exception as ex:
            print(f"[write] error occurred on msg send {ex}")

    def flush(self):
        self._producer.flush()