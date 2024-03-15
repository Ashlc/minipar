import traceback
from dictionary import WordDict
from enum_tokens import TokenEnums
from tk import *

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def parse_id_or_keyword(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha():
                identifier = self.parse_id_or_keyword()
                if identifier.upper() in TokenEnums.__members__:
                    token_type = TokenEnums[identifier.upper()]
                    return token_type, identifier
                else:
                    return TokenEnums.ID, identifier

            if self.current_char.isdigit():
                num_str = ''
                while self.current_char is not None and self.current_char.isdigit():
                    num_str += self.current_char
                    self.advance()
                return TokenEnums.NUM, int(num_str)

            # Handle single character tokens
            char = self.current_char
            self.advance()
            if char == '=':
                return TokenEnums.OP_ASSIGN, char
            elif char == '+':
                return TokenEnums.OP_PLUS, char
            elif char == '-':
                return TokenEnums.OP_MINUS, char
            elif char == '*':
                return TokenEnums.OP_MULTIPLY, char
            elif char == '/':
                return TokenEnums.OP_DIVIDE, char
            elif char == '(':
                return TokenEnums.DL_LPAREN, char
            elif char == ')':
                return TokenEnums.DL_RPAREN, char
            elif char == ';':
                return TokenEnums.DL_SEMICOLON, char
            elif char == '{':
                return TokenEnums.DL_LBRACE, char
            elif char == '}':
                return TokenEnums.DL_RBRACE, char
            elif char == ',':
                return TokenEnums.DL_COMMA, char
            elif char == '.':
                return TokenEnums.DL_DOT, char
            elif char == '[':
                return TokenEnums.DL_LBRACKET, char
            elif char == ']':
                return TokenEnums.DL_RBRACKET, char
            elif char == '#':
                # Comment handling - ignore characters until end of line
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

            # Handle string literals
            if char == '"':
                string_value = ''
                self.advance()
                while self.current_char is not None and self.current_char != '"':
                    string_value += self.current_char
                    self.advance()
                self.advance()  # Skip closing double quote
                return TokenEnums.STRING_LITERAL, string_value

        return TokenEnums.EOF, None

# Test the lexer
lexer = Lexer("""
int a = 10;
if (a > 5) {
  print("Hello");
} else {
  print("World");
}
""")
while True:
    token_type, value = lexer.get_next_token()
    if token_type == TokenEnums.EOF:
        break
    print(f"Token Type: {token_type.name}, Value: {value}")