import traceback
from dictionary import WordDict
from enum_tokens import TokenEnums
from tk import *

# Codigo do monitor

class Lexer:

    def __init__(self, file):
        try:
            self.txtline = " "
            self.pos = 1
            self.row = 1
            self.col = 1
            self.reader = open(file, 'rb')
            self.new_line()

            self.content = list(self.txtline)
            self.state = None

        except IOError as e:
            traceback.print_exc()

    @staticmethod
    def is_digit(string):
        return string.isdigit()

    @staticmethod
    def is_operator(string):

        return string in ['>', '<', '=', '!']

    @staticmethod
    def is_lower(string):
        return string.islower()

    @staticmethod
    def is_upper(string):
        return string.isupper()

    @staticmethod
    def is_blank(string):
        return string.isspace()

    @staticmethod
    def is_letter(string):
        return string.isalpha()

    @staticmethod
    def is_alphanum(string):
        return string.isalpha() or string.isdigit()

    def is_EOF(self):
        return self.pos == len(self.content)

    def next_char(self):
        self.pos += 1
        return self.content[self.pos - 1]

    def next_token(self):
        self.state = 0
        lexem = ""

        while True:
            if self.is_EOF():
                if self.new_line():
                    self.content = list(self.txtline)
                else:
                    return Token(TokenEnums.EOF, "EOF", self.row, self.col)

            currChar = self.next_char()

            if self.state == 0:

                if self.is_blank(currChar):
                    self.state = 0

                # FOR SEQ
                elif currChar == 's':
                    # Peek ahead to check if it's followed by "eq"
                    if self.peek() == 'e' and self.peek(2) == 'q':
                        lexem += currChar
                        lexem += self.next_char()  # 'e'
                        lexem += self.next_char()  # 'q'
                        self.col += 2  # Increment column for 's', 'e', 'q'
                        return Token(TokenEnums.RW_SEQ, lexem, self.row, self.col)
                    else:
                        lexem += currChar                        
                        self.state = 1
                # FOR PAR
                elif currChar == 'p':
                    # Peek ahead to check if it's followed by "ar"
                    if self.peek() == 'a' and self.peek(2) == 'r':
                        lexem += currChar
                        lexem += self.next_char()  # 'a'
                        lexem += self.next_char()  # 'r'
                        self.col += 2  # Increment column for 'p', 'a', 'r'
                        return Token(TokenEnums.RW_PAR, lexem, self.row, self.col)
                    else:
                        lexem += currChar
                        self.state = 1
                # FOR CONNECTION (c_channel -> variável)
                # n entendi como faz. mas ele tem q ter duas funções base (send e recieve)
                elif currChar == 'c':
                    # Check for 'channel' keyword
                    if self.peek(6) == '_channel':
                        lexem += currChar
                        for _ in range(6):
                            lexem += self.next_char()
                        self.col += 7
                        self.state = 14
                        #return Token(TokenEnums.RW_CHAN, lexem, self.row, self.col)
                    else:
                        lexem += currChar
                        self.state = 1

                elif self.is_lower(currChar):
                    lexem += currChar
                    self.state = 1

                elif self.is_digit(currChar):
                    lexem += currChar
                    self.state = 3

                elif self.is_operator(currChar):
                    lexem += currChar
                    self.state = 7

                elif currChar == '\'':
                    lexem += currChar
                    self.state = 8

                elif self.is_upper(currChar):
                    lexem += currChar
                    self.state = 11

                elif currChar == '#':
                    self.state = 13

                elif currChar == '+':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_SUM, lexem, self.row, self.col)

                elif currChar == '-':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_SUB, lexem, self.row, self.col)

                elif currChar == '*':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_MUL, lexem, self.row, self.col)

                elif currChar == '/':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_DIV, lexem, self.row, self.col)

                elif currChar == '%':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_MOD, lexem, self.row, self.col)

                elif currChar == '(':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_OPENP, lexem, self.row, self.col)

                elif currChar == ')':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_CLOSEP, lexem, self.row, self.col)

                elif currChar == '[':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_OPENBRA, lexem, self.row, self.col)

                elif currChar == ']':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_ENDBRA, lexem, self.row, self.col)

                elif currChar == ';':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_SEMI, lexem, self.row, self.col)

                elif currChar == ',':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.DEL_COMMA, lexem, self.row, self.col)

                elif currChar == '~':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_NOTUN, lexem, self.row, self.col)

                elif currChar == '&':
                    lexem += currChar
                    self.col += 1
                    return Token(TokenEnums.OP_CONCAT, lexem, self.row, self.col)

                else:
                    return Token(TokenEnums.ER_UNK, lexem, self.row, self.col)

            elif self.state == 1:
                if self.is_operator(currChar) or self.is_blank(currChar) or not self.is_alphanum(currChar):
                    self.back()
                    self.state = 2

                elif self.is_digit(currChar) or self.is_lower(currChar) or self.is_upper(currChar):
                    lexem += currChar

                else:
                    self.col += 1
                    return Token(TokenEnums.ER_ID, lexem, self.row, self.col)

            elif self.state == 2:
                self.back()
                self.col += 1
                return Token(TokenEnums.ID, lexem, self.row, self.col)

            elif self.state == 3:
                if currChar == '.':
                    lexem += currChar
                    self.state = 4
                    self.col = +1
                elif not self.is_alphanum(currChar):
                    self.back()
                    self.state = 5
                elif self.is_digit(currChar):
                    lexem += currChar
                else:
                    self.col += 1
                    return Token(TokenEnums.ER_NUM, lexem, self.row, self.col)

            elif self.state == 4:
                if self.is_digit(currChar):
                    lexem += currChar

                elif self.is_operator(currChar) or self.is_blank(currChar) or not self.is_alphanum(currChar):
                    self.back()
                    self.state = 6

                else:
                    self.col += 1
                    return Token(TokenEnums.ER_NUM, lexem, self.row, self.col)

            elif self.state == 5:
                self.back()
                self.col += 1
                return Token(TokenEnums.CTE_INT, lexem, self.row, self.col)

            elif self.state == 6:
                self.back()
                self.col += 1
                return Token(TokenEnums.CTE_FLOAT, lexem, self.row, self.col)

            elif self.state == 7:
                self.back()
                self.back()
                currChar = self.next_char()

                if currChar == '>':
                    currChar = self.next_char()
                    self.col += 1

                    if currChar == '=':
                        lexem += currChar
                        return Token(TokenEnums.OP_EQUALG, lexem, self.row, self.col)
                    else:
                        self.back()
                        return Token(TokenEnums.OP_GREATER, lexem, self.row, self.col)

                elif currChar == '<':

                    currChar = self.next_char()
                    self.col += 1

                    if currChar == '=':
                        lexem += currChar
                        return Token(TokenEnums.OP_EQUALL, lexem, self.row, self.col)
                    else:
                        self.back()
                        return Token(TokenEnums.OP_LESS, lexem, self.row, self.col)

                elif currChar == '!' or currChar == '=':
                    currChar = self.next_char()
                    self.col += 1

                    if currChar == '=':
                        lexem += currChar
                        return Token(TokenEnums.OP_EQUALDIFF, lexem, self.row, self.col)
                    elif not (currChar == '!' or currChar == '='):
                        return Token(TokenEnums.OP_ATR, lexem, self.row, self.col)
                    else:
                        self.back()
                        return Token(TokenEnums.OP_NOT, lexem, self.row, self.col)

                else:
                    return Token(TokenEnums.ER_UNK, lexem, self.row, self.col)

            elif self.state == 8:
                if chr(32) <= currChar <= chr(126):
                    lexem += currChar
                    currChar = self.next_char()

                    if currChar == '\'':
                        lexem += currChar
                        self.state = 9

                    else:
                        self.back()
                        self.state = 10

                else:
                    self.col += 1
                    return Token(TokenEnums.ER_CHAR, lexem, self.row, self.col)

            elif self.state == 9:
                self.back()
                self.col += 1
                return Token(TokenEnums.CTE_CHAR, lexem, self.row, self.col)

            elif self.state == 10:
                if chr(32) <= currChar <= chr(126):
                    lexem += currChar

                    if currChar == '\'':
                        self.col += 1
                        return Token(TokenEnums.CTE_STR, lexem, self.row, self.col)

                else:
                    self.col += 1
                    return Token(TokenEnums.ER_CHAR, lexem, self.row, self.col)

            elif self.state == 11:
                if not (self.is_lower(currChar)) or self.is_blank(currChar):
                    self.back()
                    self.state = 12

                elif self.is_lower(currChar):
                    lexem += currChar

            elif self.state == 12:
                self.back()
                self.col += 1

                if WordDict.words[lexem] is not None:
                    return Token(WordDict.words[lexem], lexem, self.row, self.col)
                else:
                    return Token(TokenEnums.ER_PR, lexem, self.row, self.col)

            elif self.state == 13:
                self.new_line()
                self.content = self.txtline
                lexem = ''
                self.state = 0
            
            elif self.state == 14:
                currChar = self.next_char()
                self.col += 1
                if currChar == ".":
                    lexem += currChar
                    currChar = self.next_char()
                    self.col += 1
                    # Até onde eu entendi o send e recieve são commandos que precisam existir
                    if currChar == 's':
                        # Check for 'send' keyword
                        if self.peek(4) == 'end':
                            lexem += currChar
                            for _ in range(3):
                                lexem += self.next_char()
                            self.col += 4
                            return Token(TokenEnums.RW_SEND, lexem, self.row, self.col)
                        else:
                            #Se tiver errado tem que retornar um errinho
                            self.state = 1
                            return Token(TokenEnums.ER_CHANNEL, lexem, self.row, self.col)
                    elif currChar == 'r':
                        # Check for 'receive' keyword
                        if self.peek(7) == 'eceive':
                            lexem += currChar
                            for _ in range(6):
                                lexem += self.next_char()
                            self.col += 7
                            return Token(TokenEnums.RW_RECEIVE, lexem, self.row, self.col)
                        else:
                            self.state = 1
                            return Token(TokenEnums.ER_CHANNEL, lexem, self.row, self.col)

                else:
                    return Token(TokenEnums.RW_C_CHANNEL, lexem, self.row, self.col)


    def back(self):
        self.pos -= 1

    def new_line(self):

        tmp = ''

        try:
            tmp = self.reader.readline().decode("utf-8")

        except IOError as e:
            traceback.print_exc()

        if tmp != '':
            self.txtline = tmp

            if tmp[0] != '#':
                print(f"{self.row} {self.txtline}")

            self.txtline += " "
            self.row += 1
            self.pos = 0
            self.col = 0

            return True

        return False
