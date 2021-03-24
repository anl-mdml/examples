import numpy as np
from scipy.integrate import odeint

N = 5 # Number of variables
F = 8 # Forcing

def L96(x, t):
    """ Lorenz 9 model with constant forcing"""
    # Set up vector
    d = np.zeros(N)

    # Loop over indices (with operations and
    # Python underflow indexing handling edge cases)
    for i in range(N):
        d[i] = (x[(i + 1) % N] - x[i - 2]) * x[i - 1] - x[i] + F
        
    return d

# Initial state (equilibrium)
x0 = F * np.ones(N)

# Add small perturbation to the first variable
x0[0] += 0.01

t = np.arange(0.0, 30.0, 0.01)

x = odeint(L96, x0, t)

import time
import mdml_client as mdml

exp = mdml.experiment("TUTORIAL", "tutorial", "tutorial", "merfpoc.egs.anl.gov")
exp.add_config(experiment_run_id="lorenz96", auto=True)
exp.send_config()

time.sleep(1) # Pause to let configuration be ingested

x_labels = {'time': mdml.unix_time(), 'x1':x[0][0], 'x2':x[0][1],'x3':x[0][2],'x4':x[0][3],'x5':x[0][4]}

exp.publish_data("LORENZ", x_labels, add_device=True)

time.sleep(1)

try:
    for i in x[1:]:
        dat = i
        dat = np.insert(dat,0, mdml.unix_time())
        exp.publish_data("LORENZ", dat)
        time.sleep(0.5)
except: 
    print("Stopping...")
finally:
    exp.reset()
    exp.disconnect()