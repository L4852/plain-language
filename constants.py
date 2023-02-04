class Constants:
    DIGITS = '0123456789'
    NUM_CHARS = DIGITS + '.'
    ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    ALPHANUM = ALPHA + NUM_CHARS
    VALID_IDN = ALPHA + DIGITS + '_'

    NUMPOINT = '.'

    TYPE_FLT = 'FLT'
    TYPE_INT = 'INT'
    TYPE_MUL = 'MUL'
    TYPE_DIV = 'DIV'
    TYPE_ADD = 'ADD'
    TYPE_SUB = 'SUB'
    TYPE_LPA = 'LPA'
    TYPE_RPA = 'RPA'
    TYPE_EOF = 'EOF'
    
    TYPE_KYW = 'KYW'
    TYPE_IDN = 'IDN'

    OPERATORS = {
        '+': TYPE_ADD,
        '-': TYPE_SUB,
        '*': TYPE_MUL,
        '/': TYPE_DIV
    }

    TYPE_SYMBOLS = {
        ';': 'SMC',
        '(': 'LPA',
        ')': 'RPA',
        '[': 'LSB',
        ']': 'RSB',
        '{': 'LCB',
        '}': 'RCB'
    }

    TYPE_SYMBOLS.update(OPERATORS)