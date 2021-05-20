import sys
sys.path.append(".")
import time
import random
import mdml_client as mdml

producer = mdml.kafka_mdml_producer(
    topic = "mdml-example-integer",
    schema = "example_integer.json")
stop_analysis_producer = mdml.kafka_mdml_producer(
    topic = "mdml-example-integer-sum-funcx",
    schema = "stop_funcx.json")

try:
    i = 0
    while True:
        dat = {
            'id': i,
            'time': time.time(),
            'int1': random.randint(0,25),
            'int2': random.randint(25,50),
            'int3': random.randint(50,100) 
        }
        producer.produce(dat)
        print("sent message")
        time.sleep(5)
        i += 1
except KeyboardInterrupt:
    print("Pausing 5 seconds before sending a kill signal to any FuncX functions")
    time.sleep(5)
    stop_analysis_producer.produce({"stop": True})
    print("Done.")
