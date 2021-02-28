# Copyright {% now 'local', '%Y' %} {{ cookiecutter.author }}
# See LICENSE for details.

# Kafka configuration
KAFKA_NUM_TRIES = {{ cookiecutter.kafka.num_tries }}
KAFKA_INPUT_TOPICS = {{ cookiecutter.kafka.input_topics }}
KAFKA_OUTPUT_TOPICS = {{ cookiecutter.kafka.output_topics }}
KAFKA_GROUP_ID = "{{ cookiecutter.kafka.group_id }}"
KAFKA_BROKER = "{{ cookiecutter.kafka.broker }}"
KAFKA_DELIVERY_TIMEOUT = {{ cookiecutter.kafka.delivery_timeout }}

KAFKA_SETTINGS = {
    'group.id': KAFKA_GROUP_ID,
    'retries': KAFKA_NUM_TRIES,
    'bootstrap.servers': KAFKA_BROKER,
    'default.topic.config': {
        'auto.offset.reset': 'earliest',
        'delivery.timeout.ms': KAFKA_DELIVERY_TIMEOUT
    }
}
