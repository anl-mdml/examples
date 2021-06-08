import mdml_client as mdml

consumer = mdml.kafka_mdml_consumer(
    topics = ["mdml-examples-throughput"],
    group = "mdml-examples-throughput")

i = 0

for msg in consumer.consume():
    i += 1

print(f"Messages counted: {i}")
