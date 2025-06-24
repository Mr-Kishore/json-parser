import sys
import os

# Get absolute path to PYTHON/ and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.tokenizer import Tokenizer

# Sample test
json_text = '''
{
  "name": "Kishore",
  "age": 19,
  "skills": ["Python", "Computer Hardware"],
  "active": true,
  "address": {
    "city": "Theni",
    "zip": 625531
  }
}
'''

tokenizer = Tokenizer(json_text)
tokens = tokenizer.tokenize()

for token in tokens:
    print(token)
