import glob
import math
import time
import base64
import mdml_client as mdml

images = glob.glob("images/*.PLIF1.TIF")

producer = mdml.kafka_mdml_producer(
    topic = "mdml-example-plif-multipart",
    schema = "example_plif_multipart.json")

def send_image(fn, part_size, producer):
    with open(fn, 'rb') as f:
        dat_bytes = f.read()
    dat_b64 = base64.b64encode(dat_bytes).decode('utf-8')
    dat_len = len(dat_b64)
    total_parts = math.ceil(dat_len/part_size)
    part = 1
    while len(dat_b64):
        part_bytes = dat_b64[0:part_size]
        dat_b64 = dat_b64[part_size:]
        dat = {
            'b64': part_bytes,
            'part': f'{part}.{total_parts}',
            'filename': fn
        }
        producer.produce(dat)
        part += 1
    producer.flush()

start = time.time()
print(start)
for img in images:
    send_image(img, 100000, producer)
end = time.time()

