# main.py

from tkinterdnd2 import TkinterDnD
from gui.app import JsonParserApp

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = JsonParserApp(root)
    root.mainloop()
