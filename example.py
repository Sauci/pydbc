from pydbc.parser import DbcParser

dbc_data = """
VERSION "my_version"

NS_ :
  BU_EV_REL_
  BU_BO_REL_

BO_ 1234 my_message_name: 2 my_transmitter
  SG_ my_first_signal_name : 56|8@1+ (16,0) [0|4000] "my_first_signal_unit" my_first_signal_transmitter
  SG_ my_second_signal_name : 48|8@1+ (1,0) [0|250] "my_second_signal_unit" my_first_signal_transmitter
"""

if __name__ == '__main__':
    p = DbcParser(dbc_data)
    assert p.ast.version == 'my_version'
    assert p.ast.messages[0].identifier == 1234
    first_signal = p.ast.messages[0].signals[0]
    assert first_signal.name == 'my_first_signal_name'
    assert first_signal.signal_size == 8
    assert first_signal.start_bit == 56
    assert first_signal.value_type == '+'
    assert first_signal.factor == 16
    assert first_signal.offset == 0
    assert first_signal.minimum == 0
    assert first_signal.maximum == 4000
