import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class PlotManager:
    """Data processing and plotting."""
    
    def __init__(self):
        self.figure = None
        self.axs = None
        self.slider = None
        self.df1 = None
        self.df2 = None
        self.topics1 = None
        self.topics2 = None
        self.x_axis1 = None
        self.x_axis2 = None
        self.point_plots = []

    @staticmethod
    def shift_data(df, t):
        df['__time'] = df['__time'] - t
        df = df[df['__time'] >= 0]
        return df

    def plot_data(self, df1, df2, topics1, topics2, x_axis1, x_axis2, y_lims=None, x_lims=None, auto_y_axis=False, custom_x_limits=False):
        self.df1 = df1
        self.df2 = df2
        self.topics1 = topics1
        self.topics2 = topics2
        self.x_axis1 = x_axis1
        self.x_axis2 = x_axis2
        for topic in topics1 + topics2:
            if topic not in df1.columns and topic not in df2.columns:
                raise ValueError(f"Topic {topic} not found in the respective CSV files.")

        # Create a new figure and axes
        self.figure, self.axs = plt.subplots(2, 1, figsize=(10, 14))

        # Plot first topic for each file
        self.axs[0].plot(df1[x_axis1], df1[topics1[0]], label=f'Rosbag 1', drawstyle='default')
        self.axs[0].plot(df2[x_axis2], df2[topics2[0]], label=f'Rosbag 2', drawstyle='default', linestyle='--')
        self.axs[0].set_xlabel(x_axis1)
        self.axs[0].set_ylabel(topics1[0])
        self.axs[0].legend()
        if not auto_y_axis and y_lims and 'topic 1' in y_lims:
            self.axs[0].set_ylim(y_lims['topic 1'])
        if custom_x_limits and x_lims and 'x min and max' in x_lims:
            self.axs[0].set_xlim(x_lims['x min and max'])

        # Plot second topic for each file
        self.axs[1].plot(df1[x_axis1], df1[topics1[1]], label=f'Rosbag 1', drawstyle='default')
        self.axs[1].plot(df2[x_axis2], df2[topics2[1]], label=f'Rosbag 2', drawstyle='default', linestyle='--')
        self.axs[1].set_xlabel(x_axis1)
        self.axs[1].set_ylabel(topics2[1])
        self.axs[1].legend()
        if not auto_y_axis and y_lims and 'topic 2' in y_lims:
            self.axs[1].set_ylim(y_lims['topic 2'])
        if custom_x_limits and x_lims and 'x min and max' in x_lims:
            self.axs[1].set_xlim(x_lims['x min and max'])

        # Add a slider for x-axis control
        self.add_slider(df1[x_axis1])

        plt.tight_layout()
        plt.show()

    def add_slider(self, x_data):
        """Add a slider to control the x-axis."""
        # Define slider position and size
        ax_slider = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')

        # Create the slider with a range based on x_data
        self.slider = Slider(ax_slider, 'X-Axis', min(x_data), max(x_data), valinit=min(x_data))

        # Update the plot when the slider is moved
        self.slider.on_changed(self.update_plot_with_point)

    def update_plot_with_point(self, val):
        """Plot a point at the slider's x value."""
        # Clear previous points by removing them from the axes
        for point in self.point_plots:
            point.remove()
        self.point_plots.clear()

        # Get the closest index in the x data to the slider value
        idx1 = (self.df1[self.x_axis1] - val).abs().idxmin()
        idx2 = (self.df2[self.x_axis2] - val).abs().idxmin()

        # Plot the points on the respective plots and store the references
        point1a, = self.axs[0].plot(self.df1[self.x_axis1].iloc[idx1], self.df1[self.topics1[0]].iloc[idx1], 'ro')
        point2a, = self.axs[0].plot(self.df2[self.x_axis2].iloc[idx2], self.df2[self.topics2[0]].iloc[idx2], 'ro')

        point1b, = self.axs[1].plot(self.df1[self.x_axis1].iloc[idx1], self.df1[self.topics1[1]].iloc[idx1], 'ro')
        point2b, = self.axs[1].plot(self.df2[self.x_axis2].iloc[idx2], self.df2[self.topics2[1]].iloc[idx2], 'ro')

        # Store the points so they can be removed next time
        self.point_plots.extend([point1a, point2a, point1b, point2b])

        self.figure.canvas.draw_idle()



# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button

# class PlotManager:
#     """Data processing and plotting."""
#     def __init__(self):
#         self.figure = plt.Figure(figsize=(10, 14))
#         self.slider = None

#     def add_slider(self, ax, x_data):
#         """Add a slider to control the x-axis."""
#         # Define slider position and size
#         ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')

#         # Create the slider with range based on x_data
#         self.slider = Slider(ax_slider, 'X-Axis', min(x_data), max(x_data), valinit=min(x_data))

#         # Update the plot when the slider is moved
#         self.slider.on_changed(lambda val: self.update_x_axis(ax, val))

#     def update_x_axis(self, ax, val):
#         """Update the x-axis limits based on the slider value."""
#         ax.set_xlim([val, val + (ax.get_xlim()[1] - ax.get_xlim()[0])])
#         plt.draw()
        
#     @staticmethod
#     def shift_data(df, t):
#         df['__time'] = df['__time'] - t
#         df = df[df['__time'] >= 0]
#         return df

#     @staticmethod
#     def plot_data(df1, df2, topics1, topics2, x_axis1, x_axis2, y_lims=None, x_lims = None, auto_y_axis=False, custom_x_limits = False):
#         for topic in topics1 + topics2:
#             if topic not in df1.columns and topic not in df2.columns:
#                 raise ValueError(f"Topic {topic} not found in the respective CSV files.")

#         fig, axs = plt.subplots(2, 1, figsize=(10, 14))

#         # Plot first topic for each file
#         axs[0].plot(df1[x_axis1], df1[topics1[0]], label=f'Rosbag 1', drawstyle='default')
#         axs[0].plot(df2[x_axis2], df2[topics2[0]], label=f'Rosbag 2', drawstyle='default', linestyle='--')
#         axs[0].set_xlabel(x_axis1)
#         axs[0].set_ylabel(topics1[0])
#         axs[0].legend()
#         if not auto_y_axis and y_lims and 'topic 1' in y_lims:
#             axs[0].set_ylim(y_lims['topic 1'])
#         # axs[0].set_title('First Topic Comparison')

#         if custom_x_limits and x_lims and 'x min and max' in x_lims:
#             axs[1].set_xlim(x_lims['x min and max'])
        
#         # Plot second topic for each file
#         axs[1].plot(df1[x_axis1], df1[topics1[1]], label=f'Rosbag 1', drawstyle='default')
#         axs[1].plot(df2[x_axis2], df2[topics2[1]], label=f'Rosbag 2', drawstyle='default', linestyle='--')
#         axs[1].set_xlabel(x_axis1)
#         axs[1].set_ylabel(topics2[1])
#         axs[1].legend()
#         if not auto_y_axis and y_lims and 'topic 2' in y_lims:
#             axs[1].set_ylim(y_lims['topic 2'])
#         # axs[1].set_title('Second Topic Comparison')

#         plt.tight_layout()
#         plt.show()
        