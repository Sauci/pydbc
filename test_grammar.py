import pytest

from .pydbc import *

random_strings = ['a', '0']


def test_empty_file():
    p = DbcParser('')
    assert p.ast is None


@pytest.mark.parametrize('version_string', random_strings)
def test_version_node(version_string):
    p = DbcParser('VERSION "{}"'.format(version_string))
    assert isinstance(p.ast.version, Version)
    assert p.ast.version == version_string
