import control
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def F(Vg, Vo, Ri, L, Ts, Se, Zo=None):
    # Return F(s). Exact when Zo(s) is provided. Approximate otherwise.
    Sn = (Vg - Vo) * Ri / L
    Sf = Vo * Ri / L
    Fm = 1 / ((Sn + Se) * Ts)
    He = 1 - control.tf([Ts / 2, 0], 1) + control.tf([(Ts / np.pi) ** 2, 0, 0], 1)
    kr = Ts * Ri / (2 * L)
    if Zo is None:
        alpha = (Sf - Se) / (Sn + Se)
        FmFi = control.tf(1 + alpha, [Ri * Ts, 0])
        return FmFi / (1 + FmFi * Ri * He)
    else:
        sL = control.tf([L, 0], 1)
        return Fm * Vg / (sL + Zo + Fm * Vg * (Ri * He - kr * Zo))


def plotTF(tf, label, flims, fticks=None, flabels=None):
    # Plot the given transfer function(s).
    tfs, labels = (tf, label) if isinstance(tf, list) else ([tf], [label])
    fig, (mag_ax, phase_ax) = plt.subplots(nrows=2, sharex=True, figsize=(8, 12))
    freq = np.logspace(np.log10(flims[0]), np.log10(flims[1]), 1000)

    for tf, label in zip(tfs, labels):
        mag, phase, omega = control.freqresp(tf, freq * math.tau)
        mag_ax.semilogx(freq, control.mag2db(mag), linewidth=3, label=label)
        phase_ax.semilogx(
            freq, control.unwrap(phase) * 180 / np.pi, linewidth=3, label=label
        )

    mag_ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    mag_ax.set_ylabel("Gain (dB)")
    mag_ax.grid(which="major", color="k", linestyle="-")
    mag_ax.grid(which="minor", linestyle="--")
    mag_ax.legend()
    mag_ax.set_title("Transfer Function(s)")
    phase_ax.set_xlabel("Frequency (Hz)")
    phase_ax.set_ylabel("Phase (deg)")
    phase_ax.grid(which="major", color="k", linestyle="-")
    phase_ax.grid(which="minor", linestyle="--")
    phase_ax.legend()
    plt.xticks(ticks=fticks, labels=flabels)
