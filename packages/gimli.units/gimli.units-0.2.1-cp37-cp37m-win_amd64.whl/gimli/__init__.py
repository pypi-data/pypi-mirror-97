import pkg_resources

from ._udunits2 import (
    Unit,
    UnitEncoding,
    UnitFormatting,
    UnitNameError,
    UnitStatus,
    UnitSystem,
)
from .errors import IncompatibleUnitsError


units = UnitSystem()

__version__ = pkg_resources.get_distribution("gimli.units").version
__all__ = [
    "units",
    "IncompatibleUnitsError",
    "Unit",
    "UnitEncoding",
    "UnitFormatting",
    "UnitNameError",
    "UnitStatus",
    "UnitSystem",
]

del pkg_resources
