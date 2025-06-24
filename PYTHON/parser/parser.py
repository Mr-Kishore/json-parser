from .tokenizer import Token
from .exceptions import UnexpectedTokenError, JsonSyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        value = self.parse_value()
        self.expect("EOF")
        return value

    def parse_value(self):
        current = self.current_token()

        if current.type in ("STRING", "NUMBER"):
            self.advance()
            return current.value
        elif current.type == "TRUE":
            self.advance()
            return True
        elif current.type == "FALSE":
            self.advance()
            return False
        elif current.type == "NULL":
            self.advance()
            return None
        elif current.type == "LBRACE":
            return self.parse_object()
        elif current.type == "LBRACKET":
            return self.parse_array()
        else:
            raise JsonSyntaxError(f"Unexpected token: {current}")

    def parse_object(self):
        obj = {}
        self.expect("LBRACE")

        if self.current_token().type == "RBRACE":
            self.advance()
            return obj

        while True:
            key_token = self.expect("STRING")
            self.expect("COLON")
            value = self.parse_value()
            obj[key_token.value] = value

            if self.current_token().type == "COMMA":
                self.advance()
            elif self.current_token().type == "RBRACE":
                self.advance()
                break
            else:
                raise JsonSyntaxError("Expected ',' or '}' in object")

        return obj

    def parse_array(self):
        arr = []
        self.expect("LBRACKET")

        if self.current_token().type == "RBRACKET":
            self.advance()
            return arr

        while True:
            value = self.parse_value()
            arr.append(value)

            if self.current_token().type == "COMMA":
                self.advance()
            elif self.current_token().type == "RBRACKET":
                self.advance()
                break
            else:
                raise JsonSyntaxError("Expected ',' or ']' in array")

        return arr

    def expect(self, expected_type):
        token = self.current_token()
        if token.type != expected_type:
            raise UnexpectedTokenError(expected_type, token)
        self.advance()
        return token

    def advance(self):
        self.position += 1

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else Token("EOF", None)
