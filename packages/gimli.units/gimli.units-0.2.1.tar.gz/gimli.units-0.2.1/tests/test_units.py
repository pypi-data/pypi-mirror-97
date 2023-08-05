import os
import random

import numpy as np
import pytest
from numpy.testing import assert_array_almost_equal

from gimli import (
    IncompatibleUnitsError,
    UnitFormatting,
    UnitNameError,
    UnitStatus,
    UnitSystem,
)


@pytest.fixture
def system():
    os.environ.pop("UDUNITS2_XML_PATH", None)
    return UnitSystem()


def test_get_xml():
    os.environ.pop("UDUNITS2_XML_PATH", None)
    path, status = UnitSystem.get_xml_path()
    assert path.is_file()
    assert status == UnitStatus.OPEN_DEFAULT

    path, status = UnitSystem.get_xml_path(path)
    assert path.is_file()
    assert status == UnitStatus.OPEN_ARG

    os.environ["UDUNITS2_XML_PATH"] = str(path)
    path, status = UnitSystem.get_xml_path()
    assert path.is_file()
    assert status == UnitStatus.OPEN_ENV


def test_default_system():
    os.environ.pop("UDUNITS2_XML_PATH", None)
    system = UnitSystem()
    assert system.status == "default"
    assert system.database.is_file()


def test_user_system():
    path = UnitSystem().database
    system = UnitSystem(path)
    assert system.status == "user"
    assert system.database.is_file()
    assert system == UnitSystem()
    assert UnitSystem(path) == UnitSystem(str(path))


def test_env_system(system):
    os.environ["UDUNITS2_XML_PATH"] = str(system.database)
    env_system = UnitSystem()

    assert env_system.status == "env"
    assert env_system.database.is_file()
    assert str(env_system) == str(system)
    assert env_system.database.samefile(system.database)
    assert env_system == system


def test_system_dimensionless(system):
    assert system.dimensionless_unit() == system.Unit("1")
    assert str(system.dimensionless_unit()) == "1"


def test_dimensionless_not_freed_twice():
    system = UnitSystem()
    unit = system.dimensionless_unit()
    del unit
    del system

    system = UnitSystem()
    unit = system.Unit("1")
    del unit
    del system


def test_system_unit_by_name(system):
    assert system.unit_by_name("meter") == system.Unit("m")
    assert system.unit_by_name("meters") == system.Unit("m")
    assert system.unit_by_name("m") is None
    assert system.unit_by_name("meter2") is None
    assert system.unit_by_name("not_a_name") is None


def test_system_unit_by_symbol(system):
    assert system.unit_by_symbol("m") == system.Unit("m")
    assert system.unit_by_symbol("km") is None
    assert system.unit_by_symbol("meter") is None
    assert system.unit_by_symbol("m s-2") is None
    assert system.unit_by_symbol("not_a_symbol") is None


def test_unit_formatting(system):
    unit = system.Unit("0.1 lg(re m/(5 s)^2) @ 50")
    assert (
        unit.format(encoding="ascii", formatting=UnitFormatting.NAMES)
        == "0.1 lg(re 0.04 meter-second^-2) from 50"
    )
    assert (
        unit.format(encoding="ascii", formatting=UnitFormatting.DEFINITIONS)
        == "0.1 lg(re 0.04 m.s-2) @ 50"
    )

    assert (
        unit.format(encoding="iso-8859-1", formatting=UnitFormatting.NAMES)
        == "0.1 lg(re 0.04 meter/second²) from 50"
    )
    assert (
        unit.format(encoding="iso-8859-1", formatting=UnitFormatting.DEFINITIONS)
        == "0.1 lg(re 0.04 m/s²) @ 50"
    )

    assert (
        unit.format(encoding="latin-1", formatting=UnitFormatting.NAMES)
        == "0.1 lg(re 0.04 meter/second²) from 50"
    )
    assert (
        unit.format(encoding="latin-1", formatting=UnitFormatting.DEFINITIONS)
        == "0.1 lg(re 0.04 m/s²) @ 50"
    )

    assert (
        unit.format(encoding="utf-8", formatting=UnitFormatting.NAMES)
        == "0.1 lg(re 0.04 meter·second⁻²) from 50"
    )
    assert (
        unit.format(encoding="utf-8", formatting=UnitFormatting.DEFINITIONS)
        == "0.1 lg(re 0.04 m·s⁻²) @ 50"
    )


@pytest.mark.parametrize(
    ("lhs", "cmp_", "rhs"),
    [
        ("m", "lt", "km"),
        ("m", "le", "km"),
        ("m", "le", "m"),
        ("m", "eq", "m"),
        ("m", "ne", "km"),
        ("km", "ge", "m"),
        ("km", "ge", "km"),
        ("km", "gt", "m"),
    ],
)
def test_unit_comparisons(system, lhs, cmp_, rhs):
    compare = getattr(system.Unit(lhs), f"__{cmp_}__")
    assert compare(system.Unit(rhs))
    with pytest.raises(TypeError):
        compare(rhs)


def test_unit_symbol(system):
    meters = system.Unit("m")
    assert meters.symbol == "m"

    km = system.Unit("km")
    assert km.symbol is None


def test_unit_name(system):
    meters = system.Unit("m")
    assert meters.name == "meter"

    km = system.Unit("km")
    assert km.name is None


