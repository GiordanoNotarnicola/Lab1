import wave
import numpy as np
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

## Data
file_path = r'C:/Users/Angelo/Desktop/Bouncingball15.wav'
stream = wave.open(file_path)
signal = np.frombuffer(stream.readframes(stream.getnframes()), dtype=np.int16)



if stream.getnchannels() == 2: #really important if the acquisition system is a stereo: one input shall be suppressed.
    signal = signal[::2]

t = np.arange(len(signal)) / stream.getframerate()

h_measured=0.37
s_h_measured=0.01
g=9.80513



## Manipulation
a_signal=np.abs(signal)

t_bounces=[2.03]

for i in range(3,np.size(a_signal)):
    if(np.size(t_bounces)==0):
        if(a_signal[i]/8000>1):
            t_bounces.append(t[i])
            print("Caricamento",i*100/np.size(a_signal))
    elif(max(t_bounces)+0.06-t[i]<0):
        if(a_signal[i]/8000>1):
            t_bounces.append(t[i])
            print("Caricamento",i*100/np.size(a_signal))
t_bounces.pop(0)
t_bounces=t_bounces[:np.size(t_bounces)-1]
s_t_bounces=np.full_like(t_bounces, 0.0015)


dt = np.diff(np.array(t_bounces))
s_t_dt=np.full_like(dt,0.0015*np.sqrt(2))
# Creazione dell"array con gli indici dei rimbalzi.
n = np.arange(len(dt)) + 1.
# Calcolo dell’altezza massima e propagazione degli errori.
h = g * (dt**2.) / 8.0
# h[0]=0.37
print("h [m] =",h)
s_h = 2* np.sqrt(2) * h * s_t_dt / dt

sigma_t = 0.005
a=np.full_like(t_bounces,8000)
plt.figure()
plt.plot(t,a_signal)
plt.errorbar(t_bounces,a,fmt="o")

##Function
def expo(n, h0, gamma,c):
    """Modello di fit.
    """
    return (h0 * gamma**n)+c
##Best-fit Algorythm
p0=(1.459,0.793,1)
popt, pcov = curve_fit(expo, n, h,p0, sigma=s_h)
h0_hat, gamma_hat,c_hat = popt
sigma_h0, sigma_gamma, sigma_c = np.sqrt(pcov.diagonal())
res = h - expo(n, *popt)
resnorm=res/s_h
chi2 = np.sum((res/(s_t_dt*np.ones(len(h))))**2)
ndof = len(h) - 2
chi2_red = chi2 / ndof

##Plot

# --- FIT ---
xfit = np.linspace(min(n),max(n), 5000)
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios':[3,1]})

ax1.errorbar(n, h, yerr=s_h, fmt='o', label='dati')

ax1.plot(xfit, expo(xfit,*popt), 'r-', label='fit')
ax1.set_title('Rimbalzo pallina da ping pong Lab 1')
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