from argparse import ArgumentParser, Namespace
from typing import Optional, Dict, Any
import yaml  # type: ignore
from pathlib import Path
import re
import pickle
import json
import h5py
from sklearn.preprocessing import StandardScaler


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("config", help="path to config file")
    args, _ = parser.parse_known_args()
    return args


def write_h5(
    data: Dict[str, Any],
    filename: str,
    dtype: str = "float64",
) -> None:
    compression: str = "lzf"
    kwargs = {
        "dtype": dtype,
        "compression": compression,
    }
    with h5py.File(filename + ".h5", "w") as hf:
        for key, item in data.items():
            hf.create_dataset(key, data=item, shape=item.shape, **kwargs)
    hf.close()


def read_h5_numpy(
    filename: str,
) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    with h5py.File(filename, "r") as hf:
        for key, item in hf.items():
            data.update({key: item[()]})
    return data
