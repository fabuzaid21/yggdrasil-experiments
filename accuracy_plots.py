#!/usr/bin/env python

from utils import save_figure, add_legend
import matplotlib.pyplot as plt
import numpy as np
import config

acc_1 = np.mean([1., 1, 1.])
acc_2 = np.mean([0.980032, 0.981183, 0.981170])
acc_4 = np.mean([0.968312, 0.976121, 0.973907])
acc_6 = np.mean([0.961204, 0.955811, 0.956059])
acc_8 = np.mean([0.941793, 0.940287, 0.940612])
p_s = [1, 2, 4, 6, 8]

if __name__ == '__main__':
    # p = 1 [0.8841,   0.938786, 0.968106]
    # p = 2 [0.839270, 0.914204, 0.945766]
    # p = 4 [0.780442, 0.873920, 0.917531]
    # p = 6 [0.736405, 0.823908, 0.882080]
    # p = 8 [0.708559, 0.800981, 0.861226]


    plt.plot(p_s, [acc_1, acc_2, acc_4, acc_6, acc_8], '.-',
             label='Yggdrasil')
    plt.plot(p_s, [0.8841, 0.839270, 0.780442, 0.736405, 0.708559],
             'x-', label='PLANET, B = 2')
    plt.plot(p_s, [0.938786, 0.914204, 0.873920, 0.823908, 0.800981],
             'x-', label='PLANET, B = 4')
    plt.plot(p_s, [0.968106, 0.945766, 0.917531, 0.882080, 0.861226],
             'x-', label='PLANET, B = 8')

    add_legend('lower left')
    plt.ylabel('Training Accuracy')
    plt.xlabel('Num. Features')
    plt.grid(True)
    save_figure('accuracy', 'Yggdrasil vs. PLANET: Discretization Error')

