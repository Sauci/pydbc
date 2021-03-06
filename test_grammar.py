import pytest
import pytest_cases

from .pydbc import *

doubles = [0.0]
char_strings = ['"s"']
empty_string = ''
random_strings = ['a']
c_identifiers = ['_']
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
unsigned_integers = [0]
multiplexer_indicators = [' ', 'M', 'm0']
access_types = ['DUMMY_NODE_VECTOR0',
                'DUMMY_NODE_VECTOR1',
                'DUMMY_NODE_VECTOR2',
                'DUMMY_NODE_VECTOR3']


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
def value_table(value_table_name, value_descriptions_count, value_description_0, value_description_1):
    value_description_0_string, value_description_0_value = value_description_0
    value_description_1_string, value_description_1_value = value_description_1
    value_descriptions_string = [value_description_0_string, value_description_1_string][:value_descriptions_count]
    value_descriptions_value = [value_description_0_value, value_description_1_value][:value_descriptions_count]
    return ('VAL_TABLE_ {} {} ;'.format(value_table_name, ' '.join(value_descriptions_string)),
            ValTable(value_table_name, value_descriptions_value))


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('value_tables_count', [1, 2])
@pytest_cases.parametrize_plus('value_table_0', [pytest_cases.fixture_ref('value_table')])
@pytest_cases.parametrize_plus('value_table_1', [pytest_cases.fixture_ref('value_table')])
def value_tables(value_tables_count, value_table_0, value_table_1):
    value_table_0_string, value_table_0_value = value_table_0
    value_table_1_string, value_table_1_value = value_table_1
    value_tables_string = '\n'.join([value_table_0_string, value_table_1_string][:value_tables_count])
    value_tables_value = [value_table_0_value, value_table_1_value][:value_tables_count]
    return value_tables_string, value_tables_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('receivers_count', [1, 2])
@pytest.mark.parametrize('receiver_0', c_identifiers + ['Vector_XXX'])
@pytest.mark.parametrize('receiver_1', c_identifiers + ['Vector_XXX'])
def receivers(receivers_count, receiver_0, receiver_1):
    receivers_string = ', '.join([receiver_0, receiver_1][:receivers_count])
    receivers_value = [receiver_0, receiver_1][:receivers_count]
    return receivers_string, receivers_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('transmitters_count', [1, 2])
@pytest.mark.parametrize('transmitter_0', c_identifiers + ['Vector_XXX'])
@pytest.mark.parametrize('transmitter_1', c_identifiers + ['Vector_XXX'])
def transmitters(transmitters_count, transmitter_0, transmitter_1):
    transmitters_string = '\n'.join([transmitter_0, transmitter_1][:transmitters_count])
    transmitters_value = [transmitter_0, transmitter_1][:transmitters_count]
    return transmitters_string, transmitters_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('access_nodes_count', [1, 2])
@pytest.mark.parametrize('access_node_0', c_identifiers + ['Vector_XXX'])
@pytest.mark.parametrize('access_node_1', c_identifiers + ['Vector_XXX'])
def access_nodes(access_nodes_count, access_node_0, access_node_1):
    access_nodes_string = ', '.join([access_node_0, access_node_1][:access_nodes_count])
    access_nodes_value = [access_node_0, access_node_1][:access_nodes_count]
    return access_nodes_string, access_nodes_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('signal_name', c_identifiers)
@pytest.mark.parametrize('multiplexer_indicator', multiplexer_indicators)
@pytest.mark.parametrize('start_bit', unsigned_integers)
@pytest.mark.parametrize('signal_size', unsigned_integers)
@pytest.mark.parametrize('byte_order', ['0', '1'])
@pytest.mark.parametrize('value_type', ['+', '-'])
@pytest.mark.parametrize('factor', doubles)
@pytest.mark.parametrize('offset', doubles)
@pytest.mark.parametrize('minimum', doubles)
@pytest.mark.parametrize('maximum', doubles)
@pytest.mark.parametrize('unit', char_strings)
@pytest_cases.parametrize_plus('rs', [pytest_cases.fixture_ref('receivers')])
def signal(signal_name,
           multiplexer_indicator,
           start_bit,
           signal_size,
           byte_order,
           value_type,
           factor,
           offset,
           minimum,
           maximum,
           unit,
           rs):
    receivers_string, receivers_value = rs
    return ('SG_ {} {} : {} | {} @ {} {} ({}, {}) [ {} | {} ] {} {}'.format(signal_name,
                                                                            multiplexer_indicator,
                                                                            start_bit,
                                                                            signal_size,
                                                                            byte_order,
                                                                            value_type,
                                                                            factor,
                                                                            offset,
                                                                            minimum,
                                                                            maximum,
                                                                            unit,
                                                                            receivers_string),
            Signal(signal_name,
                   multiplexer_indicator,
                   start_bit,
                   signal_size,
                   byte_order,
                   value_type,
                   factor,
                   offset,
                   minimum,
                   maximum,
                   unit,
                   receivers_value))


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('signals_count', [1, 2])
@pytest_cases.parametrize_plus('signal_0', [pytest_cases.fixture_ref('signal')])
@pytest_cases.parametrize_plus('signal_1', [pytest_cases.fixture_ref('signal')])
def signals(signals_count, signal_0, signal_1):
    signal_0_string, signal_0_value = signal_0
    signal_1_string, signal_1_value = signal_1
    signals_string = '\n'.join([signal_0_string, signal_1_string][:signals_count])
    signals_value = [signal_0_value, signal_1_value][:signals_count]
    return signals_string, signals_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('message_id', unsigned_integers)
