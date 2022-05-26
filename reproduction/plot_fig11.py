import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
rcParams['font.family'] = ['serif']
rcParams['font.serif'] = ['Times New Roman']

# EMD
emd_tpr = [0.9941,0.9790,0.9658,0.9417,0.8878,0.8201,0.7153,0.5482,0.3409,0.0049,0.0004]
emd_fpr = [0.9772,0.9608,0.9319,0.8896,0.8250,0.7163,0.5474,0.3317,0.1250,0.0003,0.00009]
print(len(emd_tpr))

# PhishZoo
phishzoo_tpr = [0.9215,0.9185,0.8955,0.8480,0.7700,0.6942,0.6080,0.3349,0.2524,0.2454,0.2391,0.2202,0.2190]
phishzoo_fpr = [0.4093,0.4061,0.3922,0.3683,0.3335,0.2935,0.2548,0.1970,0.1625,0.1589,0.1576,0.1567,0.1567]
print(len(phishzoo_tpr))

# VisualPhishNet
visual_tpr = [0.0086,0.0158,0.0264,0.1786,0.1952,0.2102,0.2369,0.5496,0.6710,0.7495,0.8067,0.8610,0.9044,0.9398]
visual_fpr = [0.0000,0.0002,0.0048,0.0048,0.0057,0.0069,0.0097,0.0953,0.2439,0.3789,0.5070,0.6232,0.7217,0.7991]
print(len(visual_tpr))

# Digest matching
digest_tpr = [0.4835909954]
digest_fpr = [10.0**(-5)]

# # phishpedia
phishpedia_tpr = [0.9384,0.9384,0.9365,0.9059,0.8690,0.8584,0.8460,0.8244,0.7536,0.6474,0.3953,0.1139,0.0036,0.0000]
phishpedia_fpr = [0.6845,0.6840,0.6404,0.1696,0.0071,0.0042,0.0027,0.0020,0.0014,0.0012,0.0009,0.0004,0.0000,0.0000]
print(len(phishpedia_tpr))

# phishintention new
phishintention_tpr_new = [0.9552,0.9552,0.9550,0.9419,0.9093,0.9055,0.8984,0.8845,0.8584,0.8045,0.6604,0.3708,0.0138,0.0000]
phishintention_fpr_new = [0.5222,0.5221,0.5102,0.1972,0.0034,0.0015,0.0009,0.0007,0.0006,0.0004,0.0004,0.0003,0.0000,0.0000]
print(len(phishintention_tpr_new))

# method I: plt
plt.figure(figsize=(10,10))

# plt.title('Receiver Operating Characteristic')
ax = plt.gca()

ax.plot(emd_fpr, emd_tpr, 'black', label='EMD',linestyle='--', marker='o', markersize=10)
ax.plot(phishzoo_fpr, phishzoo_tpr, 'purple', label='PhishZoo',linestyle=':', marker='v', markersize=10)
ax.plot(visual_fpr, visual_tpr, 'darkgreen', label='VisualPhishNet',linestyle='--', marker='^', markersize=10)
ax.plot(phishpedia_fpr, phishpedia_tpr, 'blue', label='Phishpedia', marker='D', markersize=10)
ax.plot(phishintention_fpr_new, phishintention_tpr_new, 'red', label='PhishIntention', marker='p', markersize=10)


plt.xlim([10.0**(-5), 1])
plt.ylim([0, 1])
plt.ylabel('True Positive Rate', fontsize=20,  fontname='Times')
plt.xlabel('False Positive Rate', fontsize=20, fontname='Times')
plt.legend(loc = 'best', fontsize=15)
plt.grid(linestyle='--', which='both', linewidth=1)
ax.set_xscale('log')
plt.xticks(fontsize=20) 
plt.yticks(np.arange(0, 1.1, step=0.1),fontsize=20)
plt.show()