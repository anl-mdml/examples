import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Kafka hostname",
                        required=True)
parser.add_argument("--port", help="Kafka port",
                        required=True)
parser.add_argument("--srhost", help="Schema registry hostname",
                        required=True)
parser.add_argument("--seconds", help="Number of seconds to send messages",
                        required=True)
parser.add_argument("--bytes", help="Number of bytes for the message",
                        required=True)
args = parser.parse_args()

import time
import mdml_client as mdml

producer = mdml.kafka_mdml_producer(
    topic = "mdml-example-throughput",
    schema = "example_throughput.json",
    kafka_host = args.host,
    kafka_port = int(args.port),
    schema_host = args.srhost
)

dat = {
    'filler': "A" * int(args.bytes)
}
i=0
start = time.time()
end_time = start + int(args.seconds)
while time.time() < end_time:
    producer.produce(dat)
    i += 1
    if i % 1000 == 0:
        producer.flush()
end = time.time()

print(f"Sent {i} messages with a random part size of {args.bytes} bytes in {end-start} seconds.")
print(f"AVG Messages Per Second: {i/(end-start)}")
