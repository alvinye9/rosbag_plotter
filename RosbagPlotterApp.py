import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from PlotManager import PlotManager
from FileSelector import FileSelector

class DataPlotterApp:
    """Main application class handling the GUI and end-user interactions."""

    def __init__(self, root):
        self.root = root
        self.root.title("Data Plotter")

        # Initialize variables for dropdown selections
        self.dropdown_var1a = tk.StringVar(root)
        self.dropdown_var1b = tk.StringVar(root)
        self.dropdown_var2a = tk.StringVar(root)
        self.dropdown_var2b = tk.StringVar(root)
        self.auto_y_axis_var = tk.IntVar(value=0)  
        self.use_custom_x_var = tk.IntVar(value=0)  

        self.dropdown_var_x1 = tk.StringVar(root)
        self.dropdown_var_x2 = tk.StringVar(root)

        # Initialize the FileSelector and PlotManager
        self.file_selector = FileSelector(root)
        self.plot_manager = PlotManager()
        
        # Store OptionMenu references
        self.option_menus = []

        # Setup the GUI components
        self.setup_gui()

    def setup_gui(self):
        # File 1
        tk.Label(self.root, text="Rosbag 1:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_file1 = tk.Entry(self.root, width=50)
        self.entry_file1.grid(row=0, column=1, padx=5, pady=5)
        dropdown1a = tk.OptionMenu(self.root, self.dropdown_var1a, "")
        dropdown1b = tk.OptionMenu(self.root, self.dropdown_var1b, "")
        # lambda function required to prevent the function from auto running
        tk.Button(self.root, text="Browse...", command=lambda: self.file_selector.load_file(self.entry_file1, [self.dropdown_var1a, self.dropdown_var1b], [dropdown1a, dropdown1b])).grid(row=0, column=2, padx=5, pady=5)
        dropdown1a.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 1 (Top Plot):").grid(row=1, column=0, padx=5, pady=5)
        dropdown1b.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 2 (Bottom Plot):").grid(row=2, column=0, padx=5, pady=5)

        # File 2
        tk.Label(self.root, text="Rosbag 2:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_file2 = tk.Entry(self.root, width=50)
        self.entry_file2.grid(row=3, column=1, padx=5, pady=5)
        dropdown2a = tk.OptionMenu(self.root, self.dropdown_var2a, "")
        dropdown2b = tk.OptionMenu(self.root, self.dropdown_var2b, "")
        tk.Button(self.root, text="Browse...", command=lambda: self.file_selector.load_file(self.entry_file2, [self.dropdown_var2a, self.dropdown_var2b], [dropdown2a, dropdown2b])).grid(row=3, column=2, padx=5, pady=5)
        dropdown2a.grid(row=4, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 1 (Top Plot):").grid(row=4, column=0, padx=5, pady=5)
        dropdown2b.grid(row=5, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 2 (Bottom Plot):").grid(row=5, column=0, padx=5, pady=5)

        # Shift seconds for file 1
        tk.Label(self.root, text="X-axis left-shift for Rosbag 1:").grid(row=6, column=0, padx=5, pady=5)
        self.entry_shift1 = tk.Entry(self.root, width=10)
        self.entry_shift1.grid(row=6, column=1, padx=5, pady=5)
        self.entry_shift1.insert(0, "0.0")

        # Shift seconds for file 2
        tk.Label(self.root, text="X-axis left-shift for Rosbag 2:").grid(row=7, column=0, padx=5, pady=5)
        self.entry_shift2 = tk.Entry(self.root, width=10)
        self.entry_shift2.grid(row=7, column=1, padx=5, pady=5)
        self.entry_shift2.insert(0, "0.0")

        # Y-axis limits for Lateral Error
        tk.Label(self.root, text="Y-axis limits for Topic 1 (min, max):").grid(row=8, column=0, padx=5, pady=5)
        self.entry_y_min_1 = tk.Entry(self.root, width=10)
        self.entry_y_min_1.grid(row=8, column=1, padx=5, pady=5, sticky="W")
        self.entry_y_min_1.insert(0, "-10.0")
        self.entry_y_max_1 = tk.Entry(self.root, width=10)
        self.entry_y_max_1.grid(row=8, column=1, padx=5, pady=5, sticky="E")
        self.entry_y_max_1.insert(0, "10.0")

        # Y-axis limits for Vehicle Roll
        tk.Label(self.root, text="Y-axis limits for Topic 2 (min, max):").grid(row=9, column=0, padx=5, pady=5)
        self.entry_y_min_2 = tk.Entry(self.root, width=10)
        self.entry_y_min_2.grid(row=9, column=1, padx=5, pady=5, sticky="W")
        self.entry_y_min_2.insert(0, "-10.0")
        self.entry_y_max_2 = tk.Entry(self.root, width=10)
        self.entry_y_max_2.grid(row=9, column=1, padx=5, pady=5, sticky="E")
        self.entry_y_max_2.insert(0, "10.0")

        # Auto-format Y-axis checkbox
        tk.Checkbutton(self.root, text="Auto-scale Y-axis", variable=self.auto_y_axis_var).grid(row=10, column=1, padx=5, pady=5, sticky="W")
        
        # Use another value for X-axis checkbox
        tk.Checkbutton(self.root, text="Use another value for X-axis", variable=self.use_custom_x_var, command=self.toggle_x_axis_dropdowns).grid(row=11, column=1, padx=5, pady=5, sticky="W")

        # X-axis dropdowns (initially hidden)
        self.dropdown_x1 = tk.OptionMenu(self.root, self.dropdown_var_x1, "")
        self.dropdown_x2 = tk.OptionMenu(self.root, self.dropdown_var_x2, "")
        self.option_menus.extend([self.dropdown_x1, self.dropdown_x2])
        
        # Start plotting button
        tk.Button(self.root, text="Plot Data", command=self.start_plotting).grid(row=15, column=0, columnspan=3, pady=10)

    def toggle_x_axis_dropdowns(self):
        """Show or hide X-axis dropdowns based on checkbox."""
        if self.use_custom_x_var.get():
            self.dropdown_x1.grid(row=12, column=1, padx=5, pady=5)
            self.dropdown_x2.grid(row=12, column=2, padx=5, pady=5)
            
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_x1], [self.dropdown_x1])
            self.file_selector.populate_dropdown(self.entry_file2.get(), [self.dropdown_var_x2], [self.dropdown_x2])
                
        else:
            self.dropdown_x1.grid_remove()
            self.dropdown_x2.grid_remove()

    def start_plotting(self):
        file1_path = self.entry_file1.get()
        file2_path = self.entry_file2.get()

        if not file1_path or not file2_path:
            messagebox.showerror("Error", "Please specify both CSV files.")
            return

        try:
            shift_seconds = float(self.entry_shift1.get())
            shift_seconds_2 = float(self.entry_shift2.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid shift seconds.")
            return

        topics1 = [self.dropdown_var1a.get(), self.dropdown_var1b.get()]
        topics2 = [self.dropdown_var2a.get(), self.dropdown_var2b.get()]
        auto_y_axis = bool(self.auto_y_axis_var.get())

        if self.use_custom_x_var.get():
            # print("Use custom x axis")
            x_axis1 = self.dropdown_var_x1.get()
            x_axis2 = self.dropdown_var_x2.get()
        else:
            x_axis1 = x_axis2 = '__time'

        y_limits = {
            'topic 1': [float(self.entry_y_min_1.get()), float(self.entry_y_max_1.get())],
            'topic 2': [float(self.entry_y_min_2.get()), float(self.entry_y_max_2.get())]
        }
        
        try:
            df1 = pd.read_csv(file1_path)
            df2 = pd.read_csv(file2_path)

            df1.fillna(method='ffill', inplace=True)
            df2.fillna(method='ffill', inplace=True)

            df1['__time'] -= df1['__time'].min()
            df2['__time'] -= df2['__time'].min()

            df1_shifted = self.plot_manager.shift_data(df1.copy(), shift_seconds)
            df2_shifted = self.plot_manager.shift_data(df2.copy(), shift_seconds_2)

            self.plot_manager.plot_data(df1_shifted, df2_shifted, topics1, topics2, x_axis1, x_axis2, y_lims=y_limits, auto_y_axis=auto_y_axis)

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()