def test_unit_is_dimensionless(system):
    assert not system.Unit("m").is_dimensionless
    assert system.Unit("1").is_dimensionless
    assert system.Unit("rad").is_dimensionless


def test_unit_is_convertible(system):
    assert system.Unit("m").is_convertible_to(system.Unit("km"))
    assert not system.Unit("m").is_convertible_to(system.Unit("kg"))

    with pytest.raises(TypeError):
        system.Unit("m").is_convertible_to("km")


def test_unit_converter_length(system):
    meters = system.Unit("m")
    km = system.Unit("km")

    assert meters.to(km)(1.0) == pytest.approx(1e-3)
    with pytest.raises(TypeError):
        meters.to("km")

    m_to_km = meters.to(km)
    assert m_to_km(1.0) == pytest.approx(1e-3)


def test_unit_converter_time(system):
    hours = system.Unit("h")
    seconds = system.Unit("s")
    hours_to_seconds = hours.to(seconds)
    assert hours_to_seconds(1.0) == pytest.approx(3600.0)

    with pytest.raises(TypeError):
        hours.to("s")


def test_unit_converter_same_units(system):
    hours = system.Unit("h")
    hours_to_hours = hours.to(system.Unit("h"))
    assert hours_to_hours(1.0) == pytest.approx(1.0)


@pytest.mark.parametrize(
    ("to_", "from_"),
    [("not_a_unit", "m"), ("m", "not_a_unit"), ("not_a_unit", "not_a_unit")],
)
def test_unit_converter_bad_from_units(system, to_, from_):
    with pytest.raises(UnitNameError):
        system.Unit(from_).to(system.Unit(to_))


def test_unit_converter_incompatible_units(system):
    with pytest.raises(IncompatibleUnitsError) as exc_info:
        system.Unit("s").to(system.Unit("m"))
    assert "incompatible units" in str(exc_info.value)


def test_unit_converter_inverse(system):
    val = random.random()
    seconds_to_hours = system.Unit("s").to(system.Unit("h"))
    hours_to_seconds = system.Unit("h").to(system.Unit("s"))
    assert hours_to_seconds(seconds_to_hours(val)) == pytest.approx(val)


@pytest.mark.parametrize("dtype", (np.single, np.double))
@pytest.mark.parametrize("shape", [(5,), (5, 1), (4, 5), (5, 6, 7)])
def test_unit_converter_double_array(system, shape, dtype):
    meters = system.Unit("m")
    km = system.Unit("km")

    m_to_km = meters.to(km)
    values_in_m = np.ones(shape, dtype=dtype)
    values_in_km = m_to_km(values_in_m)
    assert_array_almost_equal(values_in_m, values_in_km * 1000.0)
    assert values_in_km.dtype == dtype


@pytest.mark.parametrize("dtype", (np.single, np.double))
@pytest.mark.parametrize("shape", [(5,), (5, 1), (4, 5), (5, 6, 7)])
def test_unit_converter_dtype_array_out_keyword(system, shape, dtype):
    meters = system.Unit("m")
    km = system.Unit("km")

    m_to_km = meters.to(km)
    values_in_m = np.ones(shape, dtype=dtype)
    values_in_km = np.empty_like(values_in_m)

    rtn = m_to_km(values_in_m, out=values_in_km)
    assert_array_almost_equal(values_in_m, values_in_km * 1000.0)
    assert rtn.dtype == dtype
    assert rtn is values_in_km


@pytest.mark.parametrize("dtype", ("int", "uint8", "bool"))
def test_unit_converter_non_float_dtype(system, dtype):
    meters = system.Unit("m")
    dm = system.Unit("dm")

    m_to_dm = meters.to(dm)
    values_in_m = np.ones(10, dtype=dtype)

    values_in_dm = m_to_dm(values_in_m)
    assert values_in_dm.dtype == np.double
    assert_array_almost_equal(values_in_m, values_in_dm / 10.0)

    with pytest.raises(ValueError):
        values_in_dm = np.empty(10, dtype=dtype)
        m_to_dm(values_in_m, out=values_in_dm)


@pytest.mark.parametrize(
    "src_dtype,dst_dtype",
    ((np.single, np.double), (np.double, np.single)),
)
def test_unit_converter_wrong_out_dtype(system, src_dtype, dst_dtype):
    meters = system.Unit("m")
    km = system.Unit("km")

    m_to_km = meters.to(km)
    values_in_m = np.ones(100, dtype=src_dtype)
    values_in_km = np.empty_like(values_in_m, dst_dtype)
    with pytest.raises(ValueError):
        m_to_km(values_in_m, out=values_in_km)


@pytest.mark.parametrize("dtype", (np.single, np.double))
def test_unit_converter_in_place(system, dtype):
    meters = system.Unit("m")
    km = system.Unit("km")

    m_to_km = meters.to(km)
    values_in_m = np.ones((10, 5), dtype=dtype)
    rtn = m_to_km(values_in_m, out=values_in_m)
    assert rtn is values_in_m
    assert_array_almost_equal(rtn, 1e-3)


def test_unit_converter_non_contiguous(system):
    meters = system.Unit("m")
    km = system.Unit("km")

    m_to_km = meters.to(km)
    values_in_m = np.ones((10, 5), dtype=float)
    values_in_km = np.empty_like(values_in_m).T
    with pytest.raises(ValueError):
        m_to_km(values_in_m, out=values_in_km)
