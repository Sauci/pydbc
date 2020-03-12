import pytest

from .pydbc import *

random_strings = ['a', '0']


@pytest.mark.parametrize('prop, value', (
        ('version', None),
        ('new_symbols', None),
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
