import pytest

from .pydbc import *

empty_string = ''
random_strings = ['a', '0']
new_symbols_strings = ['CM_',
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
                       'BU_BO_REL_']


@pytest.mark.parametrize('prop, value', (
        ('version', None),
        ('new_symbols', tuple()),
        ('bit_timing', None),
        ('nodes', None),
        ('value_tables', None),
        ('messages', None),
        ('message_transmitters', None),
        ('environment_variables', None),
        ('environment_variables_data', None),
        ('signal_types', None),
        ('comments', None),
        ('attribute_definitions', None),
        ('sigtype_attr_list', None),
        ('attribute_defaults', None),
        ('attribute_values', None),
        ('value_descriptions', None),
        ('category_definitions', None),
        ('categories', None),
        ('filter', None),
        ('signal_type_refs', None),
        ('signal_groups', None),
        ('signal_extended_value_type_list', None),
        ('multiplexed_signals', None)))
def test_empty_file(prop, value):
    p = DbcParser('')
    assert isinstance(p.ast, DbcFile)
    assert getattr(p.ast, prop) == value


@pytest.mark.parametrize('version_string', random_strings)
def test_version_node(version_string):
    p = DbcParser('VERSION "{}"'.format(version_string))
    assert isinstance(p.ast.version, Version)
    assert p.ast.version == version_string


@pytest.mark.parametrize('new_symbols_string_0', [empty_string] + new_symbols_strings)
@pytest.mark.parametrize('new_symbols_string_1', new_symbols_strings)
def test_new_symbols_node(new_symbols_string_0, new_symbols_string_1):
    p = DbcParser('NS_ : {} {}'.format(new_symbols_string_0, new_symbols_string_1))
    assert isinstance(p.ast.new_symbols, list)
    assert p.ast.new_symbols == ([new_symbols_string_0] if new_symbols_string_0 else []) + [new_symbols_string_1]
