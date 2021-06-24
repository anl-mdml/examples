import glob
import time
import mdml_client as mdml

images = glob.glob("images/*.PLIF1.TIF")

producer = mdml.kafka_mdml_producer(
    topic = "mdml-example-plif-multipart",
    schema = "example_plif_multipart.json")

start = time.time()
print(f"streaming {len(images)} images")
print(f"start: {start}")
for img in images:
    chunks = mdml.chunk_file(img, 100000)
    for chunk in chunks:
        producer.produce(chunk)
producer.flush()
end = time.time()
print(f"end: {end}")