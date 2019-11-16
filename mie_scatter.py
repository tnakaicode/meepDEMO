import PyMieScatt as ps
import matplotlib.pyplot as plt
import numpy as np
from time import time
import matplotlib.colors as colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from scipy.ndimage import zoom


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list('trunc({n},{a:.2f},{b:.2f})'.format(
        n=cmap.name, a=minval, b=maxval), cmap(np.linspace(minval, maxval, n)))
    return new_cmap


d = 300
w = 375
m = 1.77 + 0.63j

nMin = 1.33
nMax = 3
kMin = 0.001
kMax = 1
err = 0.01

Qm = ps.fastMieQ(m, w, d)

points = 200
interpolationFactor = 2

nRange = np.linspace(nMin, nMax, points)
kRange = np.linspace(kMin, kMax, points)

plt.close('all')

start = time()
QscaList = []
QabsList = []
QbackList = []
nList = []
kList = []
for n in nRange:
    s = []
    a = []
    b = []
    for k in kRange:
        m = n + k * 1.0j
        Qsca, Qabs, Qback = ps.fastMieQ(m, w, d)
        s.append(Qsca)
        a.append(Qabs)
        b.append(Qback)
    QscaList.append(s)
    QabsList.append(a)
    QbackList.append(b)
n = zoom(nRange, interpolationFactor)
k = zoom(kRange, interpolationFactor)
QscaSurf = zoom(np.transpose(np.array(QscaList)), interpolationFactor)
QabsSurf = zoom(np.transpose(np.array(QabsList)), interpolationFactor)
QbackSurf = zoom(np.transpose(np.array(QbackList)), interpolationFactor)

nSurf, kSurf = np.meshgrid(n, k)

c1 = truncate_colormap(cm.Reds, 0.2, 1, n=256)
c2 = truncate_colormap(cm.Blues, 0.2, 1, n=256)
c3 = truncate_colormap(cm.Greens, 0.2, 1, n=256)

xMin, xMax = nMin, nMax
yMin, yMax = kMin, kMax

fig1 = plt.figure()

ax1 = plt.subplot2grid((2, 2), (0, 0), projection='3d')
ax2 = plt.subplot2grid((2, 2), (0, 1), projection='3d')
ax3 = plt.subplot2grid((2, 2), (1, 0), projection='3d')
ax4 = plt.subplot2grid((2, 2), (1, 1))
ax1.set_proj_type('ortho')
ax2.set_proj_type('ortho')
ax3.set_proj_type('ortho')

qscaerrs = [Qm[0] - Qm[0] * err, Qm[0] + Qm[0] * err]
qabserrs = [Qm[1] - Qm[1] * err, Qm[1] + Qm[1] * err]
qbackerrs = [Qm[2] - Qm[2] * err, Qm[2] + Qm[2] * err]

ax1.plot_surface(nSurf, kSurf, QscaSurf, rstride=1,
                 cstride=1, cmap=c1, alpha=0.5)
ax1.contour(nSurf, kSurf, QscaSurf,
            Qm[0], linewidths=2, colors='r', linestyles='dashdot')
ax1.contour(nSurf, kSurf, QscaSurf, qscaerrs, linewidths=0.5,
            colors='r', linestyles='dashdot', alpha=0.75)
ax1.contour(nSurf, kSurf, QscaSurf,
            Qm[0], linewidths=2, colors='r', linestyles='dashdot', offset=0)
ax1.contourf(nSurf, kSurf, QscaSurf, qscaerrs,
             colors='r', offset=0, alpha=0.25)

ax2.plot_surface(nSurf, kSurf, QabsSurf, rstride=1,
                 cstride=1, cmap=c2, alpha=0.5)
ax2.contour(nSurf, kSurf, QabsSurf,
            Qm[1], linewidths=2, colors='b', linestyles='solid')
ax2.contour(nSurf, kSurf, QabsSurf, qabserrs, linewidths=0.5,
            colors='b', linestyles='solid', alpha=0.75)
ax2.contour(nSurf, kSurf, QabsSurf,
            Qm[1], linewidths=2, colors='b', linestyles='solid', offset=0)
ax2.contourf(nSurf, kSurf, QabsSurf, qabserrs,
             colors='b', offset=0, alpha=0.25)

ax3.plot_surface(nSurf, kSurf, QbackSurf, rstride=1,
                 cstride=1, cmap=c3, alpha=0.5)
ax3.contour(nSurf, kSurf, QbackSurf,
            Qm[2], linewidths=2, colors='g', linestyles='dotted')
ax3.contour(nSurf, kSurf, QbackSurf, qbackerrs, linewidths=0.5,
            colors='g', linestyles='dotted', alpha=0.75)
ax3.contour(nSurf, kSurf, QbackSurf,
            Qm[2], linewidths=2, colors='g', linestyles='dotted', offset=0)
ax3.contourf(nSurf, kSurf, QbackSurf, qbackerrs,
             colors='g', offset=0, alpha=0.25)

boxLabels = ["Qsca", "Qabs", "Qback"]

yticks = np.arange(kMax, kMin - 0.25, -0.25)  # [1,0.75,0.5,0.25,0]
xticks = np.arange(nMax, 1.5 - 0.25, -0.25)  # [2,1.75,1.5,1.25]
xticks = np.append(xticks, 1.3)

for a, t in zip([ax1, ax2, ax3], boxLabels):
    lims = a.get_zlim3d()
    a.set_zlim3d(0, lims[1])
    a.set_ylim(kMax, 0)
    a.set_yscale('linear')
    a.set_xlim(nMax, 1.3)
    a.set_xticks(xticks)
    a.set_xticklabels(xticks, rotation=28, va='bottom', ha='center')
    a.set_yticks(yticks)
    a.set_yticklabels(yticks, rotation=-10, va='center', ha='left')
    a.set_zticklabels([])
    a.view_init(20, 120)
    a.tick_params(axis='x', labelsize=12, pad=12)
    a.tick_params(axis='y', labelsize=12, pad=-2)
    a.set_xlabel("n", fontsize=18, labelpad=4)
    a.set_ylabel("k", fontsize=18, labelpad=3)
    a.set_zlabel(t, fontsize=18, labelpad=-10, rotation=90)

Qm = [(q, q * err) for q in Qm]
giv = ps.ContourIntersection(Qm[0], Qm[1], w, d, Qback=Qm[2], gridPoints=200,
                             nMin=nMin, nMax=nMax, kMin=kMin, kMax=kMax, axisOption=1, fig=fig1, ax=ax4)
ax4.set_xlim(nMin, nMax)
ax4.yaxis.tick_right()
ax4.yaxis.set_label_position("right")
ax4.set_title("")
ax4.set_yscale('linear')
l = [giv[-1]['Qsca'], giv[-1]['Qabs'], giv[-1]['Qback']]
[x.set_label(tx) for x, tx in zip(l, boxLabels)]
h = [x.get_label() for x in l]
ax4.legend(l, h, fontsize=16, loc='upper right')

plt.suptitle(
    "m={n:1.3f}+{k:1.3f}i".format(n=giv[0][0].real, k=giv[0][0].imag), fontsize=24)

plt.tight_layout()
plt.savefig(
    "{n:1.2f}+{k:1.2f}i.png".format(n=giv[0][0].real, k=giv[0][0].imag))
plt.show()

end = time()
print("Done in {t:1.2f} seconds.".format(t=end - start))
