
import uproot
import numpy as np
import matplotlib.pyplot as plt

print("Loading data...")
f = uproot.open("<file path. root>")
tree = f["Data_R"]
ts = tree["Timestamp"].array(library="np").astype(np.int64)
ch = tree["Channel"].array(library="np")

# split into the two channels (each is already time-sorted)
t0 = ts[ch == 0]
t1 = ts[ch == 1]
print(f"ch0: {len(t0)} hits,  ch1: {len(t1)} hits") 

# for each ch0 hit, find the nearest ch1 hit in time
# searchsorted gives insertion index; check the neighbor on each side
idx = np.searchsorted(t1, t0)
idx = np.clip(idx, 1, len(t1) - 1)      # keep indices valid
left  = t1[idx - 1]
right = t1[idx]
# pick whichever neighbor is closer to each t0
dt_left  = t0 - left      # positive
dt_right = t0 - right     # negative
dt = np.where(np.abs(dt_left) < np.abs(dt_right), dt_left, dt_right)

# coincidence window: keep pairs within +/- 5 ns  (5000 ps)
WINDOW = 5000  # picoseconds -- adjust if units differ
mask = np.abs(dt) < WINDOW
dt_coinc = dt[mask]
print(f"Coincidences within +/-{WINDOW} ps: {len(dt_coinc)}")

# histogram of time differences -- THE coincidence timing peak
plt.hist(dt_coinc, bins=200, histtype="step")
plt.xlabel("Time difference ch0 - ch1 (ps)")
plt.ylabel("Coincidence counts")
plt.title("Na-22 coincidence timing spectrum")
plt.tight_layout()
plt.savefig("<DESTINATIONPATH.png>", dpi=150)
print("Saved coincidence_dt.png")
plt.show()
