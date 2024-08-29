import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from PlotManager import PlotManager
from FileSelector import FileSelector
from matplotlib.widgets import Slider

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
        self.dropdown_var3a = tk.StringVar(root)
        self.dropdown_var3b = tk.StringVar(root)
        
        self.auto_y_axis_var = tk.IntVar(value=0)  
        self.use_custom_x_var = tk.IntVar(value=0)  
        self.custom_x_axis_var = tk.IntVar(value = 0)
        self.plot_track = tk.IntVar(value= 0)

        self.dropdown_var_x1 = tk.StringVar(root)
        self.dropdown_var_x2 = tk.StringVar(root)
        self.dropdown_var_x3 = tk.StringVar(root)
        
        self.dropdown_var_x_pos = tk.StringVar(root)
        self.dropdown_var_y_pos = tk.StringVar(root)

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

        # File 3
        tk.Label(self.root, text="Rosbag 3:").grid(row=6, column=0, padx=5, pady=5)
        self.entry_file3 = tk.Entry(self.root, width=50)
        self.entry_file3.grid(row=6, column=1, padx=5, pady=5)
        dropdown3a = tk.OptionMenu(self.root, self.dropdown_var3a, "")
        dropdown3b = tk.OptionMenu(self.root, self.dropdown_var3b, "")
        tk.Button(self.root, text="Browse...", command=lambda: self.file_selector.load_file(self.entry_file3, [self.dropdown_var3a, self.dropdown_var3b], [dropdown3a, dropdown3b])).grid(row=6, column=2, padx=5, pady=5)
        dropdown3a.grid(row=7, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 1 (Top Plot):").grid(row=7, column=0, padx=5, pady=5)
        dropdown3b.grid(row=8, column=1, padx=5, pady=5)
        tk.Label(self.root, text="Topic 2 (Bottom Plot):").grid(row=8, column=0, padx=5, pady=5)

        # Shift seconds for file 1
        tk.Label(self.root, text="X-axis left-shift for Rosbags 1, 2, 3 (resp.):").grid(row=9, column=0, padx=5, pady=5)
        self.entry_shift1 = tk.Entry(self.root, width=7)
        self.entry_shift1.grid(row=10, column=0, padx=3, pady=5)
        self.entry_shift1.insert(0, "0.0")

        # Shift seconds for file 2
        # tk.Label(self.root, text="X-axis left-shift for Rosbag 2:").grid(row=10, column=0, padx=5, pady=5)
        self.entry_shift2 = tk.Entry(self.root, width=7)
        self.entry_shift2.grid(row=10, column=1, padx=3, pady=5)
        self.entry_shift2.insert(0, "0.0")
        
        # Shift seconds for file 3
        # tk.Label(self.root, text="X-axis left-shift for Rosbag 3:").grid(row=11, column=0, padx=5, pady=5)
        self.entry_shift3 = tk.Entry(self.root, width=7)
        self.entry_shift3.grid(row=10, column=2, padx=3, pady=5)
        self.entry_shift3.insert(0, "0.0")

        # Y-axis limits for Lateral Error
        tk.Label(self.root, text="Y-axis limits for Topic 1 (min, max):").grid(row=11, column=0, padx=5, pady=5)
        self.entry_y_min_1 = tk.Entry(self.root, width=10)
        self.entry_y_min_1.grid(row=11, column=1, padx=5, pady=5, sticky="W")
        self.entry_y_min_1.insert(0, "-1.0")
        self.entry_y_max_1 = tk.Entry(self.root, width=10)
        self.entry_y_max_1.grid(row=11, column=1, padx=5, pady=5, sticky="E")
        self.entry_y_max_1.insert(0, "1.0")

        # Y-axis limits for Vehicle Roll
        tk.Label(self.root, text="Y-axis limits for Topic 2 (min, max):").grid(row=12, column=0, padx=5, pady=5)
        self.entry_y_min_2 = tk.Entry(self.root, width=10)
        self.entry_y_min_2.grid(row=12, column=1, padx=5, pady=5, sticky="W")
        self.entry_y_min_2.insert(0, "-1.0")
        self.entry_y_max_2 = tk.Entry(self.root, width=10)
        self.entry_y_max_2.grid(row=12, column=1, padx=5, pady=5, sticky="E")
        self.entry_y_max_2.insert(0, "1.0")

        # Auto-format Y-axis checkbox
        tk.Checkbutton(self.root, text="Auto-scale Y-axis", variable=self.auto_y_axis_var).grid(row=13, column=1, padx=5, pady=5, sticky="W")

        # Custom Format X-axis checkbox
        tk.Checkbutton(self.root, text="Custom X-axis limits (min, max)", variable=self.custom_x_axis_var, command=self.toggle_x_axis_limit_entries).grid(row=14, column=1, padx=5, pady=5, sticky="W")

        # Use another value for X-axis checkbox
        tk.Checkbutton(self.root, text="Use another variable for X-axis for Rosbags 1, 2, 3", variable=self.use_custom_x_var, command=self.toggle_x_axis_dropdowns).grid(row=15, column=1, padx=5, pady=5, sticky="W")

        # Plot 2D Track Positions checkbox
        tk.Checkbutton(self.root, text="Plot Track Positions (Choose x,y topics)", variable=self.plot_track, command=self.toggle_x_y_dropdown).grid(row=16, column=1, padx=5, pady=5, sticky="W")

        # X-axis dropdowns (initially hidden)
        self.dropdown_x1 = tk.OptionMenu(self.root, self.dropdown_var_x1, "")
        self.dropdown_x2 = tk.OptionMenu(self.root, self.dropdown_var_x2, "")
        self.dropdown_x3 = tk.OptionMenu(self.root, self.dropdown_var_x3, "")
        self.entry_x_min = tk.Entry(self.root, width=10)
        self.entry_x_max = tk.Entry(self.root, width=10)
        self.dropdown_x_pos = tk.OptionMenu(self.root, self.dropdown_var_x_pos, "")
        self.dropdown_y_pos = tk.OptionMenu(self.root, self.dropdown_var_y_pos, "")
        self.option_menus.extend([self.dropdown_x1, self.dropdown_x2, self.dropdown_var_x3, self.entry_x_min, self.entry_x_max, self.dropdown_x_pos, self.dropdown_y_pos])
        
        # Start plotting button
        tk.Button(self.root, text="Plot Data", command=self.start_plotting).grid(row=17, column=0, columnspan=3, pady=10)

    def toggle_x_y_dropdown(self):
        if self.plot_track.get():
            self.dropdown_x_pos.grid(row=16, column=2, padx=5, pady=5)
            self.dropdown_y_pos.grid(row=16, column=3, padx=5, pady=5)
            
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_x_pos], [self.dropdown_x_pos])
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_y_pos], [self.dropdown_y_pos])
        else:
            self.dropdown_x_pos.grid_remove()
            self.dropdown_y_pos.grid_remove()       
            
    
    def toggle_x_axis_dropdowns(self):
        """Show or hide X-axis dropdowns based on checkbox."""
        if self.use_custom_x_var.get():
            self.dropdown_x1.grid(row=15, column=2, padx=5, pady=5)
            self.dropdown_x2.grid(row=15, column=3, padx=5, pady=5)
            self.dropdown_x3.grid(row=15, column=4, padx=5, pady=5)
            
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_x1], [self.dropdown_x1])
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_x2], [self.dropdown_x2])
            self.file_selector.populate_dropdown(self.entry_file1.get(), [self.dropdown_var_x3], [self.dropdown_x3])
                
        else:
            self.dropdown_x1.grid_remove()
            self.dropdown_x2.grid_remove()
            self.dropdown_x3.grid_remove()
            
    def toggle_x_axis_limit_entries(self):
        if self.custom_x_axis_var.get():
            self.entry_x_min.grid(row=14, column=2, padx=5, pady=5)
            self.entry_x_max.grid(row=14, column=3, padx=5, pady=5)        
        else:
            self.entry_x_min.grid_remove()
            self.entry_x_max.grid_remove()
            
    def start_plotting(self):
        file1_path = self.entry_file1.get()
        file2_path = self.entry_file2.get()
        file3_path = self.entry_file3.get()

        if not file1_path or not file2_path:
            messagebox.showerror("Error", "Please specify at least two CSV files.")
            return

        try:
            shift_seconds = float(self.entry_shift1.get())
            shift_seconds_2 = float(self.entry_shift2.get())
            shift_seconds_3 = float(self.entry_shift3.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid shift seconds.")
            return

        topics1 = [self.dropdown_var1a.get(), self.dropdown_var1b.get()]
        topics2 = [self.dropdown_var2a.get(), self.dropdown_var2b.get()]
        topics3 = None
        
        if file3_path:
            topics3 = [self.dropdown_var3a.get(), self.dropdown_var3b.get()]
        
         # Handle the case that user wants to auto format y-axis
        auto_y_axis = bool(self.auto_y_axis_var.get())

        # Handle the case that user wants to use custom variable for x-axis
        if self.use_custom_x_var.get():
            x_axis1 = self.dropdown_var_x1.get()
            x_axis2 = self.dropdown_var_x2.get()
            x_axis3 = self.dropdown_var_x3.get()
        else:
            x_axis1 = x_axis2 = x_axis3 = '__time'
        
        x_limits = None 
        custom_x_limits = False
        
        # Handle the case that user wants to specify x-axis limits 
        if self.custom_x_axis_var.get():
            custom_x_limits = True
            x_limits = {
                'x min and max': [float(self.entry_x_min.get()), float(self.entry_x_max.get())]
            }

        y_limits = {
            'topic 1': [float(self.entry_y_min_1.get()), float(self.entry_y_max_1.get())],
            'topic 2': [float(self.entry_y_min_2.get()), float(self.entry_y_max_2.get())]
        }

        # Handle the case that user wants to plot 2D track
        plot_track_positions = bool(self.plot_track.get())
        track_position_topics = [self.dropdown_var_x_pos.get(), self.dropdown_var_y_pos.get()]
        
        try:
            df1 = pd.read_csv(file1_path)
            df2 = pd.read_csv(file2_path)
            df3 = None
            df3_shifted = None
            if file3_path:
                df3 = pd.read_csv(file3_path)
                df3.fillna(method='ffill', inplace=True)
                df3['__time'] -= df3['__time'].min()
                df3_shifted = self.plot_manager.shift_data(df3.copy(), shift_seconds_3)

            df1.fillna(method='ffill', inplace=True)
            df2.fillna(method='ffill', inplace=True)

            df1['__time'] -= df1['__time'].min()
            df2['__time'] -= df2['__time'].min()

            df1_shifted = self.plot_manager.shift_data(df1.copy(), shift_seconds)
            df2_shifted = self.plot_manager.shift_data(df2.copy(), shift_seconds_2)

            self.plot_manager.plot_data(df1_shifted, df2_shifted, df3_shifted, topics1, topics2, topics3, x_axis1, x_axis2, x_axis3, y_lims=y_limits, x_lims=x_limits, auto_y_axis=auto_y_axis, custom_x_limits=custom_x_limits, plot_track_pos=plot_track_positions, track_pos_topics= track_position_topics)

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()
