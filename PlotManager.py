import matplotlib.pyplot as plt

class PlotManager:
    """Data processing and plotting."""

    @staticmethod
    def shift_data(df, t):
        df['__time'] = df['__time'] - t
        df = df[df['__time'] >= 0]
        return df

    @staticmethod
    def plot_data(df1, df2, topics1, topics2, y_lims=None, auto_y_axis=False):
        for topic in topics1 + topics2:
            if topic not in df1.columns and topic not in df2.columns:
                raise ValueError(f"Topic {topic} not found in the respective CSV files.")

        fig, axs = plt.subplots(2, 1, figsize=(10, 14))

        # Plot first topic for each file
        axs[0].plot(df1['__time'], df1[topics1[0]], label=f'Rosbag 1', drawstyle='default')
        axs[0].plot(df2['__time'], df2[topics2[0]], label=f'Rosbag 2', drawstyle='default')
        axs[0].set_xlabel('Time [s]')
        axs[0].set_ylabel(topics1[0])
        axs[0].legend()
        if not auto_y_axis and y_lims and 'lateral_error' in y_lims:
            axs[0].set_ylim(y_lims['lateral_error'])
        # axs[0].set_title('First Topic Comparison')

        # Plot second topic for each file
        axs[1].plot(df1['__time'], df1[topics1[1]], label=f'Rosbag 1', drawstyle='default')
        axs[1].plot(df2['__time'], df2[topics2[1]], label=f'Rosbag 2', drawstyle='default')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel(topics2[1])
        axs[1].legend()
        if not auto_y_axis and y_lims and 'other' in y_lims:
            axs[1].set_ylim(y_lims['other'])
        # axs[1].set_title('Second Topic Comparison')

        plt.tight_layout()
        plt.show()