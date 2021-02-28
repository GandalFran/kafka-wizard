
from {{cookiecutter.name}} import config
from {{cookiecutter.name}}.processing import DataProcessor
{% if cookiecutter.flow.consumer == "yes" %}from {{cookiecutter.name}}.kafka import KafkaConsumer{%- endif %}
{% if cookiecutter.flow.producer == "yes" %}from {{cookiecutter.name}}.kafka import KafkaProducer{%- endif %}

{% if cookiecutter.flow.consumer == "no" %}
def generate_data():
	from time import sleep
	sleep(10)
	return {'mesage': 'Sample generated data'}
{%- endif %}
{% if not cookiecutter.flow.producer == "no" %}
def manage_data(data):
	print(f'managing data {data}')
{%- endif %}

procesor = DataProcessor()
{% if cookiecutter.flow.consumer == "yes" %}consumer = KafkaConsumer(config.KAFKA_INPUT_TOPICS, config.KAFKA_SETTINGS){%- endif %}
{% if cookiecutter.flow.producer == "yes" %}producer = KafkaProducer(config.KAFKA_OUTPUT_TOPICS, config.KAFKA_SETTINGS){%- endif %}


def behaviour():
	# obtain data
	{% if cookiecutter.flow.consumer == "yes" %}data = consumer.consume(){% else %}data = generate_data(){%- endif %}
	if data is None or not data:
		return

	# manage data
	data = procesor.process(data)

	# send data
	{% if cookiecutter.flow.producer == "yes" %}producer.produce(data)	{% else %}manage_data(data){%- endif %}


def run():
	while True:
		behaviour()

if __name__ == '__main__':
	run()