@pytest.mark.parametrize('message_name', c_identifiers)
@pytest.mark.parametrize('message_size', unsigned_integers)
@pytest.mark.parametrize('transmitter', c_identifiers + ['Vector_XXX'])
@pytest_cases.parametrize_plus('ss', [pytest_cases.fixture_ref('signals')])
def message(message_id, message_name, message_size, transmitter, ss):
    signals_string, signals_value = ss
    return ('BO_ {} {} : {} {} {}'.format(message_id, message_name, message_size, transmitter, signals_string),
            Message(message_id, message_name, message_size, transmitter, signals_value))


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('messages_count', [1, 2])
@pytest_cases.parametrize_plus('message_0', [pytest_cases.fixture_ref('message')])
@pytest_cases.parametrize_plus('message_1', [pytest_cases.fixture_ref('message')])
def messages(messages_count, message_0, message_1):
    message_0_string, message_0_value = message_0
    message_1_string, message_1_value = message_1
    messages_string = '\n'.join([message_0_string, message_1_string][:messages_count])
    messages_value = [message_0_value, message_1_value][:messages_count]
    return messages_string, messages_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('message_id', unsigned_integers)
@pytest_cases.parametrize_plus('ts', [pytest_cases.fixture_ref('transmitters')])
def message_transmitter(message_id, ts):
    transmitters_string, transmitters_value = ts
    return ('BO_TX_BU_ {} : {} ;'.format(message_id, transmitters_string),
            MessageTransmitter(message_id, transmitters_value))


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('message_transmitters_count', [1, 2])
@pytest_cases.parametrize_plus('message_transmitter_0', [pytest_cases.fixture_ref('message_transmitter')])
@pytest_cases.parametrize_plus('message_transmitter_1', [pytest_cases.fixture_ref('message_transmitter')])
def message_transmitters(message_transmitters_count, message_transmitter_0, message_transmitter_1):
    message_transmitter_0_string, message_transmitter_0_value = message_transmitter_0
    message_transmitter_1_string, message_transmitter_1_value = message_transmitter_1
    message_transmitters_string = '\n'.join([message_transmitter_0_string,
                                             message_transmitter_1_string][:message_transmitters_count])
    message_transmitters_value = [message_transmitter_0_value, message_transmitter_1_value][:message_transmitters_count]
    return message_transmitters_string, message_transmitters_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('env_var_name', c_identifiers)
@pytest.mark.parametrize('env_var_type', unsigned_integers)  # TODO: allowed values are 0, 1 and 2, add a check?...
@pytest.mark.parametrize('minimum', doubles)
@pytest.mark.parametrize('maximum', doubles)
@pytest.mark.parametrize('unit', char_strings)
@pytest.mark.parametrize('initial_value', doubles)
@pytest.mark.parametrize('ev_id', unsigned_integers)
@pytest.mark.parametrize('access_type', access_types)
@pytest_cases.parametrize_plus('access_node', [pytest_cases.fixture_ref('access_nodes')])
def environment_variable(env_var_name,
                         env_var_type,
                         minimum,
                         maximum,
                         unit,
                         initial_value,
                         ev_id,
                         access_type,
                         access_node):
    access_nodes_string, access_nodes_value = access_node
    return ('EV_ {} : {} [ {} | {} ] {} {} {} {} {} ;'.format(env_var_name,
                                                              env_var_type,
                                                              minimum,
                                                              maximum,
                                                              unit,
                                                              initial_value,
                                                              ev_id,
                                                              access_type,
                                                              access_nodes_string),
            EnvironmentVariable(env_var_name,
                                env_var_type,
                                minimum,
                                maximum,
                                unit,
                                initial_value,
                                ev_id,
                                access_type,
                                access_nodes_value))


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('environment_variables_count', [1, 2])
@pytest_cases.parametrize_plus('environment_variable_0', [pytest_cases.fixture_ref('environment_variable')])
@pytest_cases.parametrize_plus('environment_variable_1', [pytest_cases.fixture_ref('environment_variable')])
def environment_variables(environment_variables_count, environment_variable_0, environment_variable_1):
    environment_variable_0_string, environment_variable_0_value = environment_variable_0
    environment_variable_1_string, environment_variable_1_value = environment_variable_1
    environment_variable_string = '\n'.join([environment_variable_0_string,
                                             environment_variable_1_string][:environment_variables_count])
    environment_variable_value = [environment_variable_0_value,
                                  environment_variable_1_value][:environment_variables_count]
    return environment_variable_string, environment_variable_value


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('env_var_name', c_identifiers)
@pytest.mark.parametrize('data_size', unsigned_integers)
def environment_variable_data(env_var_name, data_size):
    return 'ENVVAR_DATA_ {} : {} ;'.format(env_var_name, data_size), EnvironmentVariableData(env_var_name, data_size)


