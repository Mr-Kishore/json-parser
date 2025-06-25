import sys
import os

# Add the parent directory to sys.path to access parser and tokenizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from parser.parser import Parser
from parser.tokenizer import Tokenizer
from parser.parser import Parser

# Sample JSON string
json_text = '''
{
  "name": "Kishore",
  "age": 19,
  "active": true,
  "skills": ["Python", "Hardware"],
  "address": { "city": "Chennai", "pin": 600001 }
}
'''

# Tokenize the input
tokens = Tokenizer(json_text).tokenize()

# Parse the tokens into a Python object
parser = Parser(tokens)
result = parser.parse()

# Display the result
print("Parsed JSON Object:")
print(result)
