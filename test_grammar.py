import pytest
import pytest_cases

from .pydbc import *

doubles = [0.0, -1.0, 1.0]
char_strings = ['"s"', '"_"']
empty_string = ''
random_strings = ['a', '0']
c_identifiers = ['_', '_c']
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


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('double', doubles)
@pytest.mark.parametrize('char_string', char_strings)
def value_table_description(double, char_string):
    return '{} {}'.format(double, char_string), ValueTableDescription(double, char_string)


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('value_table_name', c_identifiers)
@pytest.mark.parametrize('value_descriptions_count', [1, 2])
@pytest_cases.parametrize_plus('value_description_0', [pytest_cases.fixture_ref('value_table_description')])
@pytest_cases.parametrize_plus('value_description_1', [pytest_cases.fixture_ref('value_table_description')])
def value_tables(value_table_name, value_descriptions_count, value_description_0, value_description_1):
    value_description_0_string, value_description_0_value = value_description_0
    value_description_1_string, value_description_1_value = value_description_1
    value_descriptions_string = [value_description_0_string, value_description_1_string][:value_descriptions_count]
    value_descriptions_value = [value_description_0_value, value_description_1_value][:value_descriptions_count]
    return ('VAL_TABLE_ {} {} ;'.format(value_table_name, ' '.join(value_descriptions_string)),
            ValTable(value_table_name, value_descriptions_value))


@pytest.mark.parametrize('prop, value', (
        ('version', None),
        ('new_symbols', tuple()),
        ('bit_timing', None),
        ('nodes', tuple()),
        ('value_tables', tuple()),
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


@pytest.mark.parametrize('bit_timing_string, bit_timing_value', (
        ('', None),
        ('11 : 12 , 13', BitTiming(11, 12, 13))))
def test_bit_timing_node(bit_timing_string, bit_timing_value):
    p = DbcParser('BS_ : {}'.format(bit_timing_string))
    assert p.ast.bit_timing == bit_timing_value


@pytest.mark.parametrize('node_name_string_0', [empty_string] + c_identifiers)
@pytest.mark.parametrize('node_name_string_1', c_identifiers)
def test_nodes_node(node_name_string_0, node_name_string_1):
    p = DbcParser('BU_ : {} {}'.format(node_name_string_0, node_name_string_1))
    assert isinstance(p.ast.nodes, list)
    assert p.ast.nodes == ([node_name_string_0] if node_name_string_0 else []) + [node_name_string_1]


@pytest_cases.parametrize_plus('value_table', [pytest_cases.fixture_ref('value_tables')])
def test_value_tables_node(value_table):
    value_table_string, value_table_value = value_table
    p = DbcParser(value_table_string)
    assert isinstance(p.ast.value_tables, list)
    assert p.ast.value_tables[0] == value_table_value
