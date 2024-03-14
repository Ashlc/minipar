from enum import Enum

class TokenEnums(Enum):
    # Reserved Words - Types
    RW_INT = 1
    RW_BOOL = 2
    RW_STRING = 3
    RW_C_CHANNEL = 4
    RW_TRUE = 5
    RW_FALSE = 6
    RW_NULL = 7

    # Reserved Words - Control Flow
    RW_SEQ = 8
    RW_PAR = 9
    RW_IF = 10
    RW_ELSE = 11
    RW_WHILE = 12
    RW_CHAN = 13
    
    # Operators and Delimiters
    OP_ASSIGN = 14  # =
    OP_PLUS = 15    # +
    OP_MINUS = 16   # -
    OP_MULTIPLY = 17  # *
    OP_DIVIDE = 18    # /
    DL_LPAREN = 19    # (
    DL_RPAREN = 20    # )
    DL_SEMICOLON = 21 # ;
    
    # Identifiers and Literals
    ID = 22
    NUM = 23  
    STRING_LITERAL = 24
    
    # End of File
    EOF = 25
