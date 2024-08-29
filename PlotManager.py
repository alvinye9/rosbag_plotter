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
        self.track_plot = None
        self.track_position_points = []
        self.track_pos_topics = None

    @staticmethod
    def shift_data(df, t):
        df['__time'] = df['__time'] - t
        df = df[df['__time'] >= 0]
        return df

    def plot_data(self, df1, df2, df3, topics1, topics2, topics3, x_axis1, x_axis2, x_axis3, y_lims=None, x_lims=None, auto_y_axis=False, custom_x_limits=False, plot_track_pos=False, track_pos_topics=None):
        #topics 1 is all the data for file 1
        
        self.df1 = df1
        self.df2 = df2
        self.topics1 = topics1
        self.topics2 = topics2
        self.topics3 = topics3
        self.x_axis1 = x_axis1
        self.x_axis2 = x_axis2
        self.x_axis3 = x_axis3
        self.track_pos_topics = track_pos_topics

        if plot_track_pos:
            self.figure, self.axs = plt.subplots(3, 1, figsize=(8, 12))
        else:
            self.figure, self.axs = plt.subplots(2, 1, figsize=(8, 8))

        # Plot first topic for each file
        self.axs[0].plot(df1[x_axis1], df1[topics1[0]], label=f'Rosbag 1', drawstyle='default')
        self.axs[0].plot(df2[x_axis2], df2[topics2[0]], label=f'Rosbag 2', drawstyle='default', linestyle='--')
        if df3 is not None:
            self.axs[0].plot(df3[x_axis3], df3[topics3[0]], label=f'Rosbag 3', drawstyle='default', linestyle=':')
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
        if df3 is not None:
            self.axs[1].plot(df3[x_axis3], df3[topics3[1]], label=f'Rosbag 3', drawstyle='default', linestyle=':')
        self.axs[1].set_xlabel(x_axis1)
        self.axs[1].set_ylabel(topics2[1])
        self.axs[1].legend()
        if not auto_y_axis and y_lims and 'topic 2' in y_lims:
            self.axs[1].set_ylim(y_lims['topic 2'])
        if custom_x_limits and x_lims and 'x min and max' in x_lims:
            self.axs[1].set_xlim(x_lims['x min and max'])

        # Plot track positions if the option is selected
        if plot_track_pos:
            x_pos_topic, y_pos_topic = track_pos_topics
            self.track_plot = self.axs[2]
            self.track_plot.plot(df1[x_pos_topic], df1[y_pos_topic], label=f'Track Position Rosbag 1', linestyle='-', color='b')
            self.track_plot.plot(df2[x_pos_topic], df2[y_pos_topic], label=f'Track Position Rosbag 2', linestyle='--', color='g')
            self.track_plot.set_xlabel('X Position')
            self.track_plot.set_ylabel('Y Position')
            self.track_plot.legend()

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

        # Clear previous track position points
        for point in self.track_position_points:
            point.remove()
        self.track_position_points.clear()

        # Get the closest index in the x data to the slider value
        idx1 = (self.df1[self.x_axis1] - val).abs().idxmin()
        idx2 = (self.df2[self.x_axis2] - val).abs().idxmin()
        idx3 = (self.df3[self.x_axis3] - val).abs().idxmin()

        # Plot the points on the respective plots and store the references
        point1a, = self.axs[0].plot(self.df1[self.x_axis1].iloc[idx1], self.df1[self.topics1[0]].iloc[idx1], 'ro')
        point2a, = self.axs[0].plot(self.df2[self.x_axis2].iloc[idx2], self.df2[self.topics2[0]].iloc[idx2], 'ro')
        point3a, = self.axs[0].plot(self.df3[self.x_axis3].iloc[idx3], self.df2[self.topics3[0]].iloc[idx3], 'ro')

        point1b, = self.axs[1].plot(self.df1[self.x_axis1].iloc[idx1], self.df1[self.topics1[1]].iloc[idx1], 'ro')
        point2b, = self.axs[1].plot(self.df2[self.x_axis2].iloc[idx2], self.df2[self.topics2[1]].iloc[idx2], 'ro')
        point3b, = self.axs[1].plot(self.df3[self.x_axis3].iloc[idx3], self.df3[self.topics3[1]].iloc[idx3], 'ro')

        # Store the points so they can be removed next time
        self.point_plots.extend([point1a, point2a, point3a, point1b, point2b, point3b])

        # Plot the track position if applicable
        if self.track_plot is not None and self.track_pos_topics is not None:
            self.track_plot.set_aspect('equal')
            x_pos_topic, y_pos_topic = self.track_pos_topics
            track_point1, = self.track_plot.plot(self.df1[x_pos_topic].iloc[idx1], self.df1[y_pos_topic].iloc[idx1], 'ro')
            track_point2, = self.track_plot.plot(self.df2[x_pos_topic].iloc[idx2], self.df2[y_pos_topic].iloc[idx2], 'ro')
            self.track_position_points.extend([track_point1, track_point2])
            

        self.figure.canvas.draw_idle()
