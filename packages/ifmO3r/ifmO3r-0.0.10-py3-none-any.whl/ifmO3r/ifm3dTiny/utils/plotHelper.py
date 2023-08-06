"""
Author: ifm

This is a helper script: it contains functions for plotting 2D / 3D data.

Simple use cas:
    from plot_helper import *

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plotAmp(ax, data['amplitude'], title='Amplitude',cbar=False)
    plt.show()
"""

import numpy as np
from matplotlib.colorbar import ColorbarBase,cm,make_axes
from matplotlib.colors import Normalize

def plot3d(ax,x,y,z,title='3D Image'):
    """
    function for plotting 3D data
    :param ax: matplotlib.pyplot axis object
    :param x: X coordinates of the point cloud data
    :param y: Y coordinates of the point cloud data
    :param z: Z coordinates of the point cloud data
    :param title: figure title
    :return:
    """
    colmap = 'viridis'
    cmap = cm.get_cmap(colmap)
    ax.scatter(x.flatten(), y.flatten(), z.flatten(), c=z.flatten(), cmap=cmap, marker='.')
    # Layout
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    #ax.set_zlabel('Z')

def plotAmp(ax,amp,title='Amplitude',cbar=True):
    """
    function for plotting 2D data, i.e. amplitude data
    :param ax: matplotlib.pyplot axis object
    :param amp: numpy array containing amplitude data
    :param title: figure title
    :param cbar: str desc color bar name
    :return:
    """
    colmap = 'viridis'
    cmap = cm.get_cmap(colmap)
    mynorm=Normalize(vmin=np.min(amp), vmax=np.max(amp))

    ax.imshow(amp,interpolation='none', cmap=cmap)

    ax.set_title(title)
    if cbar:
        cbax, kw = make_axes(ax, orientation='vertical')
        cb1 = ColorbarBase(cbax, cmap=cmap, norm=mynorm, orientation='vertical')
        return ax, cbax
    else:
        return ax
