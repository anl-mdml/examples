import time
from funcx.sdk.client import FuncXClient

fxc = FuncXClient()

def mdml_example_integer_sum(params):
    import time
    import mdml_client as mdml
    consumer = mdml.kafka_mdml_consumer(
        topics = ["mdml-example-integer", "mdml-example-integer-sum-funcx"],
        group = "mdml-example-integer-sum-funcx")
    # Creating producer for analysis results
    results_schema = {
        "$schema": "http://merf.egs.anl.gov/mdml-example-integer-sum-data-schema#",
        "title": "ExampleIntegerSum",
        "description": "Schema for MDML with Kafka example integer data from the sum analysis",
        "type": "object",
        "properties": {
            "id": {
                "description": "ID of the data point",
                "type": "number"
            },
            "time": {
                "description": "Unix time the data point occurred",
                "type": "number"
            },
            "sum": {
                "description": "Sum of three random integers",
                "type": "number"
            }
        },
        "required": [ "id", "time", "sum" ]
    }
    producer = mdml.kafka_mdml_producer(
        topic = "mdml-example-integer-sum",
        schema = results_schema)
    for msg in consumer.consume():
        topic = msg['topic']
        value = msg['value']
        if topic == 'mdml-example-integer':
            producer.produce({
                'id': value['id'],
                'time': time.time(),
                'sum': int(value['int1']) + int(value['int2']) + int(value['int3'])
            })
        elif topic == "mdml-example-integer-sum-funcx":
            if value['stop']:
                return "done"

func_uuid = fxc.register_function(mdml_example_integer_sum, 
    description="Example function for topic mdml-example-integer.")

# MERF GPU Server Endpoint
merf_ep_uuid = "19a6506e-311d-4a25-bef5-7ede4af87c76"

# Send task to FuncX
task_id = fxc.run(
    {},
    endpoint_id=merf_ep_uuid,
    function_id=func_uuid
)

while True:
    try:
        result = fxc.get_result(task_id)
        print("result")
        print(result)
        time.sleep(5)
    except KeyboardInterrupt:
        print("Done.")
        break
    except Exception as e:
        print(f"Exception: {e}")
        time.sleep(3)