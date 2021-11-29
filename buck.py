import control
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def F(Vg, Vo, Ri, L, Ts, Se, Zo=None, BW=None, nBW=None):
    # When Zo(s) is provided, F(s) is an nBW-point FRD with bandwidth BW.
    # F(s) is otherwise an approximate transfer function, valid up to 1/(2*Ts).
    Sn = (Vg - Vo) * Ri / L
    Sf = Vo * Ri / L
    Fm = 1 / ((Sn + Se) * Ts)
    kr = Ts * Ri / (2 * L)
    if Zo is None:
        alpha = (Sf - Se) / (Sn + Se)
        FmFi = control.tf(1 + alpha, [Ri * Ts, 0])
        He = 1 - control.tf([Ts / 2, 0], 1) + control.tf([(Ts / np.pi) ** 2, 0, 0], 1)
        Fapprox = FmFi / (1 + FmFi * Ri * He)
        return Fapprox.minreal()
    else:
        freqBW = np.logspace(np.log10(BW[0]), np.log10(BW[1]), nBW) * math.tau
        respBW = freqBW * 1j * Ts / (np.exp(freqBW * 1j * Ts) - 1)
        He = control.FrequencyResponseData(respBW, freqBW)
        sL = control.tf([L, 0], 1)
        Fexact = Fm * Vg / (Fm * Vg * (Ri * He - kr * Zo) + Zo + sL)
        return control.FrequencyResponseData(Fexact, smooth=True)


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


def plotTF(tf, label, flims, n):
    # Plot the given transfer function(s). Frequency limits are in Hz.
    tfs, labels = (tf, label) if isinstance(tf, list) else ([tf], [label])
    fig, (mag_ax, phase_ax) = plt.subplots(nrows=2, sharex=True, figsize=(8, 12))
    freq = np.logspace(np.log10(flims[0]), np.log10(flims[1]), n)

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
    
    pow10 = [10 ** math.ceil(math.log10(flims[0]))]
    while pow10[-1] < flims[1]:
        pow10.append(pow10[-1]*10)
    
    plt.xticks(ticks=pow10, labels=[to_si(ftick) for ftick in pow10])
