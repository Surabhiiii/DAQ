
import uproot
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

f = uproot.open("<FILEPATH.root>")
tree = f["Data_R"]
ts = tree["Timestamp"].array(library="np").astype(np.int64)
ch = tree["Channel"].array(library="np")

t0 = ts[ch == 0]; t1 = ts[ch == 1]
idx = np.clip(np.searchsorted(t1, t0), 1, len(t1)-1)
dt_left = t0 - t1[idx-1]; dt_right = t0 - t1[idx]
dt = np.where(np.abs(dt_left) < np.abs(dt_right), dt_left, dt_right)

# zoom on the peak region
mask = (dt > -15000) & (dt < 0)
dt_peak = dt[mask]

counts, edges = np.histogram(dt_peak, bins=300)
centers = (edges[:-1] + edges[1:]) / 2

# fit a Gaussian to get FWHM (timing resolution)
def gauss(x, A, mu, sigma):
    return A * np.exp(-(x-mu)**2 / (2*sigma**2))

p0 = [counts.max(), centers[np.argmax(counts)], 1000]
popt, _ = curve_fit(gauss, centers, counts, p0=p0)
A, mu, sigma = popt
fwhm = 2.355 * abs(sigma)

print(f"Peak center: {mu:.0f} ps")
print(f"Sigma: {abs(sigma):.0f} ps")
print(f"TIMING RESOLUTION (FWHM): {fwhm:.0f} ps  =  {fwhm/1000:.2f} ns")

plt.hist(dt_peak, bins=300, histtype="step", label="data")
xfit = np.linspace(centers.min(), centers.max(), 500)
plt.plot(xfit, gauss(xfit, *popt), 'r-', label=f"Gaussian fit\nFWHM={fwhm:.0f} ps")
plt.xlabel("Time difference ch0 - ch1 (ps)")
plt.ylabel("Coincidence counts")
plt.title("Na-22 coincidence peak with Gaussian fit")
plt.legend()
plt.tight_layout()
plt.savefig("<DESTINATION.png>", dpi=150)
print("Saved coinc_fit.png")
plt.show()
