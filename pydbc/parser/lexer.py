import os

import ply.lex as lex

keywords = {r'VERSION',
            r'NS_DESC_',  # not in specification
            r'FILTER_',  # not in specification
            r'SG_MUL_VAL_',  # not in specification
            r'FILTER',  # obsolete
            r'CM_',
            r'BA_DEF_',
            r'BA_',
            'BS_',
            r'VAL_',
            r'CAT_DEF_',
            r'CAT_',
            r'FILTER',
            r'BA_DEF_DEF_',
            r'EV_DATA_',
            r'ENVVAR_DATA_',
            r'SGTYPE_',
            r'SGTYPE_VAL_',
            r'BA_DEF_SGTYPE_',
            r'BA_SGTYPE_',
            r'SIG_TYPE_REF_',
            r'VAL_TABLE_',
            r'SIG_GROUP_',
            r'SIG_VALTYPE_',
            r'SIGTYPE_VALTYPE_',
            r'BO_TX_BU_',
            r'BA_DEF_REL_',
            r'BA_REL_',
            r'BA_DEF_DEF_REL_',
            r'BU_SG_REL_',
            r'BU_EV_REL_',
            r'BU_BO_REL_',
            r'BU_',
            r'NS_',
            r'BO_',
            r'SG_',
            r'EV_',
            r'AROBASE',
            r'VERTICAL_BAR',
            r'PARENTHESE_OPEN',
            r'PARENTHESE_CLOSE',
            r'BRACE_OPEN',
            r'BRACE_CLOSE',
            r'SEMICOLON',
            r'COMMA',
            r'COLON',
            r'STRING',
            r'NUMERIC',
            r'RANGE',
            r'IDENT',
            r'PLUS',
            r'MINUS',
            r'INT',
            r'HEX',
            r'FLOAT',
            r'ENUM'}

_keywords = dict((k, k) for k in keywords)

tokens = tuple(keywords)

t_ignore = ' \t\r\n'

t_PARENTHESE_OPEN = r'\('
t_PARENTHESE_CLOSE = r'\)'
t_BRACE_OPEN = r'\['
t_BRACE_CLOSE = r'\]'
t_SEMICOLON = r';'
t_COMMA = r','
t_COLON = r':'
t_VERTICAL_BAR = r'\|'
t_AROBASE = r'@'
t_PLUS = r'\+'
t_MINUS = r'-'


@lex.TOKEN(r'"(?:[^"\\]|\\.)*"')
def t_STRING(token):
    token.value = token.value[1:-1]
    return token


@lex.TOKEN(r'[0-9]+-[0-9]+')
def t_RANGE(token):
    token.value = tuple(int(n) for n in token.value.split('-'))
    return token


@lex.TOKEN(r'[+-]?(([0]{1}[Xx]{1}[A-Fa-f0-9]+)|(\d+(\.(\d*([eE][+-]?\d+)?)?|([eE][+-]?\d+)?)?))')
def t_NUMERIC(token):
    try:
        token.value = int(token.value, 10)
    except ValueError:
        try:
            token.value = int(token.value, 16)
        except ValueError:
            token.value = float(token.value)
    return token


@lex.TOKEN(r'[A-Za-z_][A-Za-z0-9_]*')
def t_IDENT(token):
    try:
        token.type = _keywords[token.value]
    except KeyError:
        pass
    return token


def t_error(token):
    print('invalid character at line ' + str(token.lineno) + ', position ' + str(token.lexpos))
    token.lexer.skip(1)


lexer = lex.lex(optimize=False, outputdir=os.path.dirname(os.path.realpath(__file__)), lextab='lextab')
