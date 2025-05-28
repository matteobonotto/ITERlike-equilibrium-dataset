from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from .types import _TypeNpFloat
from .equil import Equilibrium

def contourf(
    z: _TypeNpFloat,
    RR: _TypeNpFloat,
    ZZ: _TypeNpFloat,
    title: str = "",
    separatrix: Optional[_TypeNpFloat] = None,
) -> None:
    plt.figure()
    plt.contourf(RR, ZZ, z, 20)
    plt.axis("equal")
    plt.colorbar()
    if separatrix is not None:
        plt.plot(separatrix[:, 0], separatrix[:, 1], "r")
    plt.title(title)
    plt.show()


def contour(
    z: _TypeNpFloat,
    RR: _TypeNpFloat,
    ZZ: _TypeNpFloat,
    separatrix: Optional[_TypeNpFloat] = None,
) -> None:
    plt.figure()
    plt.contour(RR, ZZ, z, 20)
    plt.axis("equal")
    if separatrix is not None:
        plt.plot(separatrix[:, 0], separatrix[:, 1], "k")
    plt.colorbar()
    plt.show()


def contour_diff(
    z_ref: _TypeNpFloat, z: _TypeNpFloat, RR: _TypeNpFloat, ZZ: _TypeNpFloat
) -> None:
    l1 = mlines.Line2D([], [], label="DNN")
    l2 = mlines.Line2D([], [], color="black", label="FRIDA")

    plt.figure()
    plt.contour(RR, ZZ, z, 10)
    plt.colorbar()
    plt.contour(RR, ZZ, z_ref, 10, colors="black", linestyles="dashed")
    plt.legend(handles=[l1, l2])
    plt.axis("equal")
    plt.show()



def plot_equilibrium(
    equilibrium: Equilibrium
) -> None:

    flux = equilibrium.flux
    jphi = equilibrium.jphi
    coil_curr = equilibrium.coils_current
    mag_measures = equilibrium.mag_measures
    p_profile = equilibrium.p_profile
    RR = equilibrium.grid.r
    ZZ = equilibrium.grid.z
    first_wall = equilibrium.first_wall
    separatrix = equilibrium.separatrix

    def contourf(z, RR, ZZ, title="", separatrix=None, first_wall=None, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        c = ax.contourf(RR, ZZ, z, 20)
        ax.axis("equal")
        plt.colorbar(c, ax=ax)
        if separatrix is not None:
            ax.plot(separatrix[:, 0], separatrix[:, 1], "r")
        if first_wall is not None:
            ax.plot(first_wall.r, first_wall.z, "k")
        ax.set_title(title)

    # Create figure and master GridSpec
    fig = plt.figure(figsize=(15, 10))
    outer = gridspec.GridSpec(
        nrows=1, ncols=3, width_ratios=[1, 1, 1.2], wspace=0.3
    )

    # Contour plots (left and middle) take full height
    ax1 = fig.add_subplot(outer[0, 0])
    contourf(flux, RR, ZZ, separatrix=separatrix, first_wall=first_wall, title="flux", ax=ax1)

    ax2 = fig.add_subplot(outer[0, 1])
    contourf(jphi, RR, ZZ, separatrix=separatrix, first_wall=first_wall, title="jphi", ax=ax2)

    # Right column: nested GridSpec for vertical stacking
    inner = gridspec.GridSpecFromSubplotSpec(
        3, 1, subplot_spec=outer[0, 2], hspace=0.5
    )

    ax3 = fig.add_subplot(inner[0])
    ax4 = fig.add_subplot(inner[1])
    ax5 = fig.add_subplot(inner[2])

    # plot measures
    ax3.scatter(np.arange(mag_measures.shape[0]), mag_measures.reshape(-1, 1))
    ax3.set_title("magnetic measures")
    ax3.set_xlabel("sensor ID")
    ax3.grid(True)

    # plot currents
    ax4.scatter(np.arange(coil_curr.shape[0]), coil_curr.reshape(-1, 1))
    ax4.set_title("coils current ")
    ax4.set_xlabel("coil ID")
    ax4.grid(True)

    # plot p profile
    ax5.plot(np.linspace(0, 1, p_profile.shape[0]), p_profile.reshape(-1, 1))
    ax5.set_title("p profile")
    ax5.set_xlabel("normalized radius")
    ax5.grid(True)

    plt.show()
