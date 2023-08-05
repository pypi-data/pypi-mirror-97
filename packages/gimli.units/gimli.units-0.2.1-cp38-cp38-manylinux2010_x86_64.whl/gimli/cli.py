import sys
from functools import partial
from io import StringIO

import click
import numpy as np

from ._udunits2 import IncompatibleUnitsError, UnitNameError, UnitSystem
from .utils import err, out


@click.command()
@click.version_option()
@click.argument("filename", type=click.File("rb"), nargs=-1)
@click.option("-f", "--from", "from_", default="1", metavar="UNIT")
@click.option("-t", "--to", default="1", metavar="UNIT")
@click.option("--data", default="")
@click.pass_context
def gimli(ctx, from_, to, data, filename):
    load = partial(np.loadtxt, delimiter=",")
    dump = partial(np.savetxt, sys.stdout, delimiter=", ", fmt="%f")

    if data:
        data = (StringIO(data),)
    else:
        data = ()

    system = UnitSystem()

    src_unit = get_unit_from_system(ctx, from_, system)
    dst_unit = get_unit_from_system(ctx, to, system)

    try:
        src_to_dst = src_unit.to(dst_unit)
    except IncompatibleUnitsError:
        err(f"incompatible units: {from_}, {to}")
        ctx.exit(-1)

    out(f"Convering {from_} -> {to}")

    for name in data + filename:
        array = load(name)
        dump(np.atleast_1d(src_to_dst(array, out=array)))

    ctx.exit(0)


def get_unit_from_system(ctx, unit, system):
    try:
        return system.Unit(unit)
    except UnitNameError:
        err(f"unknown or poorly-formed unit: {unit}")
        ctx.exit(-1)
