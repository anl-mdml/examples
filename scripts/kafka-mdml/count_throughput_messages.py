import mdml_client as mdml

consumer = mdml.kafka_mdml_consumer(
    topics = ["mdml-example-throughput"],
    group = "mdml-examples-throughput",
    kafka_host = "192.168.39.2",
    kafka_port = 9093,
    schema_host = "192.168.39.2"
)

i = 0

for msg in consumer.consume():
    i += 1
    if i%1000==0:
        print(f"received {i} messages")

print(f"Messages counted: {i}")
