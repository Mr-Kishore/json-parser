import parser.*;

import java.util.List;

public class JsonParserTest {
    public static void main(String[] args) {
        String json = """
        {
            "name": "Kishore",
            "age": 25,
            "languages": ["Java", "Python", "Rust"],
            "active": true,
            "address": {
                "city": "Chennai",
                "pin": 600001
            },
            "projects": null
        }
        """;

        try {
            // Tokenize
            Tokenizer tokenizer = new Tokenizer(json);
            List<Token> tokens = tokenizer.tokenize();
            System.out.println("Tokens:");
            for (Token token : tokens) {
                System.out.println("  " + token);
            }

            // Parse
            JsonParser parser = new JsonParser(tokens);
            Object parsed = parser.parse();
            System.out.println("\nParsed Output:");
            System.out.println(parsed);

        } catch (Exception e) {
            System.err.println("Parsing failed: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
