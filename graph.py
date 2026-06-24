import uproot
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("Opening file...")
f = uproot.open("/Users/ashwani/Downloads/DataR_run7_22Na_polymer_foam_cups.root")
tree = f["Data_R"]

print("Reading branches...")
energy  = tree["Energy"].array(library="np")
channel = tree["Channel"].array(library="np")

print("Channels present:", np.unique(channel))

for ch in np.unique(channel):
    plt.hist(energy[channel == ch], bins=2048, histtype="step", label=f"Channel {ch}")

plt.xlabel("Energy (ADC channels)")
plt.ylabel("Counts")
plt.yscale("log")
plt.legend()
plt.title("Na-22 spectrum by detector channel")
plt.tight_layout()
plt.savefig("/Users/ashwani/na22-analysis/na22_by_channel.png", dpi=150)
print("Saved plot to na22_by_channel.png")
