from .exceptions import *


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.text):
            current = self.text[self.position]

            if current.isspace():
                self.position += 1
                continue

            if self.handle_symbol(current):
                continue
            elif current == '"':
                self.tokens.append(self.read_string())
            elif current.isdigit() or (current == '-' and self.peek().isdigit()):
                self.tokens.append(self.read_number())
            elif self.handle_literal():
                continue
            else:
                raise JsonSyntaxError(f"Unexpected character: {current}")

        self.tokens.append(Token("EOF", None))
        return self.tokens

    def handle_symbol(self, current):
        symbol_map = {
            '{': "LBRACE",
            '}': "RBRACE",
            '[': "LBRACKET",
            ']': "RBRACKET",
            ':': "COLON",
            ',': "COMMA"
        }
        if current in symbol_map:
            self.tokens.append(Token(symbol_map[current], current))
            self.position += 1
            return True
        return False

    def handle_literal(self):
        if self.text.startswith("true", self.position):
            self.tokens.append(Token("TRUE", True))
            self.position += 4
            return True
        elif self.text.startswith("false", self.position):
            self.tokens.append(Token("FALSE", False))
            self.position += 5
            return True
        elif self.text.startswith("null", self.position):
            self.tokens.append(Token("NULL", None))
            self.position += 4
            return True
        return False

    def read_string(self):
        self.position += 1
        start = self.position
        while self.position < len(self.text):
            if self.text[self.position] == '"':
                value = self.text[start:self.position]
                self.position += 1
                return Token("STRING", value)
            self.position += 1
        raise UnterminatedStringError()

    def read_number(self):
        start = self.position
        if self.text[self.position] == '-':
            self.position += 1
        while self.position < len(self.text) and self.text[self.position].isdigit():
            self.position += 1
        if self.position < len(self.text) and self.text[self.position] == '.':
            self.position += 1
            if not self.text[self.position].isdigit():
                raise InvalidNumberError(self.text[start:self.position])
            while self.position < len(self.text) and self.text[self.position].isdigit():
                self.position += 1
        value = self.text[start:self.position]
        try:
            return Token("NUMBER", float(value) if '.' in value else int(value))
        except ValueError:
            raise InvalidNumberError(value)

    def peek(self):
        return self.text[self.position + 1] if self.position + 1 < len(self.text) else ''
