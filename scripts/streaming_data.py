import sys
import time
import json
import random
import mdml_client as mdml # pip install mdml_client #

print("**************************************************************************")
print("*** This example will publish data once every second for 20 seconds.   ***")
print("*** Press Ctrl+C to stop the example.                                  ***")
print("**************************************************************************")
time.sleep(5)

# Approved experiment ID (supplied by MDML administrators - will not work otherwise)
Exp_ID = 'TUTORIAL'
# MDML message broker host
host = 'merfpoc.egs.anl.gov'
# MDML username and password
username = 'tutorial'
password = 'tutorial'


# Create a configuration for your experiment
config = {
    "experiment": {
        "experiment_id": "TUTORIAL",
        "experiment_notes": "example.py file for MDML python package",
        "experiment_devices": ["DEVICE_A", "DEVICE_B"],
        "delete_db_data_when_reset": True
    },
    "devices": [
        {
            "device_id": "DEVICE_A",
            "device_name": "Test device A",
            "device_output": "random data",
            "device_output_rate": 1, # in Hertz
            "device_data_type": "text/numeric",
            "device_notes": "Random data generated and streamed for example purposes",
            "headers" : [
                "time",
                "variable1",
                "variable2",
                "variable3",
                "variable4",
                "variable5"
            ],
            "data_types" : [
                "numeric",
                "numeric",
                "numeric",
                "numeric",
                "numeric",
                "numeric"
            ],
            "data_units" : [
                "NA",
                "NA",
                "NA",
                "NA",
                "NA",
                "NA"
            ]
        },
        {
            "device_id": "DEVICE_B",
            "device_name": "Test device B",
            "device_output": "random data",
            "device_output_rate": 1, # in Hertz
            "device_data_type": "text/numeric",
            "device_notes": "Random data generated and streamed for example purposes",
            "headers" : [
                "time",
                "variable1",
                "variable2",
                "variable3"
            ],
            "data_types" : [
                "numeric",
                "numeric",
                "numeric",
                "numeric"
            ],
            "data_units" : [
                "NA",
                "NA",
                "NA",
                "NA"
            ]
        }
    ]
}

# Create MDML experiment
My_MDML_Exp = mdml.experiment(Exp_ID, username, password, host)

# Sleep to let debugger thread set up
time.sleep(1)

# Add and validate a configuration for the experiment
My_MDML_Exp.add_config(config, 'mdml_examples')
# NOTE: The config variable created earlier is to illustrate the 
# relevant configuration information for this example. The actual configuration
# sent to the MDML contains devices for all examples so that different examples can 
# be run together. However, it is not recommended due to MDML details that are
# explained in the multiple_clients example scripts.
# Using the line below is also valid 
# My_MDML_Exp.add_config(config, 'mdml_examples')

# Send configuration file to the MDML
My_MDML_Exp.send_config() # this starts the experiment

# Sleep to let MDML ingest the configuration
time.sleep(2)

def random_data(size):
    dat = []
    for _ in range(size):
        dat.append(str(random.random()))
    return dat

reset = False
try:
    i = 0
    while True:
        while i < 200:
            # Create random data
            deviceA_data = '\t'.join(random_data(5))
            print(f'Device A: {deviceA_data}')
            # Send data
            My_MDML_Exp.publish_data('DEVICE_A', f"{time.time()}\t{deviceA_data}", '\t')
            
            # Repeat for Device B
            deviceB_data = '\t'.join(random_data(3))
            print(f'Device B: {deviceB_data}')
            My_MDML_Exp.publish_data('DEVICE_B', f"{time.time()}\t{deviceB_data}", '\t')

            # Sleep to publish data once a second
            time.sleep(1)
            i += 1
        if not reset:
            print("Ending MDML experiment")
            My_MDML_Exp.reset()
            reset = True
except KeyboardInterrupt:
    if not reset:
        My_MDML_Exp.reset()
    My_MDML_Exp.disconnect()
