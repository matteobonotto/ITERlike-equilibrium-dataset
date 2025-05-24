from datasets import load_dataset, Dataset
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

import numpy as np

from .equil import Equilibrium, RZCoordinates


root = Path(os.path.realpath(__file__))




class IterlikeDataset:

    def __init__(self, dataset_id: str = "matteobonotto/iterlike-equil-sample"):
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

    def get_huggingface_dataset(self) -> Dataset:
        return self.equil_data

    def __getitem__(self, idx: int) -> Any:
        return Equilibrium(grid=self.grid, first_wall=self.first_wall, **self.equil_data[idx])

    def __len__(self) -> int:
        return len(self.equil_data)

    def __repr__(self) -> str:
        s = f"ITER-like equilibrium dataset with {len(self.equil_data)} samples and keys:\n"
        for k, v in self.equil_data.features.items():
            s += f" {k}\n"
        return s

