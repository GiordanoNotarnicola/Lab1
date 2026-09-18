import wave
import numpy as np
from scipy.stats import chi2
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams['figure.facecolor'] = "#ffffff"
plt.rcParams['axes.facecolor'] = '#f0f0f0'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.color'] = '#d0d0d0'
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.linewidth'] = 0.7
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = 18


file_path = "DadP2-1.00.wav"
stream = wave.open(file_path)
signal = np.frombuffer(stream.readframes(stream.getnframes()), dtype=np.int16)
# Importante: se il file originale e‘ stereo dobbiamo prendere solo uno dei canali.
if stream.getnchannels() == 2:
    signal = signal[::2]
# L’unica cosa che ci manca e‘ l’array dei tempi corrispondenti ai singoli campioni.
t = np.arange(len(signal)) / stream.getframerate()

# A questo punto siamo pronti per analizzare il tracciato audio. Una volta
# messi i dati in un grafico di matplotlib possiamo utilizzare lo strumento
# zoom ed il mouse per misurare i tempi di rimbalzo 


# Supponiamo di aver preso a mano questa serie di tempi di rimbalzo.
t = [0.9477, 1.6274, 2.1495, 2.5458, 2.8543, 3.0925, 3.2654, 3.3914, 3.4809]
# Cercate di stimare ragionevolmente gli errori...
sigma_t = 0.005
# Calcolo delle differenze di tempo.
dt = np.diff(t)
# Creazione dell’array con gli indici dei rimbalzi.
n = np.arange(len(dt)) + 1.
# Calcolo dell’altezza massima e propagazione degli errori.
h = 9.81 * (dt**2.) / 8.0
dh = 2.0 * np.sqrt(2.0) * h * sigma_t / dt

def expo(n, h0, gamma):
    return h0 * gamma**n

popt, pcov = curve_fit(expo, n, h, sigma=dh, absolute_sigma = True)
h0_hat, gamma_hat = popt
sigma_h0, sigma_gamma = np.sqrt(pcov.diagonal())
xfit = np.linspace(min(n), max(n), 200)
res = h - expo(n, *popt)
resnorm=res/dh
chi2 = np.sum((res/(sigma_t*np.ones(len(h))))**2)
ndof = len(h) - 2
chi2_red = chi2 / ndof
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[3,1]})

# --- FIT ---
ax1.errorbar(n, h, yerr=sigma_t*np.ones(len(h)), fmt='o', label='dati')

ax1.plot(xfit, expo(xfit,*popt), 'r-', label='fit')
ax1.set_title('Rimbalzo pallina da tennis Lab 1')
ax1.set_ylabel(r"$h_{max}\, [m]$")

ax1.legend(loc='center right', frameon=True)
# --- RESIDUI ---
ax2.errorbar(n, resnorm, fmt='.')
ax2.axhline(0, color='black', linewidth=1)
ax2.set_xlabel(r"$n$")
ax2.set_ylabel("Residui")


text = (
    f"y0 = {popt[0]:.3f} ± {np.sqrt(pcov[0,0]):.3f} m\n"
    f"$\gamma = {popt[1]:.2f} \pm {0.01}$"
    rf"$\chi^2_\nu = {chi2_red:.2f}$"
)
ax1.text(0.93, 0.71, text, transform=ax1.transAxes,
         verticalalignment='bottom',
         horizontalalignment='right',
         bbox=dict(boxstyle="round", facecolor="white"))

plt.tight_layout()
plt.show()
