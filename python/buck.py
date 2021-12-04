import control
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def F(Vg, Vo, Ri, L, Ts, Se, Zo=0):
    # Zo(s) default value is 0 (a high-frequency approximation).
    # He(s) is estimated with the Pade Approximant (10th-order).
    Sn = (Vg - Vo) * Ri / L
    Sf = Vo * Ri / L
    Fm = 1 / ((Sn + Se) * Ts)
    kr = Ts * Ri / (2 * L)
    pade = control.tf(*control.pade(Ts, 10))
    He = control.tf([Ts, 0], 1) / (1 / pade - 1)
    sL = control.tf([L, 0], 1)
    return Fm * Vg / (Fm * Vg * (Ri * He - kr * Zo) + Zo + sL)


def to_si(d, sep=""):
    # Metric prefix formatting, courtesy of StackOverflow.
    # https://stackoverflow.com/questions/15733772/...
    #    convert-float-number-to-string-with-engineering-notation-with-si-prefix-in-pyt

    if d == 0:
        return str(0)

    degree = int(math.floor(math.log10(math.fabs(d)) / 3))
    prefix = ""
    inc_prefixes = ["k", "M", "G", "T", "P", "E", "Z", "Y"]
    dec_prefixes = ["m", "µ", "n", "p", "f", "a", "z", "y"]

    if degree != 0:
        ds = degree / math.fabs(degree)
        if ds == 1:
            if degree - 1 < len(inc_prefixes):
                prefix = inc_prefixes[degree - 1]
            else:
                prefix = inc_prefixes[-1]
                degree = len(inc_prefixes)
        elif ds == -1:
            if -degree - 1 < len(dec_prefixes):
                prefix = dec_prefixes[-degree - 1]
            else:
                prefix = dec_prefixes[-1]
                degree = -len(dec_prefixes)

        scaled = float(d * math.pow(1000, -degree))
        s = "{scaled}{sep}{prefix}".format(scaled=scaled, sep=sep, prefix=prefix)
    else:
        s = "{d}".format(d=d)

    return s


def plotTF(tf, label, flims, phase=True):
    # Plot the given transfer function(s). Frequency limits are in Hz.
    tfs, labels = (tf, label) if isinstance(tf, list) else ([tf], [label])
    if phase:
        fig, (mag_ax, phase_ax) = plt.subplots(nrows=2, sharex=True, figsize=(8, 12))
    else:
        fix, mag_ax = plt.subplots(nrows=1, figsize=(8, 6))

    freq = np.logspace(np.log10(flims[0]), np.log10(flims[1]), 10000)
    omega = freq * math.tau
    for tf, label in zip(tfs, labels):
        mag, angle, _ = control.freqresp(tf, omega)
        mag_db = control.mag2db(mag)
        mag_ax.semilogx(freq, mag_db, label=label, linewidth=3)
        if phase:
            angle_deg = control.unwrap(angle) * 180 / np.pi
            phase_ax.semilogx(freq, angle_deg, label=label, linewidth=3)

    mag_ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    mag_ax.set_ylabel("Gain (dB)")
    mag_ax.grid(which="major", color="k", linestyle="-")
    mag_ax.grid(which="minor", linestyle="--")
    mag_ax.legend()
    mag_ax.set_title("Transfer Function(s)")
    if not phase:
        mag_ax.set_xlabel("Frequency (Hz)")
    else:
        phase_ax.set_xlabel("Frequency (Hz)")
        phase_ax.set_ylabel("Phase (deg)")
        phase_ax.grid(which="major", color="k", linestyle="-")
        phase_ax.grid(which="minor", linestyle="--")
        phase_ax.legend()

    pow10 = [10 ** math.ceil(math.log10(flims[0]))]
    while pow10[-1] < flims[1]:
        pow10.append(pow10[-1] * 10)

    plt.xticks(ticks=pow10, labels=[to_si(ftick) for ftick in pow10])
