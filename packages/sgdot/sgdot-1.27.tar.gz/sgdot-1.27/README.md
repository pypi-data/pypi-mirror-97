**SG-DOT**

SGDOT is a Package created to help design and optimize the network
topology for swarm-grids. It uses satellite imagery of villages to be
electrified and enables designing and optimizing a grid with a tree-star
configuration.

The grids module containes the Grid class. A grid essentially contains two
DataFrames representing the nodes and the links composing the network as well as
a set of attributes representing the price of the grid's components.
The nodes represent houses to be connected to the grid and the links represent
wires connecting pairs of houses together. There is a price associated with
each link and node. The price of a Grid is the sum of the prices of each
nodes and links.

The tools sub-package contains the **grid_optimizer, grid_visualizer, io** and **plot** modules.

- The **grid_optimizer** modules encapsulates GridOptimizer class which contains methods for optimizing a Grid object.
- The **grid_visualizer** modules encapsulates GridVisualizer class which contains methods for visualise a Grid object using opencv.
- The **io** module contains functions to handle files.
- The **plot** module enables to display the grid object in a 2D plot as well as displaying the plot of the results of the optimizations
