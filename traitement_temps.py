import numpy as np
import json
from matplotlib import pyplot as plt


with open('results.json', mode='r') as file:
	datas = json.load(file)

ns, times = np.array(datas)

discard_up_to = 25
ns = ns[discard_up_to:]
times = times[discard_up_to:]

n_smooth = 1001  # must be odd (because I'm too lazy to cover the case where it is even)
mid_smooth = n_smooth // 2
mask = np.array([
	1 / ((abs(mid_smooth - i) + 3)**0.7 * n_smooth)
	for i in range(n_smooth)
])
norm = mask.sum()
mask = mask / norm

smoothened_times = np.sqrt(np.convolve(times ** 2, mask))
overflow = smoothened_times.shape[0] - times.shape[0]
trim_amount = overflow // 2
smoothened_times = smoothened_times[trim_amount:-trim_amount]

print(flush=True)

# plt.scatter(ns, times / ns, s=5)
# plt.scatter(ns, smoothened_times / ns, s=5)
# plt.plot(ns, times / (ns * np.log2(ns)))
plt.plot(ns, smoothened_times / (ns * np.log2(ns)))
# plt.plot(ns, smoothened_times)
# plt.scatter(ns, abs(times - smoothened_times) / times, s=5)

plt.tight_layout()
plt.show()
