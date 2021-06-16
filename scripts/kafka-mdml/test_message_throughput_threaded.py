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
parser.add_argument("--threads", help="Number of threads",
                        required=True)
args = parser.parse_args()

import time
import mdml_client as mdml
import threading, queue

msg_count_q = queue.Queue()

def work(args, q):
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

    q.put(i)
    print(f"Sent {i} messages with a random part size of {args.bytes} bytes in {end-start} seconds.")
    print(f"AVG Messages Per Second: {i/(end-start)}")
    print(f"AVG MB/sec {(i/(end-start))*(int(args.bytes)/1000000)}")

threads = []
for i in range(int(args.threads)):
    thread = threading.Thread(target=work, kwargs={'args':args, 'q': msg_count_q}, daemon=True)
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

num_msgs = 0
while not msg_count_q.empty():
    num_msgs += int(msg_count_q.get())

print(f"Sent {num_msgs} messages with a random part size of {args.bytes} bytes in {args.seconds} seconds.")
print(f"AVG Messages Per Second: {num_msgs/int(args.seconds)}")
print(f"AVG MB/sec: {(num_msgs/int(args.seconds))*(int(args.bytes)/1000000)}")