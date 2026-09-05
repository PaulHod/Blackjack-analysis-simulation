import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

OVERLAY_FIT = True
OVERLAY_OCCURENCES = False
CUTOFF_OCCURENCES = 1000

with open("10000000_hands_wins_occurences.json", "r") as f:
    stats = json.load(f)

winrate_per_count = np.array(stats[0])*100
occurences_per_count = np.array(stats[1])
counts = np.arange(-20,21,41/len(occurences_per_count))

def linear_fit(m, x, b):
    return m * x + b

sigma=1/np.sqrt(occurences_per_count)

params, covariance = curve_fit(
    linear_fit,
    counts,
    winrate_per_count,
    sigma=sigma,
    absolute_sigma=True
)

m, b = params
winrate_fit = linear_fit(m, counts, b)

weights = 1/np.square(sigma)
weighted_avg = np.average(winrate_per_count, weights=weights)
ss_res = np.sum(weights*(winrate_per_count - winrate_fit)**2)
ss_tot = np.sum(weights*(winrate_per_count - weighted_avg)**2)
r_squared = 1 - ss_res / ss_tot
print("R²:", r_squared)

occurences_normalized = occurences_per_count*(winrate_per_count.max()/occurences_per_count.max())

valid = occurences_per_count >= CUTOFF_OCCURENCES

x_intercept = -b/m

plt.plot(counts[valid], winrate_per_count[valid], label = "Winrate (10M hands)")
plt.plot(counts[valid], winrate_fit[valid], label=fr"Linear fit: {m:.2f}$\cdot$x - {-b:.2f}")
plt.plot(x_intercept, 0, 'o', label=f"x-intercept: {x_intercept:.2f}")
if OVERLAY_OCCURENCES:
    plt.plot(counts[valid], occurences_normalized[valid], label = f"Occurences per count, maximum = {occurences_per_count.max()}")
plt.xlabel("True Count")
plt.ylabel("Win rate [%]")
plt.title(fr"Wine Rate vs True Count Linear Fit: $R^2=${r_squared:.3f}")
plt.legend()
plt.grid()
plt.show()