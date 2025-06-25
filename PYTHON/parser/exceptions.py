__all__ = [
    "JsonParserError",
    "UnexpectedTokenError",
    "UnterminatedStringError",
    "InvalidNumberError",
    "JsonSyntaxError",
]

def _safe_repr(value, max_length=100):
    """Safely represent a value for error messages, truncating if necessary."""
    try:
        result = repr(value)
    except Exception:
        result = "<unrepresentable>"
    if len(result) > max_length:
        result = result[:max_length - 3] + "..."
    return result

class JsonParserError(Exception):
    """Base exception for JSON parser errors."""
    pass

class UnexpectedTokenError(JsonParserError):
    """Raised when an unexpected token is encountered."""
    def __init__(self, expected, actual):
        actual_type = getattr(actual, 'type', '<unknown>')
        actual_value = getattr(actual, 'value', '<unknown>')
        safe_value = _safe_repr(actual_value)
        message = (
            f"Expected token '{_safe_repr(expected)}', "
            f"but got '{_safe_repr(actual_type)}' with value {safe_value}"
        )
        super().__init__(message)

class UnterminatedStringError(JsonParserError):
    """Raised when a string literal is not terminated."""
    def __init__(self):
        super().__init__("Unterminated string literal found while parsing.")

class InvalidNumberError(JsonParserError):
    """Raised when an invalid number format is encountered."""
    def __init__(self, value):
        safe_value = _safe_repr(value)
        super().__init__(f"Invalid number format: {safe_value}")

class JsonSyntaxError(JsonParserError):
    """Raised for generic syntax errors in JSON."""
    def __init__(self, message, line=None):
        safe_message = _safe_repr(message, max_length=200)
        full_message = f"Syntax Error: {safe_message}"
        if line is not None:
            full_message += f" (line {line})"
        super().__init__(full_message)