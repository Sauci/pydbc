import os

import ply.yacc as yacc

from .exception import FormatException
from .lexer import tokens as lex_tokens
from .node import *


class DbcParser(object):
    tokens = lex_tokens

    def __init__(self, string):
        self._ast = list()
        self._yacc = yacc.yacc(debug=True, module=self, optimize=True,
                               outputdir=os.path.dirname(os.path.realpath(__file__)))
        self._yacc.parse(string)

    @staticmethod
    def p_error(p):
        if p:
            raise FormatException('invalid sequence at position ', p.lexpos, string=p.lexer.lexdata)
        else:
            raise FormatException('unvalid sequence in root node ', 0, string='')

    @property
    def ast(self):
        return self._ast

    def p_dbc(self, p):
        """dbc : empty
               | dbc_optionals_list"""
        kwargs = dict()
        if p[1] is not None:
            kwargs = dict(p[1])
        self._ast = DbcFile(**kwargs)

    @staticmethod
    def p_dbc_optionals_list(p):
        """dbc_optionals_list : dbc_optionals
                              | dbc_optionals dbc_optionals_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_dbc_optionals(p):
        """dbc_optionals : version
                         | new_symbols
                         | bit_timing
                         | nodes
                         | value_tables
                         | messages
                         | message_transmitters
                         | environment_variables
                         | environment_variables_data
                         | comments
                         | attribute_definitions
                         | attribute_defaults
                         | attribute_values
                         | value_descriptions
                         | multiplexed_signals"""
        p[0] = p.slice[1].type, p[1]

    @staticmethod
    def p_environment_variables_data(p):
        """environment_variables_data : environment_variable_data_list"""
        if p[1] is not None:
            environment_variables_data = p[1]
        else:
            environment_variables_data = []
        p[0] = EnvironmentVariableDatas(environment_variables_data)

    @staticmethod
    def p_environment_variable_data_list(p):
        """environment_variable_data_list : environment_variable_data
                                          | environment_variable_data environment_variable_data_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_environment_variable_data(p):
        """environment_variable_data : ENVVAR_DATA_ IDENT COLON NUMERIC SEMICOLON"""
        p[0] = EnvironmentVariableData(p[2], p[4])

    @staticmethod
    def p_environment_variables(p):
        """environment_variables : environment_variable_list"""
        if p[1] is not None:
            environment_variables = p[1]
        else:
            environment_variables = []
        p[0] = EnvironmentVariables(environment_variables)

    @staticmethod
    def p_environment_variable_list(p):
        """environment_variable_list : environment_variable
                                     | environment_variable environment_variable_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_environment_variable(p):
        """environment_variable : EV_ IDENT COLON env_var_type BRACE_OPEN NUMERIC VERTICAL_BAR NUMERIC BRACE_CLOSE STRING NUMERIC NUMERIC access_type access_node_list SEMICOLON"""
        p[0] = EnvironmentVariable(p[2], p[4], p[6], p[8], p[10], p[11], p[12], p[13], p[14])

    @staticmethod
    def p_env_var_type(p):
        """env_var_type : NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_access_type(p):
        """access_type : DUMMY_NODE_VECTOR0
                       | DUMMY_NODE_VECTOR1
                       | DUMMY_NODE_VECTOR2
                       | DUMMY_NODE_VECTOR3"""
        p[0] = p[1]

    @staticmethod
    def p_access_node_list(p):
        """access_node_list : IDENT
                            | IDENT COMMA access_node_list"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_message_transmitters(p):
        """message_transmitters : message_transmitters_list"""
        if p[1] is not None:
            message_transmitters = p[1]
        else:
            message_transmitters = []
        p[0] = MessageTransmitters(message_transmitters)

    @staticmethod
    def p_message_transmitters_list(p):
        """message_transmitters_list : message_transmitter
                                     | message_transmitter message_transmitters_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_message_transmitter(p):
        """message_transmitter : BO_TX_BU_ NUMERIC COLON transmitter_list_optional SEMICOLON"""
        p[0] = MessageTransmitter(p[2], p[4])

    @staticmethod
    def p_transmitter_list(p):
        """transmitter_list : IDENT
                            | IDENT transmitter_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_transmitter_list_optional(p):
        """transmitter_list_optional : empty
                                     | transmitter_list"""
        p[0] = p[1]

    @staticmethod
    def p_multiplexed_signals(p):
        """multiplexed_signals : multiplexed_signals_list"""
        if p[1] is not None:
            multiplexed_signals = p[1]
        else:
            multiplexed_signals = []
        p[0] = MultiplexedSignals(multiplexed_signals)

    @staticmethod
    def p_multiplexed_signals_list(p):
        """multiplexed_signals_list : multiplexed_signal
                                    | multiplexed_signal multiplexed_signals_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_multiplexed_signal(p):
        """multiplexed_signal : SG_MUL_VAL_ message_id multiplexed_signal_name multiplexer_switch_name multiplexer_value_ranges SEMICOLON """
        p[0] = MultiplexedSignal(p[2], p[3], p[4], p[5])

    @staticmethod
    def p_multiplexed_signal_name(p):
        """multiplexed_signal_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_multiplexer_switch_name(p):
        """multiplexer_switch_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_multiplexer_value_ranges(p):
        """multiplexer_value_ranges : value_range
                                    | value_range COMMA multiplexer_value_ranges"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_value_range(p):
        """value_range : RANGE"""
        p[0] = p[1]

    @staticmethod
    def p_value_descriptions(p):
        """value_descriptions : value_descriptions_list"""
        if p[1] is not None:
            value_descriptions = p[1]
        else:
            value_descriptions = []
        p[0] = ValueDescriptions(value_descriptions)

    @staticmethod
    def p_value_descriptions_list(p):
        """value_descriptions_list : value_descriptions_for
                                   | value_descriptions_for value_descriptions_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_value_descriptions_for(p):
        """value_descriptions_for : value_descriptions_for_signal
                                  | value_descriptions_for_env_var"""
        p[0] = p[1]

    @staticmethod
    def p_value_descriptions_for_signal(p):
        """value_descriptions_for_signal : VAL_ message_id signal_name value_description_list SEMICOLON"""
        p[0] = ValueDescriptionForSignal(p[2], p[3], p[4])

    @staticmethod
    def p_value_descriptions_for_env_var(p):
        """value_descriptions_for_env_var : VAL_ env_var_aname value_description_list SEMICOLON"""
        p[0] = ValueDescriptionForEnvVar(p[2], p[3])

    @staticmethod
    def p_value_description(p):
        """value_description : NUMERIC STRING"""
        p[0] = ValueDescription(p[1], p[2])

    @staticmethod
    def p_value_description_list(p):
        """value_description_list : value_description
                                  | value_description value_description_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_attribute_values(p):
        """attribute_values : attribute_values_list"""
        if p[1] is not None:
            attribute_values = p[1]
        else:
            attribute_values = []
        p[0] = AttributeValues(attribute_values)

    @staticmethod
    def p_attribute_values_list(p):
        """attribute_values_list : attribute_value_for_object
                                 | attribute_value_for_object attribute_values_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_env_var_aname(p):
        """env_var_aname : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_attribute_value_for_object(p):
        """attribute_value_for_object : BA_ attribute_name attribute_value_ SEMICOLON"""
        p[0] = AttributeValueForObject(p[2], p[3])

    @staticmethod
    def p_attribute_value_(p):
        """attribute_value_ : attribute_value
                            | attribute_value_network_node
                            | attribute_value_message
                            | attribute_value_signal
                            | attribute_value_environment_variable"""
        p[0] = p[1]

    @staticmethod
    def p_attribute_value_network_node(p):
        """attribute_value_network_node : BU_ node_name attribute_value"""
        p[0] = AttributeValueNetworkNode(p[2], p[3])

    @staticmethod
    def p_attribute_value_message(p):
        """attribute_value_message : BO_ message_id attribute_value"""
        p[0] = AttributeValueMessage(p[2], p[3])

    @staticmethod
    def p_attribute_value_signal(p):
        """attribute_value_signal : SG_ message_id signal_name attribute_value"""
        p[0] = AttributeValueSignal(p[2], p[3], p[4])

    @staticmethod
    def p_attribute_value_environment_variable(p):
        """attribute_value_environment_variable : EV_ env_var_name attribute_value"""
        p[0] = AttributeValueEnvironmentVariable(p[2], p[3])

    @staticmethod
    def p_node_name(p):
        """node_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_message_id(p):
        """message_id : NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_signal_name(p):
        """signal_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_env_var_name(p):
        """env_var_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_attribute_defaults(p):
        """attribute_defaults : attribute_defaults_list"""
        p[0] = AttributeDefaults(p[1])

    @staticmethod
    def p_attribute_defaults_list(p):
        """attribute_defaults_list : attribute_default
                                   | attribute_default attribute_defaults_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_attribute_default(p):
        """attribute_default : BA_DEF_DEF_ attribute_name attribute_value SEMICOLON"""
        p[0] = AttributeDefault(p[2], p[3])

    @staticmethod
    def p_attribute_value(p):
        """attribute_value : NUMERIC
                           | STRING"""
        p[0] = AttributeValue(p[1])

    @staticmethod
    def p_attribute_definitions(p):
        """attribute_definitions : attribute_definitions_list"""
        p[0] = AttributeDefinitions(p[1])

    @staticmethod
    def p_attribute_definitions_list(p):
        """attribute_definitions_list : attribute_definition
                                      | attribute_definition attribute_definitions_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_attribute_definition(p):
        """attribute_definition : BA_DEF_ object_type attribute_name attribute_value_type SEMICOLON"""
        p[0] = AttributeDefinition(p[2], p[3], p[4])

    @staticmethod
    def p_opbject_type(p):
        """object_type : empty
                       | BU_
                       | BO_
                       | SG_
                       | EV_"""
        p[0] = p[1]

    @staticmethod
    def p_attribute_value_type(p):
        """attribute_value_type : attribute_value_type_int
                                | attribute_value_type_hex
                                | attribute_value_type_float
                                | attribute_value_type_string
                                | attribute_value_type_enum"""
        p[0] = p[1]

    @staticmethod
    def p_attribute_value_type_int(p):
        """attribute_value_type_int : INT NUMERIC NUMERIC"""
        p[0] = AttributeValueTypeInt(p[2], p[3])

    @staticmethod
    def p_attribute_value_type_hex(p):
        """attribute_value_type_hex : HEX NUMERIC NUMERIC"""
        p[0] = AttributeValueTypeHex(p[2], p[3])

    @staticmethod
    def p_attribute_value_type_float(p):
        """attribute_value_type_float : FLOAT NUMERIC NUMERIC"""
        p[0] = AttributeValueTypeFloat(p[2], p[3])

    @staticmethod
    def p_attribute_value_type_string(p):
        """attribute_value_type_string : STRING"""
        p[0] = AttributeValueTypeString()

    @staticmethod
    def p_attribute_value_type_enum(p):
        """attribute_value_type_enum : ENUM comma_separated_char_string_list"""
        p[0] = AttributeValueTypeEnum(p[2])

    @staticmethod
    def p_comma_separated_char_string_list(p):
        """comma_separated_char_string_list : STRING
                                            | STRING COMMA comma_separated_char_string_list"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_attribute_name(p):
        """attribute_name : STRING"""
        # TODO : check the format here according to section 12.1...
        p[0] = p[1]

    @staticmethod
    def p_comments(p):
        """comments : comment_list"""
        if p[1] is not None:
            comments = p[1]
        else:
            comments = []
        p[0] = Comments(comments)

    @staticmethod
    def p_comment(p):
        """comment : CM_ comment_definition SEMICOLON"""
        p[0] = p[2]

    @staticmethod
    def p_comment_definition(p):
        """comment_definition : char_string
                              | comment_network_node
                              | comment_message
                              | comment_signal
                              | comment_environment_variable"""
        p[0] = p[1]

    @staticmethod
    def p_char_string(p):
        """char_string : STRING"""
        p[0] = p[1]

    @staticmethod
    def p_comment_network_node(p):
        """comment_network_node : BU_ node_name char_string"""
        p[0] = CommentNetworkNode(p[2], p[3])

    @staticmethod
    def p_comment_message(p):
        """comment_message : BO_ message_id char_string"""
        p[0] = CommentMessage(p[2], p[3])

    @staticmethod
    def p_comment_signal(p):
        """comment_signal : SG_ message_id signal_name char_string"""
        p[0] = CommentSignal(p[2], p[3], p[4])

    @staticmethod
    def p_comment_environment_variable(p):
        """comment_environment_variable : EV_ env_var_name char_string"""
        p[0] = CommentEnvironmentVariable()

    @staticmethod
    def p_comment_list(p):
        """comment_list : comment
                        | comment comment_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_messages(p):
        """messages : message_list"""
        if p[1] is not None:
            messages = p[1]
        else:
            messages = []
        p[0] = Messages(messages)

    @staticmethod
    def p_message(p):
        """message : BO_ message_id message_name COLON message_size transmitter signal_list_optional"""
        p[0] = Message(p[2], p[3], p[5], p[6], p[7])

    @staticmethod
    def p_message_size(p):
        """message_size : NUMERIC"""
        p[0] = p[1]

    @staticmethod
    def p_transmitter(p):
        """transmitter : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_message_list(p):
        """message_list : message
                        | message message_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_message_name(p):
        """message_name : IDENT"""
        p[0] = p[1]

    @staticmethod
    def p_signal(p):
        """signal : SG_ IDENT multiplexer_indicator COLON NUMERIC VERTICAL_BAR NUMERIC AROBASE NUMERIC value_type PARENTHESE_OPEN NUMERIC COMMA NUMERIC PARENTHESE_CLOSE BRACE_OPEN NUMERIC VERTICAL_BAR NUMERIC BRACE_CLOSE STRING receiver_list"""
        p[0] = Signal(p[2], p[3], p[5], p[7], p[9], p[10], p[12], p[14], p[17], p[19], p[21], p[22])

    @staticmethod
    def p_receiver_list(p):
        """receiver_list : IDENT
                         | IDENT COMMA receiver_list"""
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_signal_list(p):
        """signal_list : signal
                       | signal signal_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_signal_list_optional(p):
        """signal_list_optional : empty
                                | signal_list"""
        p[0] = p[1]

    @staticmethod
    def p_value_type(p):
        """value_type : PLUS
                      | MINUS"""
        p[0] = p[1]

    @staticmethod
    def p_multiplexer_indicator(p):
        """multiplexer_indicator : empty
                                 | IDENT"""
        # TODO: handle format specified at page 5...
        p[0] = p[1]

    @staticmethod
    def p_value_tables(p):
        """value_tables : value_table_list"""
        if p[1] is not None:
            value_tables = p[1]
        else:
            value_tables = []
        p[0] = ValueTables(value_tables)

    @staticmethod
    def p_value_table_list(p):
        """value_table_list : value_table
                            | value_table value_table_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_value_table(p):
        """value_table : VAL_TABLE_ IDENT value_table_description_list_optional SEMICOLON"""
        p[0] = ValTable(p[2], p[3])

    @staticmethod
    def p_value_table_description(p):
        """value_table_description : NUMERIC STRING"""
        p[0] = ValueTableDescription(p[1], p[2])

    @staticmethod
    def p_value_table_description_list(p):
        """value_table_description_list : value_table_description
                                        | value_table_description value_table_description_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_value_table_description_list_optional(p):
        """value_table_description_list_optional : empty
                                                 | value_table_description_list"""
        p[0] = p[1]

    @staticmethod
    def p_version(p):
        """version : VERSION STRING"""
        p[0] = Version(p[2])

    @staticmethod
    def p_new_symbols(p):
        """new_symbols : NS_ COLON new_symbols_list_optional"""
        try:
            p[0] = p[3]
        except IndexError:
            p[0] = None

    @staticmethod
    def p_new_symbols_value(p):
        """
        new_symbols_value : CM_
                          | BA_DEF_
                          | BA_
                          | VAL_
                          | CAT_DEF_
                          | CAT_
                          | FILTER_
                          | BA_DEF_DEF_
                          | EV_DATA_
                          | ENVVAR_DATA_
                          | SGTYPE_
                          | SGTYPE_VAL_
                          | BA_DEF_SGTYPE_
                          | BA_SGTYPE_
                          | SIG_TYPE_REF_
                          | VAL_TABLE_
                          | SIG_GROUP_
                          | SIG_VALTYPE_
                          | SIGTYPE_VALTYPE_
                          | BO_TX_BU_
                          | BA_DEF_REL_
                          | BA_REL_
                          | BA_DEF_DEF_REL_
                          | BU_SG_REL_
                          | BU_EV_REL_
                          | BU_BO_REL_
                          | NS_DESC_
                          | FILTER
                          | SG_MUL_VAL_
        """
        p[0] = p[1]

    @staticmethod
    def p_new_symbols_list(p):
        """new_symbols_list : new_symbols_value
                            | new_symbols_value new_symbols_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_new_symbols_list_optional(p):
        """
        new_symbols_list_optional : empty
                                 | new_symbols_list
        """
        p[0] = p[1]

    @staticmethod
    def p_bit_timing(p):
        """bit_timing : BS_ COLON bit_timing_optional"""
        p[0] = p[3]

    @staticmethod
    def p_bit_timing_optional(p):
        """bit_timing_optional : empty
                               | NUMERIC COLON NUMERIC COMMA NUMERIC"""
        try:
            p[0] = BitTiming(p[1], p[3], p[5])
        except IndexError:
            p[0] = None

    @staticmethod
    def p_nodes(p):
        """nodes : BU_ COLON nodes_list_optional"""
        p[0] = Nodes(p[3])

    @staticmethod
    def p_nodes_list(p):
        """nodes_list : IDENT
                      | IDENT nodes_list"""
        try:
            p[0] = [p[1]] + p[2]
        except IndexError:
            p[0] = [p[1]]

    @staticmethod
    def p_nodes_list_optional(p):
        """nodes_list_optional : empty
                               | nodes_list"""
        p[0] = p[1]

    @staticmethod
    def p_empty(p):
        """empty :"""
        p[0] = None
