# Kafka wizard

Kafka flow generation tool.

## Usage 
1. Install package with `python -m pip install . --upgrade`.
2. Generate a diagram in draw.io and export it in XML (it's very **important to not mark** the **compressed** option).
3. Generate the components with `kafkawizard -i diagram.xml -o output_folder -a the_author -m the_author_mail@mail.mail -b kafka_broker_address:9092`.

## How to create diagrams supported by the wizard
1. create the components with blocks.
2. join the components with arrow (ensure arrows are attached).
3. give name to the components.

**Note**: when multiple components read from one topic, if all are joined with normal arrows, all messages are received in each one. But in the ones joined with dotted arrows, the messages are distributed among all.

An example of functional diagram can be found <a href='https://github.com/GandalFran/MASI-examples/blob/main/tests/test.xml'>here</a>.

<p align="center">
  <img src="https://github.com/GandalFran/MASI-examples/blob/main/tests/test.png">
</p>
