
import matplotlib.pyplot as plt

PAPER=False

def save_figure(filename, title):
    plt.title(title, y=1.04)
    if PAPER:
        print filename + '.eps'
        plt.savefig(filename + '.eps')
    else:
        print filename + '.pdf'
        plt.savefig(filename + '.pdf', transparent=True, pad_inches=2.5)

def add_legend(loc):
    if PAPER:
        plt.legend(loc=loc)
    else:
        plt.legend(loc=loc, fancybox=True, framealpha=0.4)

