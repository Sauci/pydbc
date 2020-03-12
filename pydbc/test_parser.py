import pytest

from .node import *
from dbc_parser.pydbc.parser.parser import DbcParser

random_strings = ['a', '0']
new_symbol_strings = [
    'NS_DESC_',
    'CM_',
    'BA_DEF_',
    'BA_',
    'VAL_',
    'CAT_DEF_',
    'CAT_',
    'FILTER',
    'BA_DEF_DEF_',
    'EV_DATA_',
    'ENVVAR_DATA_',
    'SGTYPE_',
    'SGTYPE_VAL_',
    'BA_DEF_SGTYPE_',
    'BA_SGTYPE_',
    'SIG_TYPE_REF_',
    'VAL_TABLE_',
    'SIG_GROUP_',
    'SIG_VALTYPE_',
    'SIGTYPE_VALTYPE_',
    'BO_TX_BU_',
    'BA_DEF_REL_',
    'BA_REL_',
    'BA_DEF_DEF_REL_',
    'BU_SG_REL_',
    'BU_EV_REL_',
    'BU_BO_REL_',
]


def test_empty_file():
    p = DbcParser('')
    assert p.ast is None


@pytest.mark.parametrize('new_symbol_string, value', [(s, [s]) for s in new_symbol_strings])
def test_new_symbols_node(new_symbol_string, value):
    p = DbcParser("""
NS_ : 
    {}""".format(new_symbol_string))
    assert p.ast.new_symbols == value


@pytest.mark.parametrize('version_string', random_strings)
def test_version_node(version_string):
    p = DbcParser('VERSION "{}"'.format(version_string))
    assert isinstance(p.ast.version, Version)
    assert p.ast.version == version_string
