import json
import numpy as np
from matplotlib import pyplot as plt


# on récupère les mesures
with open('results.json', mode='r') as file:
    datas = json.load(file)

ns, times = np.array(datas)

# les premières valeurs sont inutilisables à cause d'un manque de précision
# des mesures et du fonctionnement de l'ordinateur
discard_up_to = 30
ns = ns[discard_up_to:]
times = times[discard_up_to:]

# on effectue une moyenne glissante
n_smooth = 300
mask = np.array([1 / n_smooth] * n_smooth)

smoothened_times = np.convolve(times, mask)
# la convolution ajoute des valeurs aux extrémités qu'on ne souhaite pas garder
overflow = smoothened_times.shape[0] - times.shape[0]
trim_amount = overflow // 2
smoothened_times = smoothened_times[
    trim_amount + (n_smooth + 1) % 2:
    -trim_amount
]

# Temps d'exécution brut
plt.plot(ns, smoothened_times)
plt.ylabel(r'Temps d\'exécution brut')

# Temps d'exécution divisé pra n * log(n)
# plt.plot(ns, smoothened_times / (ns * np.log2(ns)))
# plt.ylabel(r'Temps d\'exécution divisé par $n \log(n)$')

plt.xlabel('n')

plt.tight_layout()
plt.show()
