import pytest

from pygeoutils import InvalidInputType, InvalidInputValue


def invalid_type():
    raise InvalidInputType("coords", "tuple", "(lon, lat)")


def test_invalid_type():
    with pytest.raises(InvalidInputType):
        invalid_type()


def invalid_value():
    raise InvalidInputValue("outFormat", ["json", "geojson"])


def test_invalid_value():
    with pytest.raises(InvalidInputValue):
        invalid_value()
