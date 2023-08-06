import xltoy
from xltoy.collector import Collector, DiffCollector
from xltoy.utils import is_vertical_range
import os
import pytest

base_data_url = os.path.join(os.path.dirname(os.path.dirname(xltoy.__file__)),'data')



def coll(url):
    url=os.path.join(base_data_url,url)
    return Collector(url)


@pytest.mark.collector
@pytest.mark.parametrize("f", [src for src in list(os.walk(base_data_url))[0][2] if src.endswith('.xlsx')])
def test_injestion(f):
    coll(f)


@pytest.mark.collector
@pytest.mark.parametrize("rng", [['A1','A2','A3','$A$4','$A5','A$12','$A$13']])
def test_is_vertical(rng):
    assert is_vertical_range(rng) is False


@pytest.mark.collector
@pytest.mark.parametrize("rng", [['AA1','AA2','AA3','$AA5','$AA$6']])
def test_is_horiz(rng):
    assert is_vertical_range(rng) is False


@pytest.mark.collector
@pytest.mark.parametrize("rng",[['A1','B2','C3']])
def test_not_valid_range(rng):
    with pytest.raises(ValueError):
        is_vertical_range(rng) is True

@pytest.mark.collector
@pytest.mark.parametrize("rng",[])
def test_empty_valid_range(rng):
    with pytest.raises(ValueError):
        is_vertical_range(rng)

@pytest.mark.collector
@pytest.mark.parametrize("f", [src for src in list(os.walk(base_data_url))[0][2] if src.endswith('.xlsx')])
def test_diff(f):
    f = os.path.join(base_data_url, f)
    stone_f = os.path.join(
                  base_data_url,
                  os.path.splitext(f)[0]+'.yaml')
    if os.path.exists(stone_f):
        assert not DiffCollector(f, stone_f).diff


@pytest.mark.collector
@pytest.mark.parametrize("f", [src for src in list(os.walk(base_data_url))[0][2] if src.endswith('.xlsx')])
def test_diff_parsed(f):
    f = os.path.join(base_data_url, f)
    stone_f = os.path.join(
                  base_data_url,
                  os.path.splitext(f)[0]+'.parsed.yaml')
    if os.path.exists(stone_f):
        assert not DiffCollector(f, stone_f, parsed=True).diff
