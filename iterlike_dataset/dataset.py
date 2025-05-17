from datasets import load_dataset
import json
import os
from pathlib import Path
import numpy as np
from typing import Dict, Any
from dataclasses import dataclass, asdict

from .types import _TypeNpFloat

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
