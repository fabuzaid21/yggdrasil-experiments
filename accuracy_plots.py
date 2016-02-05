#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

plt.rc('text', usetex = True)
plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
plt.rcParams.update({'font.size': 18})

acc_1 = np.mean([1., 1, 1.])

acc_2 = np.mean([0.980032, 0.981183, 0.981170])

acc_4 = np.mean([0.968312, 0.976121, 0.973907])

acc_6 = np.mean([0.961204, 0.955811, 0.956059])

acc_8 = np.mean([0.941793, 0.940287, 0.940612])

p_s = [1, 2, 4, 6, 8]
# p = 1 [0.8841,   0.938786, 0.968106]
# p = 2 [0.839270, 0.914204, 0.945766]
# p = 4 [0.780442, 0.873920, 0.917531]
# p = 6 [0.736405, 0.823908, 0.882080]
# p = 8 [0.708559, 0.800981, 0.861226]


plt.plot(p_s, [acc_1, acc_2, acc_4, acc_6, acc_8], '.-', markersize=10, label=r'B = $\infty$')
plt.plot(p_s, [0.8841, 0.839270, 0.780442, 0.736405, 0.708559], 'x-', markersize=10, label='B = 2')
plt.plot(p_s, [0.938786, 0.914204, 0.873920, 0.823908, 0.800981], 'x-', markersize=10, label='B = 4')
plt.plot(p_s, [0.968106, 0.945766, 0.917531, 0.882080, 0.861226], 'x-', markersize=10, label='B = 8')

plt.legend(loc='lower left', fontsize='15')
plt.ylabel('Training Accuracy')
plt.xlabel('Num. Features')
plt.title('Yggdrasil vs. PLANET: Discretization Error')
plt.grid(True)
plt.savefig('Accuracy.eps')
