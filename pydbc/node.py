import itertools


class AstNode(object):
    pass


class AStNodeList(list):
    pass


class AttributeDefault(AstNode):
    def __init__(self, attribute_name, attribute_value):
        self.attribute_name = attribute_name
        self.attribute_value = attribute_value


class AttributeDefaults(AStNodeList):
    def __init__(self, attribute_defaults):
        self.attribute_defaults = attribute_defaults


class AttributeDefinition(AstNode):
    def __init__(self, object_type, attribute_name, attribute_value_type):
        self.object_type = object_type
        self.attribute_name = attribute_name
        self.attribute_value_type = attribute_value_type


class AttributeDefinitions(AStNodeList):
    def __init__(self, attribute_definitions):
        self.attribute_definitions = attribute_definitions


class AttributeValue(AstNode):
    def __init__(self, value):
        self.value = value


class AttributeValues(AStNodeList):
    def __init__(self, attribute_values):
        self.attribute_values = attribute_values


class AttributeValueEnvironmentVariable(AstNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AttributeValueForObject(AstNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AttributeValueMessage(AstNode):
    def __init__(self, message_id, value):
        self.message_id = message_id
        self.value = value


class AttributeValueNetworkNode(AstNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class AttributeValueSignal(AstNode):
    def __init__(self, message_id, signal_name, value):
        self.message_id = message_id
        self.signal_name = signal_name
        self.value = value


class AttributeValueTypeEnum(AstNode):
    def __init__(self, e):
        self.e = e


class AttributeValueTypeFloat(AstNode):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class AttributeValueTypeHex(AstNode):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class AttributeValueTypeInt(AstNode):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class AttributeValueTypeString(AstNode):
    def __init__(self):
        pass


class Comment(AstNode):
    def __init__(self, value):
        self.value = value


class Comments(AStNodeList):
    def __init__(self, comments):
        self.comments = comments


class CommentEnvironmentVariable(AstNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class CommentMessage(AstNode):
    def __init__(self, message_id, value):
        self.message_id = message_id
        self.value = value


class CommentNetworkNode(AstNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class CommentSignal(AstNode):
    def __init__(self, message_id, signal_name, value):
        self.message_id = message_id
        self.signal_name = signal_name
        self.value = value


class BitTiming(AstNode):
    def __init__(self, baud_rate, btr0, btr1):
        super(BitTiming, self).__init__()
        self.baud_rate = baud_rate
        self.btr0 = btr0
        self.btr1 = btr1


class DbcFile(AstNode):
    def __init__(self,
                 version=None,
                 new_symbols=None,
                 bit_timing=None,
                 nodes=None,
                 value_tables=None,
                 messages=None,
                 message_transmitters=None,
                 environment_variables=None,
                 environment_variables_data=None,
                 signal_types=None,
                 comments=None,
                 attribute_definitions=None,
                 sigtype_attr_list=None,
                 attribute_defaults=None,
                 attribute_values=None,
                 value_descriptions=None,
                 category_definitions=None,
                 categories=None,
                 filter=None,
                 signal_type_refs=None,
                 signal_groups=None,
                 signal_extended_value_type_list=None,
                 multiplexed_signals=None):
        self.version = version
        self.new_symbols = new_symbols
        self.bit_timing = bit_timing
        self.nodes = nodes
        self.value_tables = value_tables
        self.messages = messages
        self.message_transmitters = message_transmitters
        self.environment_variables = environment_variables
        self.environment_variables_data = environment_variables_data
        self.signal_types = signal_types
        self.comments = comments
        self.attribute_definitions = attribute_definitions
        self.sigtype_attr_list = sigtype_attr_list
        self.attribute_defaults = attribute_defaults
        self.attribute_values = attribute_values
        self.value_descriptions = value_descriptions
        self.category_definitions = category_definitions
        self.categories = categories
        self.filter = filter
        self.signal_type_refs = signal_type_refs
        self.signal_groups = signal_groups
        self.signal_extended_value_type_list = signal_extended_value_type_list


class Message(AstNode):
    def __init__(self, identifier, name, size, transmitter, signals):
        if signals is None:
            signals = list()
        self.identifier = identifier
        self.name = name
        self.size = size
        self.transmitter = transmitter
        self.signals = signals


class Messages(AStNodeList):
    def get_by_name(self, name):
        for e in self:
            if e.name == name:
                return e
        raise KeyError


class MultiplexedSignal(AstNode):
    def __init__(self, message_id, signal_name, multiplexer_switch_name, ranges):
        self.message_id = message_id
        self.signal_name = signal_name
        self.multiplexer_switch_name = multiplexer_switch_name
        self.ranges = ranges


class MultiplexedSignals(AStNodeList):
    pass


class Nodes(AStNodeList):
    def __init__(self, nodes):
        self.nodes = nodes


class Signal(AstNode):
    def __init__(self, name, multiplexer_indicator, start_bit, signal_size, byte_order, value_type, factor, offset,
                 minimum, maximum, unit, receiver):
        self.name = name
        self.multiplexer_indicator = multiplexer_indicator
        self.start_bit = start_bit
        self.signal_size = signal_size
        self.byte_order = byte_order
        self.value_type = value_type
        self.factor = factor
        self.offset = offset
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self.receiver = receiver


class ValTable(AstNode):
    def __init__(self, name, value_descriptions):
        self.name = name
        self.value_description = value_descriptions


class ValueDescription(AstNode):
    def __init__(self, a, b):
        self.a = a
        self.b = b


class ValueDescriptionForEnvVar(AstNode):
    def __init__(self, a_name, value_description):
        self.a_name = a_name
        self.value_description = value_description


class ValueDescriptionForSignal(AstNode):
    def __init__(self, message_id, signal_name, value_description):
        self.message_id = message_id
        self.signal_name = signal_name
        self.value_description = value_description


class ValueDescriptions(AStNodeList):
    def __init__(self, value_descriptions):
        self.value_descriptions = value_descriptions


class ValueTables(AStNodeList):
    def __init__(self, value_tables):
        self.value_tables = value_tables


class ValueTableDescription(AstNode):
    def __init__(self, value, name):
        self.value = value
        self.name = name


class Version(str):
    pass
