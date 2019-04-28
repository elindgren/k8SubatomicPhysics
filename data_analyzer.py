# imports
import numpy as np
import scipy as sp
import scipy.signal
import matplotlib.pyplot as plt


def parse_file_to_dict(file, labelkeys=None):
    d = {}
    for key in labelkeys:
        d[key] = []
    with open(file) as f:
        line_nbr = 0
        for line in f:
            vals = line.split()
            for i, val in enumerate(vals):
                d[labelkeys[i]].append(float(val))  # np append is much slower
            line_nbr += 1
        for key in d:
            d[key] = np.array(d[key])
    return d


# specify file name
filename = "./data/co60_coinc.txt"
# parse .txt-file to dict
data = parse_file_to_dict(filename, ["E1", "E2", "T"])
# Calibrate channel - calibration data from lab
# ******* Det 1
# Peak 1
cal1_chan1 = 3160
cal1_peak1 = 1173.237
# Peak 2
cal1_chan2 = 3590
cal1_peak2 = 1332.501
# calibration values
cal1_1val = cal1_peak1/cal1_chan1  # energy per channel number
cal1_2val = cal1_peak2/cal1_chan2
cal1 = (cal1_1val + cal1_2val)/2  # take the mean
# calibrate channel E1
data["E1"] = data["E1"]*cal1

# *******

# ******* Det 2
# Peak 1
cal2_chan1 = 3025
cal2_peak1 = 1173.237
# Peak 2
cal2_chan2 = 3435
cal2_peak2 = 1332.501
# calibration values
cal2_1val = cal2_peak1/cal2_chan1  # energy per channel number
cal2_2val = cal2_peak2/cal2_chan2
cal2 = (cal2_1val + cal2_2val)/2  # take the mean
# calibrate channel E2
data["E2"] = data["E2"]*cal2
# *******

# Declare subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 15))  # Lower resolution later - this is very high
# *************** No coincidence
# ******* Plot E1
binsE1_nc = len(np.unique(data["E1"]))  # bins with no coincidence
axs[0, 0].hist(data["E1"], binsE1_nc)
axs[0, 0].set_xlabel("E1 - no coin")
# ******* Plot E2
binsE2_nc = len(np.unique(data["E2"]))
axs[0, 1].hist(data["E2"], binsE2_nc)
axs[0, 1].set_xlabel("E2 - no coin")
# ***************

# # *************** With coincidence
# First apply coincidence - loop through data and remove points where T \neq 0
coin_data = {}
bad_idx = []
for idx in range(len(data["E1"])):
    if not data["T"][idx] == 0:
        bad_idx.append(idx)
coin_data["E1"] = np.delete(data["E1"], bad_idx)
coin_data["E2"] = np.delete(data["E2"], bad_idx)

# ******* Plot E1
binsE1_wc = len(np.unique(coin_data["E1"]))
axs[1, 0].hist(coin_data["E1"], binsE1_wc)
axs[1, 0].set_xlabel("E1 - with coin")
# ******* Plot E2
binsE2_wc = len(np.unique(coin_data["E2"]))
axs[1, 1].hist(coin_data["E2"], binsE2_wc)
axs[1, 1].set_xlabel("E2 - with coin")
# ***************

plt.show()
