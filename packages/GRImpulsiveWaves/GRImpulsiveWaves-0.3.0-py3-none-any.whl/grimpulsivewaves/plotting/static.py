import random

import matplotlib.pyplot as plt
import numpy as np


#This is deprecated and no longer will be supported






class StaticGeodesicPlotter:
    def __init__(self, use3d=False, figsize=(8, 8), labels2d=["x", "y"], zlabel = "z", labelsize=16, aspect=1):
        self.use3d = use3d
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_aspect(aspect) #Just to make sure ratio is 1:1
        self.ax.set_adjustable('box', True)
        if self.use3d:
            self.ax = plt.axes(projection="3d")
            self.ax.set_zlabel(zlabel)
        self.ax.set_xlabel(labels2d[0])
        self.ax.set_ylabel(labels2d[1])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.xaxis.label.set_size(labelsize)
        self.ax.yaxis.label.set_size(labelsize)

        if use3d:
            self.ax.set_zticks([])
            self.ax.zaxis.label.set_size(labelsize)

    def _set_scaling(self, x_range, y_range, z_range, lim):
        if x_range < lim and y_range < lim and z_range < lim:
            return
        if x_range < lim:
            self.ax.set_xlim([-lim, lim])
        if y_range < lim:
            self.ax.set_ylim([-lim, lim])
        if z_range < lim:
            self.ax.set_zlim([-lim, lim])

    def plot(self, trajectory, line="--", color="#{:06x}".format(random.randint(0, 0xFFFFFF)).upper(), xc=1, yc=2, zc=3, label=None):
        xs = np.array([x[xc] for x in trajectory])
        ys = np.array([x[yc] for x in trajectory])
        zs = np.array([x[zc] for x in trajectory])
        if not self.use3d:
            self.ax.plot(xs, ys, line, color=color, label=label)
        else:
            x_range = max(xs) - min(xs)
            y_range = max(ys) - min(ys)
            z_range = max(zs) - min(zs)
            self.ax._set_scaling(x_range, y_range, z_range, 1)
            self.ax.plot(xs, ys, zs, line, color=color, label=label)


    def show(self):
        self.fig.show()

    def save(self, name="geodesics.png", dpi=300, showlegend=False):
        if showlegend:
            self.ax.legend()
        self.fig.savefig(name, dpi=dpi)
