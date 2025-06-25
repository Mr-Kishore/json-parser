import os
import sys
import json
from tkinter import Tk, Button, scrolledtext, filedialog, messagebox, END, WORD, BOTH
from tkinterdnd2 import DND_FILES, TkinterDnD
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser.tokenizer import Tokenizer
from parser.parser import Parser
from parser.exceptions import JsonParserError, JsonSyntaxError
from gui.file_handler import read_json_file

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
MAX_OUTPUT_LENGTH = 10000
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'output')


def is_safe_path(filepath):
    user_home = os.path.expanduser("~")
    cwd = os.path.abspath(os.getcwd())
    abs_path = os.path.abspath(filepath)
    return abs_path.startswith(user_home) or abs_path.startswith(cwd)


class JsonParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom JSON Parser")
        self.root.geometry("900x600")
        self.json_filepath = None
        self.last_failed_content = None
        self.create_widgets()
        self.setup_drag_and_drop()

    def create_widgets(self):
        self.select_button = Button(self.root, text="Select JSON File", command=self.load_file_dialog)
        self.select_button.pack(pady=10)

        self.fix_button = Button(self.root, text="Fix with AI", command=self.fix_with_ai)
        self.fix_button.pack(pady=5)

        self.export_button = Button(self.root, text="Export Result as .txt", command=self.export_result)
        self.export_button.pack(pady=5)

        self.output_area = scrolledtext.ScrolledText(self.root, wrap=WORD, font=("Courier", 10))
        self.output_area.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def setup_drag_and_drop(self):
        self.output_area.drop_target_register(DND_FILES)
        self.output_area.dnd_bind("<<Drop>>", self.handle_drop)

    def handle_drop(self, event):
        filepath = event.data.strip().strip("{").strip("}")
        if not filepath.lower().endswith(".json"):
            messagebox.showerror("Invalid File", "Please drop a valid .json file.")
            return
        if not is_safe_path(filepath):
            messagebox.showerror("Security Error", "Access to this file is not allowed.")
            return
        self.load_and_parse(filepath)

    def load_file_dialog(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            if not is_safe_path(filepath):
                messagebox.showerror("Security Error", "Access to this file is not allowed.")
                return
            self.load_and_parse(filepath)

    def load_and_parse(self, filepath):
        try:
            if not os.path.isfile(filepath):
                raise JsonParserError("File does not exist.")
            if os.path.getsize(filepath) > MAX_FILE_SIZE:
                raise JsonParserError("File is too large (max 2MB).")

            json_text = read_json_file(filepath)
            if not isinstance(json_text, str):
                raise JsonParserError("File encoding error.")

            self.json_filepath = filepath
            self.last_failed_content = json_text  # Save for AI fixer

            tokens = Tokenizer(json_text).tokenize()
            result = Parser(tokens).parse()

            output = "Parsed JSON Object:\n" + str(result)
            if len(output) > MAX_OUTPUT_LENGTH:
                output = output[:MAX_OUTPUT_LENGTH] + "\n... (output truncated)"

            self.display_output(output)

        except JsonSyntaxError as e:
            self.display_output(f"Syntax Error:\n{str(e)}\n\nYou can try to fix it using the 'Fix with AI' button.")
            self.last_failed_content = json_text
            if hasattr(e, 'line') and e.line:
                self.highlight_error_line(e.line)

        except JsonParserError as e:
            self.display_output(f"Error:\n{str(e)}\n\nTry fixing with AI if it's a formatting issue.")
            self.last_failed_content = json_text

        except Exception:
            self.display_output("Unexpected Error: An internal error occurred.")

    def display_output(self, text):
        self.output_area.delete(1.0, END)
        self.output_area.insert(END, text)

    def highlight_error_line(self, line_number):
        try:
            index = f"{line_number}.0"
            self.output_area.tag_configure("error_line", background="#ffdddd")
            self.output_area.tag_add("error_line", index, f"{line_number}.end")
            self.output_area.see(index)
        except Exception:
            pass

    def export_result(self):
        try:
            if not os.path.exists(OUTPUT_FOLDER):
                os.makedirs(OUTPUT_FOLDER)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            base_name = os.path.splitext(os.path.basename(self.json_filepath or "output"))[0]
            output_file = os.path.join(OUTPUT_FOLDER, f"{base_name}-parsed-{timestamp}.txt")

            content = self.output_area.get("1.0", END).strip()
            if not content:
                messagebox.showwarning("Export Warning", "Nothing to export.")
                return

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            messagebox.showinfo("Export Successful", f"Output saved to:\n{output_file}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")

    def fix_with_ai(self):
        if not self.last_failed_content:
            messagebox.showinfo("No Content", "No invalid JSON to fix.")
            return

        try:
            # Simulate AI fix using Python’s lenient json parser
            fixed = json.loads(self.last_failed_content)
            output = "✅ AI Fixed JSON:\n" + json.dumps(fixed, indent=2)
            self.display_output(output)
        except json.JSONDecodeError as e:
            self.display_output(f"❌ AI failed to fix JSON.\nReason: {str(e)}")
        except Exception as e:
            self.display_output(f"AI Fixer Error:\n{str(e)}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = JsonParserApp(root)
    root.mainloop()
