from datasets import load_dataset
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from .types import _TypeNpFloat
from .constants import mu0


root = Path(os.path.realpath(__file__))


@dataclass
class RZCoordinates:
    r: _TypeNpFloat
    z: _TypeNpFloat

    def asdict(self) -> Dict[str, _TypeNpFloat]:
        return asdict(self)


class IterlikeDataset:

    def __init__(self, dataset_id: str = "matteobonotto/iterlike_equil_sample"):
        print("Loading eqilibrium data")
        self.equil_data = load_dataset(dataset_id, split="train").with_format("numpy")

        print("Load geometry data")

        grid = json.load(open(root.parent / Path("data/grid.json"), "r"))
        self.grid = RZCoordinates(**{k: np.array(v) for k, v in grid.items()})
        first_wall = json.load(open(root.parent / Path("data/first_wall.json"), "r"))
        self.first_wall = RZCoordinates(
            **{k: np.array(v) for k, v in first_wall.items()}
        )
        print("done")

    def __getitem__(self, idx: int) -> Any:
        return self.equil_data[idx]

    def __len__(self) -> int:
        return len(self.equil_data)

    def __repr__(self) -> str:
        s = f"ITER-like equilibrium dataset with {len(self.equil_data)} samples and keys:\n"
        for k, v in self.equil_data.features.items():
            s += f" {k}\n"
        return s

    def plot_sample(
        self, idx: Optional[int] = None, use_plotly: Optional[bool] = False
    ):
        if idx is None:
            idx = random.randint(0, len(self))
        sample = self[idx]

        z1 = sample["flux"]
        z2 = -sample["rhs"] / (mu0 * self.grid.r)
        coil_curr = sample["coils_current"]
        mag_measures = sample["mag_measures"]
        p_profile = sample["p_profile"]
        RR = self.grid.r
        ZZ = self.grid.z
        separatrix = sample["separatrix"]
        title = "flux"

        def contourf(z, RR, ZZ, title="", separatrix=None, ax=None):
            if ax is None:
                fig, ax = plt.subplots()
            c = ax.contourf(RR, ZZ, z, 20)
            ax.axis("equal")
            plt.colorbar(c, ax=ax)
            if separatrix is not None:
                ax.plot(separatrix[:, 0], separatrix[:, 1], "k")
            ax.set_title(title)

        # Create figure and master GridSpec
        fig = plt.figure(figsize=(15, 10))
        outer = gridspec.GridSpec(
            nrows=1, ncols=3, width_ratios=[1, 1, 1.2], wspace=0.3
        )

        # Contour plots (left and middle) take full height
        ax1 = fig.add_subplot(outer[0, 0])
        contourf(z1, RR, ZZ, separatrix=separatrix, title="flux", ax=ax1)

        ax2 = fig.add_subplot(outer[0, 1])
        contourf(z2, RR, ZZ, separatrix=separatrix, title="jphi", ax=ax2)

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
        ax3.set_xlabel("normalized radius")
        ax5.grid(True)

        plt.show()
