# JSON Parser - Python

This subfolder contains the implementation of the JSON Parser in **Python**.  
The parser is written from scratch without using Python's built-in `json` module to provide a deeper understanding of how parsing works internally.

---

# What does this implementation do?

- Implements a custom tokenizer that breaks a raw JSON string into valid tokens
- Uses a recursive descent parser to interpret the tokens and build valid Python data structures
- Supports:
  - JSON Objects (`{ ... }`)
  - JSON Arrays (`[ ... ]`)
  - Strings, numbers, booleans, and null
  - Nested structures
- Provides a **Tkinter GUI** that allows users to:
  - Drag and drop `.json` files
  - View the parsed output in a scrollable output window

---

# Folder Structure

```
PYTHON/
├── parser/
│   ├── __init__.py
│   ├── tokenizer.py
│   ├── parser.py
│   └── exceptions.py
│
├── gui/
│   ├── __init__.py
│   ├── app.py
│   └── file_handler.py
│
├── assets/
│   └── sample.json
│
├── main.py
├── requirements.txt
└── README.md
```

---

# How to Run

1. Make sure you have Python 3.8 or above installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

4. Drag and drop a `.json` file into the window and click **Parse** to view the result.

---

# Sample JSON Input

```json
{
  "name": "Kishore",
  "age": 19,
  "skills": ["Python", "Computer Hardware"],
  "active": true,
  "address": {
    "city": "Chennai",
    "zip": 600001
  }
}
```

---

# Note

- This parser is intentionally built without using Python’s `json` module to demonstrate the logic of parsing.
- It includes basic error handling and structure validation.
- The GUI enhances usability and makes testing easier via drag-and-drop interface.

---

# Author

Developed by [Kishore](https://github.com/Mr-Kishore)  
Part of the multi-language JSON parser repository for educational purposes.
