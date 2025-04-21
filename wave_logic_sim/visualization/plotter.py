import matplotlib.pyplot as plt

def plot_signals(time, signals, title=None, show=True):
    n = len(signals)
    fig, axes = plt.subplots(n, 1, sharex=True, figsize=(6, 2.5 * n))
    if n == 1:
        axes = [axes]
    for (label, values), ax in zip(signals.items(), axes):
        ax.plot(time, values)
        ax.set_ylabel(label)
        if title and ax is axes[0]:
            ax.set_title(title)
        ax.grid(True)
    axes[-1].set_xlabel("Time")
    fig.tight_layout()
    if show:
        plt.show()
    return fig
