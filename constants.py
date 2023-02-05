class Constants:
    DIGITS = '0123456789'
    NUM_CHARS = DIGITS + '.'
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ALPHANUM = ALPHA + NUM_CHARS
    VALID_IDN = ALPHA + DIGITS + '_'

    NUMPOINT = '.'

    STRING_QUOTES = "'"

    KW_INT = 'int'
    KW_FLT = 'flt'
    KW_BOL = 'bol'
    KW_STR = 'str'
    KW_CIF = 'if'
    KW_CEL = 'else'
    KW_CWH = 'while'
    KW_CFR = 'for'
    KW_VAR = 'var'
    KW_DEF = 'def'
    KW_AND = 'and'
    KW_OR = 'or'
    KW_NOT = 'not'
    KW_EQU = 'eq'
    KW_NEQ = 'neq'
    KW_GTE = 'gte',
    KW_LTE = 'lte'

    COMPARISONS = [KW_AND, KW_OR, KW_NOT, KW_EQU, KW_NEQ, KW_LTE, KW_GTE]

    KEYWORDS = [KW_CIF, KW_CWH, KW_CFR, KW_VAR, KW_DEF]

    KW_DATA_TYPES = [KW_INT, KW_FLT, KW_BOL, KW_STR]

    TYPE_FLT = 'FLT'
    TYPE_INT = 'INT'
    TYPE_MUL = 'MUL'
    TYPE_DIV = 'DIV'
    TYPE_ADD = 'ADD'
    TYPE_SUB = 'SUB'
    TYPE_LPA = 'LPA'
    TYPE_RPA = 'RPA'
    TYPE_EOF = 'EOF'

    TYPE_INC = 'INC'
    
    TYPE_KYW = 'KYW'
    TYPE_IDN = 'IDN'

    TYPE_SMC = 'SMC'
    TYPE_EQU = 'EQU'

    TYPE_STR = 'STR'

    OPERATORS = {
        '+': TYPE_ADD,
        '-': TYPE_SUB,
        '*': TYPE_MUL,
        '/': TYPE_DIV
    }

    TYPE_SYMBOLS = {
        ';': 'SMC',
        '=': 'EQU',
        '(': 'LPA',
        ')': 'RPA',
        '[': 'LSB',
        ']': 'RSB',
        '{': 'LCB',
        '}': 'RCB',
        'eq': 'EQU',
        'lt': 'CLT',
        'gt': 'CGT',
        'gte': 'GTE',
        'lte': 'LTE',
        'neq': 'NEQ',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT'
    }

    TYPE_SYMBOLS.update(OPERATORS)