import time
import base64
import mdml_client as mdml

consumer = mdml.kafka_mdml_consumer(
    topics = ["mdml-example-plif-multipart"],
    group = "mdml-example-plif-multipart")

files = {}
for msg in consumer.consume():
    value = msg['value']
    fn = value['filename']
    part_info = value['part'].split('.')
    if fn in files:
        files[fn][part_info[0]] = value['b64']
    else:
        files[fn] = {
            'parts': part_info[1],
            part_info[0]: value['b64'] 
        }
    if len(files[fn].keys()) == (int(files[fn]['parts']) + 1):
        print("all parts received")
        dat = ''
        for i in range(int(files[fn]['parts'])):
            dat += files[fn][str(i+1)]
        dat_bytes = base64.b64decode(dat)
        with open(f'streamed/{fn.split("/")[1]}', 'wb') as f:
            f.write(dat_bytes)
        # print(files[fn].keys())
        print(time.time())
        # del files[fn]