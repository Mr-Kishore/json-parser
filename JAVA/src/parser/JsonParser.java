package parser;

import java.util.*;

public class JsonParser {
    private final List<Token> tokens;
    private int position;

    public JsonParser(List<Token> tokens) {
        this.tokens = tokens;
        this.position = 0;
    }

    public Object parse() {
        return parseValue();
    }

    private Token peek() {
        return tokens.get(position);
    }

    private Token advance() {
        return tokens.get(position++);
    }

    private boolean match(TokenType type) {
        if (peek().type == type) {
            advance();
            return true;
        }
        return false;
    }

    private void expect(TokenType type) {
        if (!match(type)) {
            throw new RuntimeException("Expected token: " + type + " but got: " + peek().type);
        }
    }

    private Object parseValue() {
        Token token = peek();

        switch (token.type) {
            case LEFT_BRACE: return parseObject();
            case LEFT_BRACKET: return parseArray();
            case STRING: advance(); return token.value;
            case NUMBER: advance(); return Double.parseDouble(token.value);
            case TRUE: advance(); return true;
            case FALSE: advance(); return false;
            case NULL: advance(); return null;
            default:
                throw new RuntimeException("Unexpected token: " + token.type);
        }
    }

    private Map<String, Object> parseObject() {
        Map<String, Object> map = new LinkedHashMap<>();
        expect(TokenType.LEFT_BRACE);

        if (match(TokenType.RIGHT_BRACE)) {
            return map; // empty object
        }

        do {
            Token keyToken = peek();
            if (keyToken.type != TokenType.STRING) {
                throw new RuntimeException("Expected STRING key, got: " + keyToken.type);
            }
            String key = keyToken.value;
            advance();

            expect(TokenType.COLON);
            Object value = parseValue();
            map.put(key, value);
        } while (match(TokenType.COMMA));

        expect(TokenType.RIGHT_BRACE);
        return map;
    }

    private List<Object> parseArray() {
        List<Object> list = new ArrayList<>();
        expect(TokenType.LEFT_BRACKET);

        if (match(TokenType.RIGHT_BRACKET)) {
            return list; // empty array
        }

        do {
            list.add(parseValue());
        } while (match(TokenType.COMMA));

        expect(TokenType.RIGHT_BRACKET);
        return list;
    }
}
