import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import re


def real_data():
    t0 = None
    y = []
    y2 = []
    s = [0]
    e = []
    with open('data.txt') as f:
        for line in f:
            t = [int(x) for x in re.search("\d\d:\d\d:\d\d", line).group().split(":")]
            t = sum([t[2 - i] * pow(60, i) for i in range(3)])
            r1 = re.search("(\d) h", line)
            if r1 is not None:
                r1 = int(r1.group(1))
            else:
                r1 = 0
            r2 = re.search("(\d+) m", line)
            if r2 is not None:
                r2 = int(r2.group(1))
            else:
                r2 = 0
            r3 = re.search("(\d+) s", line)
            if r3 is not None:
                r3 = int(r3.group(1))
            else:
                r3 = 0
            if t0 is not None:
                y += [t - t0]
                y2 += [r1 * 3600 + r2 * 60 + r3]
                s += [s[-1] + y[-1]]
                e += [(100 - len(y)) * s[-1] / len(y)]
            t0 = t
    r = [s[-1] - k + y2[-1] for k in s]

    return e, r, s, y, y2

def do_graph(name, func):
    fig = func()
    plt.savefig(name + ".svg", dpi=500, transparent=True)
    plt.close(fig)


def graph0():
    e, r, s, y, y2 = real_data()
    fig, axs = plt.subplots(2, sharex=True)
    x = range(len(y))
    axs[0].plot(x, y, label="time cost", marker='o')
    axs[0].legend()
    axs[1].plot(x, e, color="purple", label="linear ETA")
    axs[1].plot(x, r[1:], color="red", label="remaining")
    axs[1].legend()
    return fig


def graph1():
    def func(x):
        return np.ones(np.shape(x)) * 0.5

    a, b = 0.5, 1  # integral limits
    x = np.linspace(0, 1)
    y = func(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', linewidth=2)
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0, top=1)

    # Make the shaded region
    ix = np.linspace(a, b)
    iy = func(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    ax.text(0.25, 0.25, r"$T_1$",
            horizontalalignment='center', fontsize=20)
    ax.text(0.75, 0.25, r"$R$",
            horizontalalignment='center', fontsize=20)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

    ax.set_xticks((0, a, b))
    ax.set_xticklabels(('$0$', '$x_1$', '$1$'))
    ax.set_yticks([0.5])
    ax.set_yticklabels(['$K$'])

    return fig


def graph2():
    def func(x):
        return 0.25 + 0.5 * x

    a, b, c = 0, 0.5, 1  # integral limits
    x = np.linspace(0, 1)
    y = func(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', linewidth=2)
    ax.plot(x, np.ones(np.shape(x)) * 0.25, 'r', linewidth=1, linestyle='--')
    ax.plot(x, np.ones(np.shape(x)) * 0.75, 'r', linewidth=1, linestyle='--')
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0, top=1)

    # Make the shaded region
    ix = np.linspace(a, b)
    iy = func(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    # Make the shaded region
    ix = np.linspace(b, c)
    iy = func(ix)
    verts = [(b, 0), *zip(ix, iy), (c, 0)]
    poly = Polygon(verts, facecolor='0.95', edgecolor='0.5')
    ax.add_patch(poly)

    ax.text(0.25, 0.125, r"$A_x$",
            horizontalalignment='center', fontsize=20)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

    ax.set_xticks((a, b, c))
    ax.set_xticklabels(('$0$', '$x$', '$1$'))
    ax.set_yticks([0.25, 0.75])
    ax.set_yticklabels(['$K_0$', '$K_1$'])

    return fig


def graph3():
    def func(x):
        return 0.25 + 0.5 * x

    a, b, c = 0.33, 0.66, 1  # integral limits
    x = np.linspace(0, 1)
    y = func(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, 'r', linewidth=2)
    ax.plot(x, np.ones(np.shape(x)) * 0.25, 'r', linewidth=1, linestyle='--')
    ax.plot(x, np.ones(np.shape(x)) * 0.75, 'r', linewidth=1, linestyle='--')
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0, top=1)

    # Make the shaded region
    ix = np.linspace(a, b)
    iy = func(ix)
    verts = [(a, 0), *zip(ix, iy), (b, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    # Make the shaded region
    ix = np.linspace(b, c)
    iy = func(ix)
    verts = [(b, 0), *zip(ix, iy), (c, 0)]
    poly = Polygon(verts, facecolor='0.95', edgecolor='0.5')
    ax.add_patch(poly)

    ax.text(0.33/2, 0.125, r"$T_1$",
            horizontalalignment='center', fontsize=20)

    ax.text(0.66+0.33 / 2, 0.28, r"$R$",
            horizontalalignment='center', fontsize=20)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

    ax.set_xticks((0, a, b, c))
    ax.set_xticklabels(('$0$', '$x_1$', '$x_2$', '$1$'))
    ax.set_yticks([0.25, 0.75])
    ax.set_yticklabels(['$K_0$', '$K_1$'])

    return fig


def graph4():
    e, r, s, y, y2 = real_data()
    fig, axs = plt.subplots(2, sharex=True)
    x = range(len(y))
    axs[0].plot(x, y, label="time cost", marker='o')
    axs[0].legend()
    axs[1].plot(x, y2, label="non-linear ETA")
    axs[1].plot(x, e, color="purple", label="linear ETA")
    axs[1].plot(x, r[1:], color="red", label="remaining")
    axs[1].legend()
    return fig


do_graph("graph0", graph0)
do_graph("graph1", graph1)
do_graph("graph2", graph2)
do_graph("graph3", graph3)
do_graph("graph4", graph4)
