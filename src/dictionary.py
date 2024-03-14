from enum_tokens import TokenEnums as en

# Dictionary of reserved words

class WordDict:
    words = {
    "seq": en.RW_SEQ,
    "par": en.RW_PAR,
    "if": en.RW_IF,
    "else": en.RW_ELSE,
    "while": en.RW_WHILE,
    "chan": en.RW_CHAN,
    "int": en.RW_INT,
    "bool": en.RW_BOOL,
    "string": en.RW_STRING,
    "c_channel": en.RW_C_CHANNEL,
    "true": en.RW_TRUE,
    "false": en.RW_FALSE,
    "null": en.RW_NULL,  
    "send": en.RW_SEND,
    "receive": en.RW_RECEIVE
    }
    