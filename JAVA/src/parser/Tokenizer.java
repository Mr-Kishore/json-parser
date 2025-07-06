package parser;

import java.util.ArrayList;
import java.util.List;

public class Tokenizer {
    private final String input;
    private int position;
    private final int length;

    public Tokenizer(String input) {
        this.input = input.trim();       // clean whitespace
        this.position = 0;
        this.length = this.input.length();  // get trimmed length
    }

    public List<Token> tokenize() {
        List<Token> tokens = new ArrayList<>();

        while (!isAtEnd()) {
            char current = peek();

            switch (current) {
                case '{':
                    tokens.add(new Token(TokenType.LEFT_BRACE, "{"));
                    advance();
                    break;
                case '}':
                    tokens.add(new Token(TokenType.RIGHT_BRACE, "}"));
                    advance();
                    break;
                case '[':
                    tokens.add(new Token(TokenType.LEFT_BRACKET, "["));
                    advance();
                    break;
                case ']':
                    tokens.add(new Token(TokenType.RIGHT_BRACKET, "]"));
                    advance();
                    break;
                case ',':
                    tokens.add(new Token(TokenType.COMMA, ","));
                    advance();
                    break;
                case ':':
                    tokens.add(new Token(TokenType.COLON, ":"));
                    advance();
                    break;
                case '"':
                    tokens.add(new Token(TokenType.STRING, readString()));
                    break;
                default:
                    if (isDigit(current) || current == '-') {
                        tokens.add(new Token(TokenType.NUMBER, readNumber()));
                    } else if (startsWith("true")) {
                        tokens.add(new Token(TokenType.TRUE, "true"));
                        advance(4);
                    } else if (startsWith("false")) {
                        tokens.add(new Token(TokenType.FALSE, "false"));
                        advance(5);
                    } else if (startsWith("null")) {
                        tokens.add(new Token(TokenType.NULL, "null"));
                        advance(4);
                    } else if (Character.isWhitespace(current)) {
                        advance(); // skip
                    } else {
                        throw new RuntimeException("Unexpected character: '" + current + "' at position " + position);
                    }
            }
        }

        tokens.add(new Token(TokenType.EOF, null));
        return tokens;
    }

    private boolean isAtEnd() {
        return position >= length;
    }

    private char peek() {
        if (isAtEnd()) {
            throw new RuntimeException("Attempted to peek beyond input at position " + position);
        }
        return input.charAt(position);
    }

    private void advance() {
        position++;
    }

    private void advance(int count) {
        position += count;
    }

    private boolean startsWith(String keyword) {
        return input.startsWith(keyword, position);
    }

    private String readString() {
        StringBuilder sb = new StringBuilder();
        advance(); // skip opening quote

        while (!isAtEnd()) {
            char current = peek();

            if (current == '"') {
                advance(); // closing quote
                return sb.toString();
            } else if (current == '\\') {
                advance(); // skip backslash
                if (isAtEnd()) break;

                char escape = peek();
                switch (escape) {
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    case '/': sb.append('/'); break;
                    case 'b': sb.append('\b'); break;
                    case 'f': sb.append('\f'); break;
                    case 'n': sb.append('\n'); break;
                    case 'r': sb.append('\r'); break;
                    case 't': sb.append('\t'); break;
                    default:
                        throw new RuntimeException("Invalid escape character: \\" + escape);
                }
                advance();
            } else {
                sb.append(current);
                advance();
            }
        }

        throw new RuntimeException("Unterminated string at position " + position);
    }

    private String readNumber() {
        StringBuilder sb = new StringBuilder();

        if (!isAtEnd() && peek() == '-') {
            sb.append('-');
            advance();
        }

        while (!isAtEnd() && isDigit(peek())) {
            sb.append(peek());
            advance();
        }

        if (!isAtEnd() && peek() == '.') {
            sb.append('.');
            advance();

            while (!isAtEnd() && isDigit(peek())) {
                sb.append(peek());
                advance();
            }
        }

        return sb.toString();
    }

    private boolean isDigit(char c) {
        return c >= '0' && c <= '9';
    }
}
