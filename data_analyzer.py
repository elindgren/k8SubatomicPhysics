# imports
import numpy as np
import scipy as sp
import scipy.signal
import matplotlib
import matplotlib.pyplot as plt


def parse_file_to_dict(file, labelkeys=None):
    d = {}
    for key in labelkeys:
        d[key] = []
    with open("./data/" + file + ".txt") as f:
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
compare_coin = False
filename = "na22_coinc_90"
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
if compare_coin:
    fig, axs = plt.subplots(1, 2, sharey=True, figsize=(10, 6))  # Lower resolution later - this is very high
    axs[0].set_ylim(0,500)
    axs[0].set_ylabel("Antal")
    axs[1].set_ylim(0,500)
    # *************** No coincidence
    # ******* Plot E1
    binsE1_nc = len(np.unique(data["E1"]))  # bins with no coincidence
    axs[0].hist(data["E1"], binsE1_nc, log=False)
    axs[0].set_xlabel("Energi, i KeV \n Utan koincidens")
    # ******* Plot E2
    # binsE2_nc = len(np.unique(data["E2"]))
    # axs[0,1].hist(data["E2"], binsE2_nc)
    # axs[0,1].set_xlabel("E2 - no coin")
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
    axs[1].hist(coin_data["E1"], binsE1_wc, log=False)
    axs[1].set_xlabel("Energi, i KeV \n Med koincidens")
    # ******* Plot E2
    # binsE2_wc = len(np.unique(coin_data["E2"]))
    # axs[1, 1].hist(coin_data["E2"], binsE2_wc)
    # axs[1, 1].set_xlabel("E2 - with coin")
    # ***************
    # Increase font size etc.
    for i in range(len(axs)):
        #axs[i].set_linewdith(10)
        for idx, item in enumerate(([axs[i].title, axs[i].xaxis.label, axs[i].yaxis.label] +
                     axs[i].get_xticklabels() + axs[i].get_yticklabels())):
            if idx < 4:
                item.set_fontsize(16)
            else:
                item.set_fontsize(14)
else:
    fig, axs = plt.subplots(1,1,figsize=(6, 6))
    axs.set_ylim(0, 500)
    axs.set_ylabel("Antal")
    axs.set_ylim(0, 500)
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
    axs.hist(coin_data["E1"], binsE1_wc, log=False)
    axs.set_xlabel("Energi, i KeV \n Med koincidens")

    for idx, item in enumerate(([axs.title, axs.xaxis.label, axs.yaxis.label] +
                                axs.get_xticklabels() + axs.get_yticklabels())):
        if idx < 4:
            item.set_fontsize(16)
        else:
            item.set_fontsize(14)

plt.savefig(filename+"_hist.png", format="png", bbox_inches='tight')
plt.show()

# Plot coincidence spectrum
# Declare subplots
if compare_coin:
    fig, axs = plt.subplots(1, 2, sharey=True, figsize=(10, 6))  # Lower resolution later - this is very high
    axs[0].set_ylabel("Antal")
    # *************** No coincidence
    # ******* Plot E1
    axs[0].scatter(data["E1"], data["E2"], s=0.001)
    axs[0].set_xlabel("Detektor A, Energi i KeV \n Utan koincidens")
    axs[0].set_ylabel("Detektor B, Energi i KeV")

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
    axs[1].scatter(coin_data["E1"], coin_data["E2"], s=0.001)
    axs[1].set_xlabel("Detektor A, Energi i KeV \n Med koincidens")
    axs[1].set_ylabel("Detektor B, Energi i KeV")

    # Increase font size etc.
    for i in range(len(axs)):
        for idx, item in enumerate(([axs[i].title, axs[i].xaxis.label, axs[i].yaxis.label] +
                     axs[i].get_xticklabels() + axs[i].get_yticklabels())):
            if idx < 4:
                item.set_fontsize(16)
            else:
                item.set_fontsize(14)
else:
    fig, axs = plt.subplots(1,1,figsize=(6, 6))
    axs.set_ylabel("Antal")

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
    axs.scatter(coin_data["E1"], coin_data["E2"], s=0.01)
    axs.set_ylim(0,3000)
    axs.set_xlim(0,3000)
    axs.set_xlabel("Detektor A, Energi i KeV")
    axs.set_ylabel("Detektor B, Energi i KeV")

    for idx, item in enumerate(([axs.title, axs.xaxis.label, axs.yaxis.label] +
                                axs.get_xticklabels() + axs.get_yticklabels())):
        if idx < 4:
            item.set_fontsize(16)
        else:
            item.set_fontsize(14)
plt.savefig(filename+"_coin.png", format="png", bbox_inches='tight')

plt.show()