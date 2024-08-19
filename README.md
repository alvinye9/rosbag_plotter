## About The Project

Originally built for Purdue AI Racing but can be used for easy plotting of csv data exported from plotjuggler.
This GUI can handle non-time-series plots as well as multiple line plots for easy data comparison.

## Prerequisites

To utilize this app, you must have csv data exported from plotjuggler in the following steps:

1. Install and learn the fundamentals of plotjuggler [here](https://facontidavide.github.io/PlotJuggler/index.html)
2. Import rosbag data and select the following topics:
   - Desired y-axis values (up to 2 currently)
   - Desired x-axis values (if not time-series)
3. Check the box next to "CSV Exporter"
4. Repeat steps 1-4 with another rosbag if you plan to compare (up to 2 currently) datasets 

## Usage
This will launch the GUI
  ```sh
  python3 RosbagPlotterApp.py
  ```
1. Utilize the "Browse" buttons to load in both .csv datasets
2. After selecting the datasets, the dropdowns will populate for both desired topics of comparison. You can leave Topic 2 empty if you wish to have a single plot instead of a 2x1 set of plots.
3. (optional) Specify values to offset the x-axis of either plot.
4. (optional) Specify y-axis limits or check the box to allow matplotlib to auto-format them
5. (optional) You can check the "Use Another Value for X-axis" box to specify just that, by default it is a time-series plot
