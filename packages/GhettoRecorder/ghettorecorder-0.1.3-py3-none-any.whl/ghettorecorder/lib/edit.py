import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class UItextEditor(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Ghetto Recorder Editor")
        self.rowconfigure(0, minsize=400, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)

        self.fr_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.fr_buttons.grid(row=0, column=0, sticky="ns")
        self.txt_edit = tk.Text(self)
        self.txt_edit.grid(row=0, column=1, sticky="nsew")

        self.btn_open = tk.Button(self.fr_buttons, text="Open", command=self.open_file)
        self.btn_save = tk.Button(self.fr_buttons, text="Save As...", command=self.save_file)

        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.btn_save.grid(row=1, column=0, sticky="ew", padx=5)

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        self.txt_edit.delete(1.0, tk.END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            self.txt_edit.insert(tk.END, text)
        self.title(f"Ghetto Recorder Editor - {filepath}")

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = self.txt_edit.get(1.0, tk.END)
            output_file.write(text)
        self.title(f"Ghetto Recorder Editor - {filepath}")
