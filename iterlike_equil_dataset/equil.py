from dataclasses import dataclass, asdict, field
from typing import Optional, Dict

from .types import _TypeNpFloat
from .constants import mu0


@dataclass
class RZCoordinates:
    r: _TypeNpFloat
    z: _TypeNpFloat

    def asdict(self) -> Dict[str, _TypeNpFloat]:
        return asdict(self)


@dataclass
class Equilibrium:
    flux: _TypeNpFloat
    rhs: _TypeNpFloat
    mag_measures: _TypeNpFloat
    coils_current: _TypeNpFloat
    separatrix: _TypeNpFloat
    p_profile: _TypeNpFloat
    is_diverted: bool
    grid: RZCoordinates
    first_wall: RZCoordinates
    _repr: str = ""
    jphi: _TypeNpFloat = field(init=False)

    def __post_init__(self) -> None:
        self.jphi = -self.rhs / (mu0 * self.grid.r)

    def __repr__(self) -> str:
        return self._repr
