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

    # Reserved Words - Channel
    RW_SEND = 32
    RW_RECEIVE = 33

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
    DL_LBRACE = 22    # {
    DL_RPAREN = 23    # }
    DL_COMMA = 24     # ,
    DL_DOT = 25       # .
    DL_LBRACKET = 26  # [
    DL_RBRACKET = 27  # ]
    DL_COMMENT = 28   # #
    
    # Identifiers and Literals
    ID = 28
    NUM = 29  
    STRING_LITERAL = 30

    # Errors
    ER_CHANNEL = 34
    
    # End of File
    EOF = 31
