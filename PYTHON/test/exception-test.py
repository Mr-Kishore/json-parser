import sys
import os

# Setup path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.tokenizer import Tokenizer
from parser.parser import Parser
from parser.exceptions import JsonParserError

# Malformed JSON string (170+ chars)
bad_json = '''
{
  name: Kishore,
  age: 19a,
  active: truue,
  skills: ["Python", "Hardware", ],
  address: { "city": "Chennai", "zip": 600001
'''

try:
    tokens = Tokenizer(bad_json).tokenize()
    parser = Parser(tokens)
    result = parser.parse()
    print("Parsed Result:", result)

except JsonParserError as e:
    print("JSON Parsing Failed:")
    print(e)

except ValueError as e:
    # Catch tokenizer-level ValueErrors
    print("Tokenizer Error:")
    print(e)

except Exception as e:
    print("Unexpected Error:")
    print(e)
# This code tests the JSON parser with a malformed JSON string.
# It attempts to tokenize and parse the JSON, catching specific exceptions
# related to JSON parsing errors, tokenizer errors, and any unexpected errors.
# The output will indicate the type of error encountered, helping to identify issues in the JSON structure or the tokenizer/parser logic.

