import sys
sys.path.append(".")

import mdml_client as mdml

consumer = mdml.kafka_mdml_consumer(
    topics = ["mdml-example-integer", "mdml-example-integer-sum", "mdml-example-integer-sum-func"],
    group = "mdml-example-integer")

for msg in consumer.consume():
    print(msg)
