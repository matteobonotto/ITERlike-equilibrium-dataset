from dataclasses import dataclass
from typing import Optional

from .types import _TypeNpFloat
from .constants import mu0


@dataclass
class Equilibrium:
    _repr: str = ""
    r: _TypeNpFloat
    z: _TypeNpFloat
    flux: _TypeNpFloat
    rhs: _TypeNpFloat
    mag_measures: _TypeNpFloat
    coils_current: _TypeNpFloat
    separatrix: _TypeNpFloat
    p_profile: _TypeNpFloat
    is_diverted: bool
    jphi: Optional[_TypeNpFloat] = None

    def __post_init__(self):
        self.jphi = -self.rhs / (mu0 * self.r)
        # self._repr =

    def __repr__(self):
        return self._repr
