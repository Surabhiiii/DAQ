
import uproot
import numpy as np

f = uproot.open("/FILEPATH.root")
tree = f["Data_R"]
ts = tree["Timestamp"].array(library="np").astype(np.int64)
ch = tree["Channel"].array(library="np")

# how many of each channel, and where they sit
print("Total hits:", len(ts))
print("ch0 count:", np.sum(ch==0), " ch1 count:", np.sum(ch==1))

# find where the channel changes as we go down the list
changes = np.where(np.diff(ch) != 0)[0]
print("Number of channel-switch points:", len(changes))
print("First few switch indices:", changes[:10])

# look at timestamps right around the big negative jump
diffs = np.diff(ts)
jump = np.argmin(diffs)
print(f"\nBiggest negative jump at index {jump}:")
for i in range(max(0,jump-2), min(len(ts),jump+4)):
    print(f"  idx {i}: ts={ts[i]:>18}  ch{ch[i]}")

# separate the two channels and check each is individually sorted
ts0 = ts[ch==0]
ts1 = ts[ch==1]
print("\nch0 timestamps sorted?", np.all(np.diff(ts0) >= 0))
print("ch1 timestamps sorted?", np.all(np.diff(ts1) >= 0))
print("ch0 time range:", ts0.min(), "to", ts0.max())
print("ch1 time range:", ts1.min(), "to", ts1.max())
