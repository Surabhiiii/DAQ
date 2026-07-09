import uproot
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

f = uproot.open(r"C:\Users\surab\Downloads\DAQ\DataR_run7_22Na_polymer_foam_cups.root")
tree = f["Data_R"]
energy  = tree["Energy"].array(library="np")
channel = tree["Channel"].array(library="np")

for ch in [0, 1]:
    e = energy[channel == ch]
    counts, edges = np.histogram(e, bins=2048, range=(0, 16384))
    centers = (edges[:-1] + edges[1:]) / 2

    detector_num = ch + 1   # channel 0 -> Detector 1, channel 1 -> Detector 2

    plt.figure(figsize=(10, 5))
    plt.plot(centers, counts, drawstyle="steps-mid", color="black", linewidth=0.8)
    plt.xlabel("ADC Unit")
    plt.ylabel("Counts / channel")
    plt.title(f"Energy Deposition - Detector {detector_num}")

    stats = f"Entries  {len(e)}\nMean     {e.mean():.0f}\nStd Dev  {e.std():.0f}"
    plt.text(0.98, 0.98, stats, transform=plt.gca().transAxes,
             ha="right", va="top", family="monospace",
             bbox=dict(boxstyle="square", facecolor="white", edgecolor="black"))

    plt.tight_layout()
    plt.savefig(rf"C:\Users\surab\Downloads\Energy_Detector{detector_num}.png", dpi=150)
    plt.close()
    print(f"Detector {detector_num}: {len(e)} entries, saved Energy_Detector{detector_num}.png")