@pytest_cases.fixture_plus()
@pytest.mark.parametrize('environment_variable_datas_count', [1, 2])
@pytest_cases.parametrize_plus('environment_variable_data_0', [pytest_cases.fixture_ref('environment_variable_data')])
@pytest_cases.parametrize_plus('environment_variable_data_1', [pytest_cases.fixture_ref('environment_variable_data')])
def environment_variable_datas(environment_variable_datas_count,
                               environment_variable_data_0,
                               environment_variable_data_1):
    environment_variable_data_0_string, environment_variable_data_0_value = environment_variable_data_0
    environment_variable_data_1_string, environment_variable_data_1_value = environment_variable_data_1
    environment_variable_data_string = '\n'.join([environment_variable_data_0_string,
                                                  environment_variable_data_1_string][
                                                 :environment_variable_datas_count])
    environment_variable_data_value = [environment_variable_data_0_value,
                                       environment_variable_data_1_value][:environment_variable_datas_count]
    return environment_variable_data_string, environment_variable_data_value


@pytest.mark.parametrize('prop, value', (
        ('version', None),
        ('new_symbols', tuple()),
        ('bit_timing', None),
        ('nodes', tuple()),
        ('value_tables', tuple()),
        ('messages', tuple()),
        ('message_transmitters', tuple()),
        ('environment_variables', tuple()),
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
    assert isinstance(p.ast.nodes, Nodes)
    assert p.ast.nodes == ([node_name_string_0] if node_name_string_0 else []) + [node_name_string_1]


@pytest_cases.parametrize_plus('vts', [pytest_cases.fixture_ref('value_tables')])
def test_value_tables_node(vts):
    value_table_string, value_table_value = vts
    p = DbcParser(value_table_string)
    assert isinstance(p.ast.value_tables, ValueTables)
    for index, val_table in enumerate(value_table_value):
        assert p.ast.value_tables[index] == val_table


@pytest_cases.parametrize_plus('ms', [pytest_cases.fixture_ref('messages')])
def test_messages_node(ms):
    messages_string, messages_value = ms
    p = DbcParser(messages_string)
    assert isinstance(p.ast.messages, Messages)
    for index, m in enumerate(messages_value):
        assert p.ast.messages[index] == m


@pytest_cases.parametrize_plus('mts', [pytest_cases.fixture_ref('message_transmitters')])
def test_message_transmitters_node(mts):
    message_transmitters_string, message_transmitters_value = mts
    p = DbcParser(message_transmitters_string)
    assert isinstance(p.ast.message_transmitters, MessageTransmitters)
    for index, mt in enumerate(message_transmitters_value):
        assert p.ast.message_transmitters[index] == mt


@pytest_cases.parametrize_plus('evs', [pytest_cases.fixture_ref('environment_variables')])
def test_environment_variables_node(evs):
    environment_variables_string, environment_variables_value = evs
    p = DbcParser(environment_variables_string)
    assert isinstance(p.ast.environment_variables, EnvironmentVariables)
    for index, ev in enumerate(environment_variables_value):
        assert p.ast.environment_variables[index] == ev


@pytest_cases.parametrize_plus('evds', [pytest_cases.fixture_ref('environment_variable_datas')])
def test_environment_variable_datas_node(evds):
    environment_variables_datas_string, environment_variables_datas_value = evds
    p = DbcParser(environment_variables_datas_string)
    assert isinstance(p.ast.environment_variables_data, EnvironmentVariableDatas)
    for index, evd in enumerate(environment_variables_datas_value):
        assert p.ast.environment_variables_data[index] == evd
