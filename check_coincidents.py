
import uproot
import numpy as np

f = uproot.open("/* file path */")
tree = f["Data_R"]
ts = tree["Timestamp"].array(library="np")
ch = tree["Channel"].array(library="np")

print("First 20 (timestamp, channel) pairs:")
for i in range(20):
    print(f"  {ts[i]:>15}  ch{ch[i]}")

print("\nAre timestamps sorted?", np.all(np.diff(ts) >= 0))
print("Timestamp dtype:", ts.dtype)
diffs = np.diff(ts.astype(np.int64))
print("Median gap between consecutive hits:", np.median(diffs))
print("Min gap:", diffs.min(), " Max gap:", diffs.max())
