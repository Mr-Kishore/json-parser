package parser;

public enum TokenType {
    LEFT_BRACE,     // {
    RIGHT_BRACE,    // }
    LEFT_BRACKET,   // [
    RIGHT_BRACKET,  // ]
    COMMA,          // ,
    COLON,          // :
    STRING,         // "abc"
    NUMBER,         // 123, -45.67
    TRUE,           // true
    FALSE,          // false
    NULL,           // null
    EOF             // end of input
}