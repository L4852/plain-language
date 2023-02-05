class Constants:
    DIGITS = '0123456789'
    NUM_CHARS = DIGITS + '.'
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ALPHANUM = ALPHA + NUM_CHARS
    VALID_IDN = ALPHA + DIGITS + '_'

    NUMPOINT = '.'

    KW_INT = 'int'
    KW_FLT = 'flt'
    KW_BOL = 'bol'
    KW_STR = 'str'
    KW_CIF = 'if'
    KW_CEL = 'else'
    KW_CWH = 'while'
    KW_CFR = 'for'
    KW_VAR = 'var'

    KEYWORDS = [KW_CIF, KW_CWH, KW_CFR, KW_VAR]

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
        '}': 'RCB'
    }

    TYPE_SYMBOLS.update(OPERATORS)