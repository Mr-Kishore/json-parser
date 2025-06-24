class JsonParserError(Exception):
    """Base class for all JSON parser errors."""
    pass


class UnexpectedTokenError(JsonParserError):
    def __init__(self, expected, actual):
        # Avoid leaking sensitive data from token values
        actual_type = getattr(actual, 'type', '<unknown>')
        actual_value = getattr(actual, 'value', '<unknown>')
        # Limit the length of value to prevent log injection or excessive output
        safe_value = str(actual_value)
        if len(safe_value) > 100:
            safe_value = safe_value[:97] + '...'
        message = (
            f"Expected token '{expected}', but got '{actual_type}' with value {safe_value!r}"
        )
        super().__init__(message)

class JsonSyntaxError(Exception):
    pass

class UnterminatedStringError(JsonParserError):
    def __init__(self):
        super().__init__("Unterminated string literal found while parsing.")


class InvalidNumberError(JsonParserError):
    def __init__(self, value):
        # Avoid leaking potentially sensitive or very large values
        safe_value = str(value)
        if len(safe_value) > 100:
            safe_value = safe_value[:97] + '...'
        super().__init__(f"Invalid number format: {safe_value}")


class JsonSyntaxError(JsonParserError):
    def __init__(self, message):
        # Limit error message length to prevent abuse
        safe_message = str(message)
        if len(safe_message) > 200:
            safe_message = safe_message[:197] + '...'
        super().__init__(f"Syntax Error: {safe_message}")
