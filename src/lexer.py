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
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Check if the word is a keyword/protected word
        if result.lower() in WordDict.words:
            return WordDict.words[result.lower()], result
        else:
            return TokenEnums.ID, result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self.parse_id_or_keyword()

            if self.current_char.isdigit():
                num_str = ''
                while self.current_char is not None and self.current_char.isdigit():
                    num_str += self.current_char
                    self.advance()
                return TokenEnums.NUM, int(num_str)
            
            char = self.current_char
            
            # Handle string literals
            if char == '"':
                string_value = ''
                self.advance()
                while self.current_char is not None and self.current_char != '"':
                    string_value += self.current_char
                    self.advance()
                self.advance()  # Skip closing double quote
                return TokenEnums.STRING_LITERAL, string_value

            self.advance()
            
            # Comment handling - ignore characters until end of line
            if char in WordDict.symbols:
                return WordDict.symbols[char], char
            
            elif char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                continue

        return TokenEnums.EOF, None

# Test the lexer
lexer = Lexer("""
int a = 10; #Comment
if (a > 5) {
  print("Hello");
  par {
    a += 5;
    print("World");
  }
} else {
  seq {
    print("World");
    print("!");
  }
}
""")
while True:
    token_type, value = lexer.get_next_token()
    if token_type == TokenEnums.EOF:
        break
    print(f"Token Type: {token_type.name}, Value: {value}")