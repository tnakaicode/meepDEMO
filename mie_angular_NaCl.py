# Recently, a colleague needed to know how much light a distribution of salt aerosol would scatter into two detectors, one at 60° and one at 90°. We modeled a lognormal distribution of NaCl particles based on laboratory measurements and then tried to figure out how much light we’d see at various angles.


import PyMieScatt as ps  # import PyMieScatt and abbreviate as ps
# import standard plotting library and abbreviate as plt
import matplotlib.pyplot as plt
import numpy as np  # import numpy and abbreviate as np
# import a single function for integration using trapezoidal rule
from scipy.integrate import trapz

m = 1.536  # refractive index of NaCl
wavelength = 405  # replace with the laser wavelength (nm)

dp_g = 85  # geometric mean diameter - replace with your own (nm)
# geometric standard deviation - replace with your own (unitless)
sigma_g = 1.5
N = 1e5  # total number of particles - replace with your own (cm^-3)

B = ps.Mie_Lognormal(m, wavelength, sigma_g, dp_g, N,
                     returnDistribution=True)  # Calculate optical properties

S = ps.SF_SD(m, wavelength, B[7], B[8])

fig1 = plt.figure(figsize=(10.08, 6.08))
ax1 = fig1.add_subplot(1, 1, 1)

ax1.plot(S[0], S[1], 'b', ls='dashdot', lw=1, label="Parallel Polarization")
ax1.plot(S[0], S[2], 'r', ls='dashed', lw=1,
         label="Perpendicular Polarization")
ax1.plot(S[0], S[3], 'k', lw=1, label="Unpolarized")

x_label = ["0", r"$\mathregular{\frac{\pi}{4}}$", r"$\mathregular{\frac{\pi}{2}}$",
           r"$\mathregular{\frac{3\pi}{4}}$", r"$\mathregular{\pi}$"]
x_tick = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
ax1.set_xticks(x_tick)
ax1.set_xticklabels(x_label, fontsize=14)
ax1.tick_params(which='both', direction='in')
ax1.set_xlabel("Scattering Angle ϴ", fontsize=16)
ax1.set_ylabel(r"Intensity ($\mathregular{|S|^2}$)", fontsize=16, labelpad=10)
handles, labels = ax1.get_legend_handles_labels()
fig1.legend(handles, labels, fontsize=14, ncol=3, loc=8)

fig1.suptitle("Scattering Intensity Functions", fontsize=18)

plt.tight_layout(rect=[0.01, 0.05, 0.915, 0.95])

# Highlight certain angles and compute integral
sixty = [0.96 < x < 1.13 for x in S[0]]
ninety = [1.48 < x < 1.67 for x in S[0]]
ax1.fill_between(S[0], 0, S[3], where=sixty, color='g', alpha=0.15)
ax1.fill_between(S[0], 0, S[3], where=ninety, color='g', alpha=0.15)
ax1.set_yscale('log')

int_sixty = trapz(S[3][110:130], S[0][110:130])
int_ninety = trapz(S[3][169:191], S[0][169:191])

# Annotate plot with integral results
ax1.annotate("Integrated value = {i:1.3f}".format(i=int_sixty),
             xy=(np.pi / 3, S[3][120]), xycoords='data',
             xytext=(np.pi / 6, 0.8), textcoords='data',
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3"),
             )
ax1.annotate("Integrated value = {i:1.3f}".format(i=int_ninety),
             xy=(np.pi / 2, S[3][180]), xycoords='data',
             xytext=(2 * np.pi / 5, 2), textcoords='data',
             arrowprops=dict(arrowstyle="->",
                             connectionstyle="arc3"),
             )
plt.show()
