import sys
from enum import Enum, auto

class TokenType(Enum):
    INT = auto()
    OCT = auto()
    HEX = auto()
    BIN = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()

class Token:
    def __init__(self, text, token_type):
        self.text = text
        self.type = token_type
    def __repr__(self):
        return f"{self.type.name}"

class Lexer:
    def __init__(self, source):
        self.source = source
        self.curPos = -1
        self.curChar = ''
        self.nextChar()

    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = None
        else:
            self.curChar = self.source[self.curPos]

    def make_token(self, startPos, token_type):
        text = self.source[startPos:self.curPos]
        return Token(text, token_type)

    def getTokens(self):
        tokens = []
        while self.curChar is not None:
            tk = self.q0(self.curPos)
            if tk is not None:  # None means skip (e.g., whitespace)
                tokens.append(tk)
        return tokens

    # ---- DFA states ----
    def q0(self, startPos):
        if self.curChar is None:
            return None
        elif self.curChar.isspace():
            self.nextChar()
            return None  # skip whitespace
        elif self.curChar == '+':
            self.nextChar()
            return self.q_add(startPos)
        elif self.curChar == '-':
            self.nextChar()
            return self.q_sub(startPos)
        elif self.curChar == '*':
            self.nextChar()
            return self.q_mul(startPos)
        elif self.curChar == '/':
            self.nextChar()
            return self.q_div(startPos)
        elif self.curChar.isdigit():
            if self.curChar == '0':
                self.nextChar()
                return self.q1(startPos)
            else:
                self.nextChar()
                return self.q2(startPos)
        else:
            raise Exception(f"Unexpected character: {self.curChar}")

    # Operators (accepting states)
    def q_add(self, startPos):
        return self.make_token(startPos, TokenType.ADD)
    def q_sub(self, startPos):
        return self.make_token(startPos, TokenType.SUB)
    def q_mul(self, startPos):
        return self.make_token(startPos, TokenType.MUL)
    def q_div(self, startPos):
        return self.make_token(startPos, TokenType.DIV)

    # Numbers
    def q1(self, startPos):
        if self.curChar in "01234567":
            self.nextChar()
            return self.q3(startPos)
        elif self.curChar in "bB":
            self.nextChar()
            return self.q6(startPos)
        elif self.curChar in "xX":
            self.nextChar()
            return self.q4(startPos)
        else:
            return self.make_token(startPos, TokenType.INT)

    def q2(self, startPos):
        if self.curChar is not None and self.curChar.isdigit():
            self.nextChar()
            return self.q2(startPos)
        else:
            return self.make_token(startPos, TokenType.INT)

    def q3(self, startPos):
        if self.curChar is not None and self.curChar in "01234567":
            self.nextChar()
            return self.q3(startPos)
        else:
            return self.make_token(startPos, TokenType.OCT)

    def q4(self, startPos):
        if self.curChar is not None and self.curChar.upper() in "0123456789ABCDEF":
            self.nextChar()
            return self.q4(startPos)
        else:
            return self.make_token(startPos, TokenType.HEX)

    def q6(self, startPos):
        if self.curChar is not None and self.curChar in "01":
            self.nextChar()
            return self.q6(startPos)
        else:
            return self.make_token(startPos, TokenType.BIN)

if __name__ == "__main__":
    # Read all input from stdin (strip to remove trailing newlines)
    source = sys.stdin.read().strip()

    lexer = Lexer(source)
    tokens = lexer.getTokens()

    # Print tokens, one per line or in a list
    print(tokens)
