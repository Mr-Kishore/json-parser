from parser.exceptions import JsonSyntaxError, InvalidNumberError

MAX_STRING_LENGTH = 1_000_000  # Prevent DoS via huge strings
MAX_NUMBER_LENGTH = 100        # Prevent DoS via huge numbers

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class TokenTypes:
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    COLON = "COLON"
    COMMA = "COMMA"
    STRING = "STRING"
    NUMBER = "NUMBER"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    EOF = "EOF"

class Tokenizer:
    def __init__(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        self.text = text
        self.position = 0
        self.line = 1
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.text):
            current = self.text[self.position]

            if current == '\n':
                self.line += 1
                self.position += 1
                continue

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
                raise JsonSyntaxError(
                    f"Unexpected character: {current!r} at line {self.line}",
                    line=self.line
                )

        self.tokens.append(Token(TokenTypes.EOF, None))
        return self.tokens

    def handle_symbol(self, current):
        symbol_map = {
            '{': TokenTypes.LBRACE,
            '}': TokenTypes.RBRACE,
            '[': TokenTypes.LBRACKET,
            ']': TokenTypes.RBRACKET,
            ':': TokenTypes.COLON,
            ',': TokenTypes.COMMA
        }
        if current in symbol_map:
            self.add_symbol(symbol_map[current], current)
            return True
        return False

    def handle_literal(self):
        for literal, token_type, value in [
            ("true", TokenTypes.TRUE, True),
            ("false", TokenTypes.FALSE, False),
            ("null", TokenTypes.NULL, None)
        ]:
            if self.text.startswith(literal, self.position):
                self.tokens.append(Token(token_type, value))
                self.position += len(literal)
                return True
        return False

    def add_symbol(self, token_type, char):
        self.tokens.append(Token(token_type, char))
        self.position += 1

    def read_string(self):
        self.position += 1  # Skip opening quote
        start = self.position
        value = []
        while self.position < len(self.text):
            if len(value) > MAX_STRING_LENGTH:
                raise JsonSyntaxError("String too long", line=self.line)
            char = self.text[self.position]
            if char == '"':
                self.position += 1
                return Token(TokenTypes.STRING, ''.join(value))
            if char == '\\':
                self.position += 1
                if self.position >= len(self.text):
                    raise JsonSyntaxError("Unterminated escape sequence", line=self.line)
                esc = self.text[self.position]
                escapes = {
                    '"': '"', '\\': '\\', '/': '/',
                    'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'
                }
                if esc in escapes:
                    value.append(escapes[esc])
                elif esc == 'u':
                    # Unicode escape
                    if self.position + 4 >= len(self.text):
                        raise JsonSyntaxError("Incomplete unicode escape", line=self.line)
                    hex_digits = self.text[self.position+1:self.position+5]
                    if not all(c in '0123456789abcdefABCDEF' for c in hex_digits):
                        raise JsonSyntaxError("Invalid unicode escape", line=self.line)
                    value.append(chr(int(hex_digits, 16)))
                    self.position += 4
                else:
                    raise JsonSyntaxError(f"Invalid escape character: \\{esc}", line=self.line)
            elif ord(char) < 0x20:
                raise JsonSyntaxError("Invalid control character in string", line=self.line)
            else:
                value.append(char)
            self.position += 1
        raise JsonSyntaxError("Unterminated string", line=self.line)

    def read_number(self):
        start = self.position
        if self.text[self.position] == '-':
            self.position += 1
        digits = 0
        while self.position < len(self.text) and self.text[self.position].isdigit():
            self.position += 1
            digits += 1
            if digits > MAX_NUMBER_LENGTH:
                raise InvalidNumberError("Number too long")
        if self.position < len(self.text) and self.text[self.position] == '.':
            self.position += 1
            frac_digits = 0
            while self.position < len(self.text) and self.text[self.position].isdigit():
                self.position += 1
                frac_digits += 1
                if digits + frac_digits > MAX_NUMBER_LENGTH:
                    raise InvalidNumberError("Number too long")
            if frac_digits == 0:
                raise InvalidNumberError("Missing digits after decimal point")
        if self.position < len(self.text) and self.text[self.position] in 'eE':
            self.position += 1
            if self.position < len(self.text) and self.text[self.position] in '+-':
                self.position += 1
            exp_digits = 0
            while self.position < len(self.text) and self.text[self.position].isdigit():
                self.position += 1
                exp_digits += 1
                if exp_digits > 10:
                    raise InvalidNumberError("Exponent too large")
            if exp_digits == 0:
                raise InvalidNumberError("Missing exponent digits")
        value = self.text[start:self.position]
        try:
            num = float(value) if ('.' in value or 'e' in value or 'E' in value) else int(value)
            return Token(TokenTypes.NUMBER, num)
        except ValueError:
            raise InvalidNumberError(f"Invalid number: {value}")

    def peek(self):
        if self.position + 1 < len(self.text):
            return self.text[self.position + 1]
        return ''