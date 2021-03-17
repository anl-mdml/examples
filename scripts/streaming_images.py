# Parameters to run the example
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="MDML instance host",
                        required=True)
parser.add_argument("--username", help="MDML username",
                        required=True)
parser.add_argument("--password", help="MDML password",
                        required=True)
args = parser.parse_args()

import time
import mdml_client as mdml

exp = mdml.experiment("TUTORIAL", args.username, args.password, args.host)
exp.add_config(auto=True)
exp.send_config()
time.sleep(1)

# Generating random images
import numpy as np
import cv2
from base64 import b64encode
def random_image(width,height):
    random_image = np.random.randint(255, size=(height,width,3), dtype=np.uint8)    
    _, img = cv2.imencode('.png', random_image)
    img_bytes = img.tobytes()
    img_b64bytes = b64encode(img_bytes)
    img_byte_string = img_b64bytes.decode('utf-8')
    return img_byte_string

curr_time = mdml.unix_time() # True for integer return instead of string
# Sending image
exp.publish_image(device_id="IMAGE", img_byte_string=random_image(800,600), 
                  filename='test_image1.png', timestamp=curr_time, add_device=True)

try:
    while True:
        exp.publish_image("IMAGE", random_image(800,600), timestamp=mdml.unix_time())
        time.sleep(1)
except KeyboardInterrupt:
    print("Quitting")
finally:
    exp.reset()
    time.sleep(1)
    exp.disconnect()
