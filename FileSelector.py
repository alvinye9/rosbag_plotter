from tkinter import filedialog, messagebox
import pandas as pd
import tkinter as tk

class FileSelector:
    """File selection and populating dropdowns with available topics"""

    def __init__(self, root):
        self.root = root

    def load_file(self, entry, dropdown_vars, dropdowns):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)
            self.populate_dropdown(file_path, dropdown_vars, dropdowns)
        return file_path

    def populate_dropdown(self, file_path, dropdown_vars, dropdowns):
        try:
            df = pd.read_csv(file_path)
            topics = df.columns.tolist()
            for dropdown_var, dropdown in zip(dropdown_vars, dropdowns):
                dropdown['menu'].delete(0, 'end')
                for topic in topics:
                    dropdown['menu'].add_command(label=topic, command=tk._setit(dropdown_var, topic))
                dropdown_var.set(topics[0])  # Set the default value to the first topic
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load topics: {e}")