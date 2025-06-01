import pytest
from mistocr.cli import parse_pages


def test_parse_pages_none():
    assert parse_pages(None) is None
    assert parse_pages('') is None


def test_parse_pages_list():
    assert parse_pages('0,1,2') == [0, 1, 2]


def test_parse_pages_range():
    assert parse_pages('0-2') == [0, 1, 2]


def test_parse_pages_mixed():
    assert parse_pages('1,3-5,7') == [1, 3, 4, 5, 7]


@pytest.mark.parametrize('arg', ['a,b', '1-', '-2', '1,a'])
def test_parse_pages_invalid(arg):
    with pytest.raises(ValueError):
        parse_pages(arg)
