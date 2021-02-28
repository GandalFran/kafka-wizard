
from {{cookiecutter.service_name}} import config
from {{cookiecutter.service_name}}.processing import DataProcessor

{% if cookiecutter.flow.consumer == True %}
from {{cookiecutter.service_name}}.kafka import KafkaConsumer
{%- endif %}
{% if cookiecutter.flow.producer == True %}
from {{cookiecutter.service_name}}.kafka import KafkaProducer
{%- endif %}

{% if not cookiecutter.flow.producer == True %}
def generate_data():
	return {'mesage': 'Sample generated data'}
{%- endif %}

{% if not cookiecutter.flow.consumer == True %}
def manage_data(data):
	print(f'managing data {data}')
{%- endif %}


{% if cookiecutter.flow.consumer == True %}
consumer = KafkaConsumer(config.KAFKA_INPUT_TOPIC, config.KAFKA_SETTINGS)
{%- endif %}
{% if cookiecutter.flow.producer == True %}
producer = KafkaProducer()
{%- endif %}
procesor = DataProcessor()


def behaviour():
	# obtain data
	{% if cookiecutter.flow.consumer == True %}
	data = consumer.consume()
	{% else %}
	data = generate_data()
	{%- endif %}
	if data is None or not data:
		return

	# manage data
	data = p.process_data(data)

	# send data
	{% if cookiecutter.flow.producer == True %}
	producer.produce(data)	
	{% else %}
	manage_data(data)
	{%- endif %}


def run():
	while True:
		behaviour()
