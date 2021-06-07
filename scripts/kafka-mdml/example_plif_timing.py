import glob
import time
import mdml_client as mdml

# Now that the FuncX function is running and ready to accept data, we will start sending data
s3_client = mdml.kafka_mdml_s3_client(
    topic = 'mdml-examples-plif', # S3 bucket is derived from topic as mdml-examples
    s3_endpoint = "https://s3.it.anl.gov:18082",
    s3_access_key = "JNLZP8P0XJE05KSO01LF",
    s3_secret_key = "t3+1pwXh6DmiBdY4AKJuKutlIpR5FzxiqNcewu94"
)

images = glob.glob("images/*.PLIF1.TIF")

start = time.time()
for img in images:
    s3_client.produce(
        filepath = img, 
        obj_name = img
    )
end = time.time()
print(f'Seconds to send 500 MB (50x10MB images) to S3 {end-start}')
