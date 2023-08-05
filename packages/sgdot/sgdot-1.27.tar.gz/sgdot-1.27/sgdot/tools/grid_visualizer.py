import cv2
import numpy as np
import copy
from sgdot.tools.grid_optimizer import GridOptimizer
import sgdot.grids as grids

import matplotlib.pyplot as plt


# Create default Optimizer object
opt = GridOptimizer()


class GridVisualizer:
    """
    Object cpmontaining methods for visualizing Grid
    object using opencv.

    Attributes
    ----------
    link_thickness (int):
        Pixel thinkness of the links.

    nodes_size (int):
        Pixel size of the nodes circle without label.

    nodes_size_with_label (int):
        Pixel size of the nodes circle with label.

    nodes_write_label_on_nodes (boolean):
        Wether or not the label of the node should be written in node circle.

    nodes_color_household (str):
        Color of the households node circle.
        Possible colors are:
            - green
            - red
            - blue
            - light_blue
            - orange
            - black
            - white

    nodes_color_meterhub (str):
        Color of the meterhubs node marker.
        Possible colors are:
            - green
            - red
            - blue
            - light_blue
            - orange
            - black
            - white

    text_face (int):
        Text font face.

    text_margin_color (tuple):
        Background color of upper margin. In (B, G, R) format.

    text_margin_font_size (int):
        Margin text font scale.

    text_margin_font_thickness (int):
        Margin text font thickness.

    text_node_color (tuple):
        Color of text in node. In (B, G, R) format.

    text_node_font_size (int):
        Font size of node text.

    text_node_font_thickness (int):
        Thickness of node font text.

    keyboard_event_waitkey_delay (int):
        Waitkey delay for cv2.imshow function.
    """

    def __init__(self,
                 link_thickness=4,
                 nodes_size=7,
                 nodes_size_with_label=20,
                 nodes_write_label_on_nodes=False,
                 nodes_color_household="light_blue",
                 nodes_color_meterhub="orange",
                 text_face=0,
                 text_margin_color=(0, 0, 0),
                 text_margin_font_size=1,
                 text_margin_font_thickness=1,
                 text_node_color=(0, 0, 0),
                 text_node_font_size=1,
                 text_node_font_thickness=1,
                 keyboard_event_waitkey_delay=20):

        self.link_thickness = link_thickness
        self.nodes_size = nodes_size
        self.nodes_size_with_label = nodes_size_with_label
        self.nodes_write_label_on_nodes = nodes_write_label_on_nodes
        self.nodes_color_household = nodes_color_household
        self.nodes_color_meterhub = nodes_color_meterhub
        self.text_face = text_face
        self.text_margin_color = text_margin_color
        self.text_margin_font_size = text_margin_font_size
        self.text_margin_font_thickness = text_margin_font_thickness
        self.text_node_color = text_node_color
        self.text_node_font_size = text_node_font_size
        self.text_node_font_thickness = text_node_font_thickness
        self.keyboard_event_waitkey_delay = keyboard_event_waitkey_delay

    # ---------------------------- Image processing ----------------------- #

    def add_upper_margin(self, image,  upper_margin_height):
        """
        This function adds a white margin to an opencv image and returns a
        copy of it.

        Parameters
        ----------
        upper_margin_height: int
            height (in pixels) of the upper margin to be added to the image

        Returns
        -------
            New image with white margin.
        """

        # Add upper margin to the image.
        image = cv2.copyMakeBorder(image,
                                   upper_margin_height,
                                   0,
                                   0,
                                   0,
                                   cv2.BORDER_CONSTANT, None)

        # Fill in the margin with white.
        image = cv2.rectangle(image,
                              (0, 0),
                              (image.shape[1], upper_margin_height),
                              (255, 255, 255),
                              -1)

        return image

    def resize_image(self, image, image_width):
        """
        Resize image conserving image ratio and setting width.

        Parameters
        ----------
        image: :class 'numpy.ndarray'
            initial image.
        image_width: int
            image width (in pixels) that the returned image should have.

        Returns
        -------
        class 'numpy.ndarray'
            resized image.
        """
        # Resize the image.
        if image_width is None or image_width == '':
            image_width = image.shape[1]
            image = cv2.resize(
                image,
                (image_width,
                 int(image_width/image.shape[1]*image.shape[0])))
        return image

    def draw_grid(self, grid, grid_price=None):
        """
        Draws the links and the nodes of the grid on the Grid._image attribute
        as well as writes grid info in the margin.

        Parameters
        ---------
        grid: :class:`~.grids.Grid`
            Grid to be drawn on it's _image attribute.
        grid_price:
            Price of the grid that should be written in the margin.
        """

        links = grid.get_links()
        nodes = grid.get_nodes()

        # First, clear nodes and links from the grid image.
        grid.clear_image()

        # Start by drawing the links and only then draw the nodes (so that the
        # nodes are on top of the links).
        self.draw_all_links(grid)

        self.draw_all_nodes(grid)

        # Temporary variables to adjust position of text in margin.
        horizontal_origin = int(0.05 * grid.get_image().shape[1])
        vertical_origin = int(0.15 * int(0.15*grid.get_image().shape[0]))

        horizontal_space = int(0.5 * grid.get_image().shape[1])
        vertical_space = int(0.3 * int(0.15*grid.get_image().shape[0]))
        # Temporary variable containing the grid image
        temp_image = grid.get_image()
        # Clear margin.
        temp_image = cv2.rectangle(
            temp_image,
            (0, 0),
            (grid.get_initial_image().shape[1],
             int(0.15 * grid.get_initial_image().shape[0])),
            (255, 255, 255),
            -1)

        # Write number of powerhub in the margin.
        number_of_powerhubs = nodes[nodes['node_type'] == 'powerhub'].shape[0]
        temp_image = cv2.putText(temp_image,
                                 "Number of powerhubs: "
                                 + str(number_of_powerhubs),
                                 (horizontal_origin, vertical_origin),
                                 self.text_face,
                                 self.text_margin_font_size,
                                 self.text_margin_color,
                                 self.text_margin_font_thickness)

        # Write number of meterhub in the margin.
        number_of_meterhubs = nodes[nodes['node_type'] == 'meterhub'].shape[0]
        temp_image = cv2.putText(temp_image,
                                 "Number of meterhubs: "
                                 + str(number_of_meterhubs),
                                 (horizontal_origin,
                                  vertical_origin + 1 * vertical_space),
                                 self.text_face,
                                 self.text_margin_font_size,
                                 self.text_margin_color,
                                 self.text_margin_font_thickness)

        # Write number of households in the margin.
        number_of_households = nodes[nodes['node_type']
                                     == 'household'].shape[0]
        temp_image = cv2.putText(temp_image,
                                 "Number of households: "
                                 + str(number_of_households),
                                 (horizontal_origin,
                                  vertical_origin + 2 * vertical_space),
                                 self.text_face,
                                 self.text_margin_font_size,
                                 self.text_margin_color,
                                 self.text_margin_font_thickness)

        # Write total length of interhub links in the network in the margin and
        # compute total interhub cable length in meter.
        interhub_cable_lentgh_meter = np.around(
            links[links["type"] == "interhub"]["distance"].sum())
        temp_image = cv2.putText(
            temp_image,
            "interhub cable length:   " + str(int(interhub_cable_lentgh_meter))
            + ' [m]',
            (horizontal_origin + horizontal_space,
             vertical_origin),
            self.text_face,
            self.text_margin_font_size,
            self.text_margin_color,
            self.text_margin_font_thickness)
        # Write (in the margin) total length of distribution links in the
        # network.
        distribution_cable_length_meter = np.around(
            links[links["type"] == "distribution"]["distance"].sum())

        temp_image = cv2.putText(
            temp_image,
            "Distribution cable length: "
            + str(int(distribution_cable_length_meter)) + ' [m]',
            (horizontal_origin + horizontal_space,
             vertical_origin + 1 * vertical_space),
            self.text_face,
            self.text_margin_font_size,
            self.text_margin_color,
            self.text_margin_font_thickness)

        # Write down price in the margin
        if grid_price is None:
            grid_price = int(grid.price())
        if grid.price() == 999999999999999.1:
            grid_price = '-'
        temp_image = cv2.putText(temp_image,
                                 "Grid price estimate: "
                                 + str(grid_price) + ' [$]',
                                 (horizontal_origin + horizontal_space,
                                  vertical_origin + 2 * vertical_space),
                                 self.text_face,
                                 self.text_margin_font_size,
                                 self.text_margin_color,
                                 self.text_margin_font_thickness)

        grid.set_image(temp_image)

    def draw_all_links(self, grid):
        """
        Draws the links of the grid on the Grid._image attribute.

        Parameters
        ---------
        grid: :class:`~.grids.Grid`
            Grid to be drawn on it's _image attribute.
        """

        img = grid.get_image()
        nodes = grid.get_nodes()
        links = grid.get_links()
        # Only draw links if grid._links and grid._nodes are not empty.
        if nodes.shape[0] != 0 and links.shape[0]:
            # Draw a line on the image for each link.
            for index, row in links.iterrows():
                img = cv2.line(img,
                               (int(nodes["pixel_x_axis"][row["from"]]),
                                int(nodes["pixel_y_axis"][row["from"]])),
                               (int(nodes["pixel_x_axis"][row["to"]]),
                                int(nodes["pixel_y_axis"][row["to"]])),
                               self.get_color_rgb(row["type"]),
                               self.link_thickness)
        grid.set_image(img)

    def draw_all_nodes(self, grid):
        """
        Draws the nodes of the grid on the Grid._image attribute.

        Parameters
        ---------
        grid: :class:`~.grids.Grid`
            Grid to be drawn on it's __image attribute.

        Notes:
            For each node, it draws a circle on the image at the corresponding
            coordinate and writes the index of the node in the circle if
            self.nodes_write_label_on_nodes attribute is set to True.
            Nodes representing meterhubs are drawn as squares whereas nodes
            representing households are circles. Powerhubs are drawn as squared
            with red outline.
        """

        segment_counter = 0

        # Draw circle at coordinate of each households (each segment has it's
        # color) and square hubs)
        nodes = grid.get_nodes()
        img = grid.get_image()
        size_node = self.nodes_size
        if self.nodes_write_label_on_nodes is True:
            size_node = self.nodes_size_with_label
        else:
            size_node = self.nodes_size
        for segment in nodes['segment'].unique():
            for index, row in nodes[nodes['segment'] == segment].iterrows():
                if row['node_type'] == 'meterhub':
                    img = cv2.rectangle(
                        img,
                        (int(row["pixel_x_axis"]) - int(size_node * 1.2),
                         int(row["pixel_y_axis"]) - int(size_node * 1.2)),
                        (int(row["pixel_x_axis"]) + int(size_node * 1.2),
                         int(row["pixel_y_axis"]) + int(size_node * 1.2)),
                        self.get_color_rgb('red'),
                        -1)

                    img = cv2.rectangle(
                        img,
                        (int(row["pixel_x_axis"]) - size_node,
                         int(row["pixel_y_axis"]) - size_node),
                        (int(row["pixel_x_axis"]) + size_node,
                         int(row["pixel_y_axis"]) + size_node),
                        self.get_color_rgb(str(segment_counter)),
                        -1)
                elif row['node_type'] == 'powerhub':
                    img = cv2.rectangle(
                        img,
                        (int(row["pixel_x_axis"]) - int(size_node * 1.2),
                         int(row["pixel_y_axis"]) - int(size_node * 1.2)),
                        (int(row["pixel_x_axis"]) + int(size_node * 1.2),
                         int(row["pixel_y_axis"]) + int(size_node * 1.2)),
                        self.get_color_rgb('black'),
                        -1)

                    img = cv2.rectangle(
                        img,
                        (int(row["pixel_x_axis"]) - size_node,
                         int(row["pixel_y_axis"]) - size_node),
                        (int(row["pixel_x_axis"]) + size_node,
                         int(row["pixel_y_axis"]) + size_node),
                        self.get_color_rgb(str(segment_counter)),
                        -1)
                else:
                    img = cv2.circle(img,
                                     (int(row["pixel_x_axis"]),
                                      int(row["pixel_y_axis"])),
                                     size_node,
                                     self.get_color_rgb(str(segment_counter)),
                                     -1)
                # Write the label/number of the node in the middle of the
                # corresponding circle.
                if self.nodes_write_label_on_nodes is True:

                    # introduce shift variable to center text label in the
                    # middle of the nodes
                    shift = 10
                    if '1' in str(index):
                        shift = 10
                    if str(index) == '11':
                        shift = 9

                    img = cv2.putText(img,
                                      index,
                                      (int(row["pixel_x_axis"])
                                       - 10 - shift*(len(str(index))
                                                     - 1),
                                       int(row["pixel_y_axis"])+10),
                                      self.text_face,
                                      self.text_node_font_size,
                                      self.text_node_color,
                                      self.text_node_font_thickness)
            segment_counter += 1
        grid.set_image(img)

    def show(self, img, t=0, name="Grid image"):
        """
        Plots the image (using cv2.imshow).

        Parameters
        ----------
        t: int
            time (in miliseconds), during which the image should be plotted.

        Note
        ----
            If t = 0, the image is displayed until any keyboard key is pressed.
        """

        cv2.namedWindow(name, cv2.WINDOW_FREERATIO)

        cv2.imshow(name, img)
        if t <= 0:
            cv2.waitKey(0)
        else:
            cv2.waitKey(t/1000)
        cv2.destroyAllWindows()

    def plot_grid(self, grid, lentgh=15):
        fig_dim = (lentgh,
                   lentgh
                   * grid.get_image().shape[1]/grid.get_image().shape[0])
        plt.figure(figsize=fig_dim)
        plt.imshow(grid.get_image(),
                   interpolation='nearest',
                   aspect='auto')

    def plot_image(self, image, lentgh=15):
        fig_dim = (lentgh,
                   lentgh * image.shape[1]/image.shape[0])
        plt.figure(figsize=fig_dim)
        plt.imshow(image,
                   interpolation='nearest',
                   aspect='auto',
                   vmin=0, vmax=255)

    def get_color_rgb(self, color):
        """
        Helping function that returns the rgb color corresponding one of the
        predefined colors.

        Parameters
        ----------
        color: :obj:`str`
            Name of one of the predefined colors.

        Returns
        -------
            Returns the rgb code of the color given as input.

        Notes
        -----
            The predefined colors are:
            - green
            - red
            - blue
            - light_blue
            - orange
            - black
            - white

            Note that if the string given as input doesn't correspond
            to one of this colors, the returned color code will correspond
            to gray (100, 100, 100).
        """

        if color == "red" or color == "interhub":
            return (0, 0, 205)
        elif color == "green" or color == 'distribution':
            return (0, 204, 0)
        elif color == "black" or color == "bk":
            return(0, 0, 0)
        elif color == "white" or color == "w":
            return (255, 255, 255)
        elif color == "light_blue" or color == "0":
            return (255, 204, 153)
        elif color == "pink" or color == '1':
            return (178, 102, 255)
        elif color == "orange" or color == '2':
            return (45, 195, 249)
        elif color == "cream" or color == '3':
            return (204, 255, 255)
        elif color == "blue" or color == '4':
            return (255, 0, 0)
        else:
            return (100, 100, 100)   # Gray

    def transparent_grid_image(self, grid):
        """
        Returns an image of the grid (nodes and links) on a transparent
        background.

        Parameters
        ----------
        grid: :class:`~.grids.Grid`
            Grid object whose nodes and links have to be drawn on transparent
            background.

        Returns
        -------
        img_alpha: :class:`numpy.ndarray`
            grid's image (only nodes and links) on transparent background in
            RGBA.

        """

        # Create new grid and pass it grid._nodes DataFrame
        temp_grid = grids.Grid(_image_path=None,
                               _nodes=grid.get_nodes(),
                               _links=grid.get_links())
        # Set grid's image to white image of same dimension as village picture
        temp_grid.set_image(np.ones((grid.get_image().shape[0],
                                     grid.get_image().shape[1], 3)) * 253)
        # Draw links and nodes on the white image
        self.draw_all_links(temp_grid)
        self.draw_all_nodes(temp_grid)
        # Create alph channel for the temp_grid image and add it to the image
        b_channel, g_channel, r_channel = cv2.split(temp_grid.get_image())
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
        img_alpha = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        # Set all background (white) pixels to transparent in the alpha channel
        for i in range(len(img_alpha)):
            for j in range(len(img_alpha[0])):
                if img_alpha[i][j][0] == 253\
                    and img_alpha[i][j][1] == 253\
                        and img_alpha[i][j][2] == 253:
                    img_alpha[i][j][3] = 0
        return img_alpha

    # -------------- Functions for interaction with image  -------------- #

    def nothing(self, grid):
        """
        Function that returns None.
        A function is required for the Trackbar/slider callback.
        """

        return None

    def interactive_grid_plot(self, grid):
        """
        Plot the Grid._image in an interactive window and creates an additional
        window for the Trackbars/sliders (button) functionality. (See notes
        for mouse and key events)

        Parameters
        ----------
        grid: :class:`~.grids.Grid`
            Grid to be plotted.

        Notes
        -----
            The iplot is said to be interactive, since mouse and keyboard
            events enable to interact with the grid given as parameter.
            Here are the lists of mouse and keyboard events:

            Mouse events:
            - left click on the picture adds a household at the selected point.
            - right click adds a meterhub at the selected point. If the first
                node added to the grid is a hub, it will be a powerhub.

            Keyboards events:
            - 'Esc' key closes the windows.
            - 'r' key removes all nodes and links from the grid and clears the
            grid _image attribute.
            - 'c' key removes the last node that was added to the grid.

            Note that, due to the nature of the keyboard events in opencv,
            the keyboard key has to be pressed for a time corresponding to the
            waitkey_delay parameter in milliseconds
            (from self.keyboard_event_waitkey_delay) for it to be understood
            by the program.
        """

        # -------CREATE PRINCIPAL WINDOW CONTAINING THE PICTURE-------
        # Create principlal window containing the images.
        windowName = grid.get_id()
        cv2.namedWindow(windowName, cv2.WINDOW_FREERATIO)

        # ------CREATE SECONDAR WINDOW CONATINING THE TRACKBARS------

        # Create second window containing the Trackbars/sliders.
        buttonWindow = 'buttonWindow'
        cv2.namedWindow(buttonWindow)

        # Create Trackbarsliders to the buttonWindow for connecting the nodes
        # (here sliders are used instead of buttons as there are no buttons in
        # Opencv on python).

        # Add slider to the buttonWindow.
        cv2.createTrackbar('Connect nodes', buttonWindow, 1, 1, self.nothing)

        # Create temporary variable that store the status of the slider.
        Trackbar_connect_node_previous_status = 1

        # Create Trackbar/slider tot the buttonWindow for removing the last
        # node each times the slider is moved.
        # add slider to the buttonWindow
        cv2.createTrackbar('Remove last node',
                           buttonWindow, 0, 1, self.nothing)
        # Create temporary variable that store the status of the slider.
        Trackbar_remove_last_node_previous_status = 0

        # Create Trackbar/slider tot the buttonWindow for swaping the household
        # status of a randomly selected node each times the slider is moved.
        flip_random_node_node_type_trackbar_name = 'Flip random node'
        # Add slider to the buttonWindow.
        cv2.createTrackbar(flip_random_node_node_type_trackbar_name,
                           buttonWindow,
                           0,
                           1,
                           self.nothing)
        # Create temporary variable that store the status of the slider.
        Trackbar_flip_random_node_previous_status = 0

        """------SET MOUSE CALLBACKFUNCTION-------
        """
        #  Bind the callback function to window
        Trackbar_connect_node_status = cv2.getTrackbarPos('Connect nodes',
                                                          buttonWindow)
        parameter_dic = {
            'grid': grid,
            'trackbar connect nodes': Trackbar_connect_node_status}
        cv2.setMouseCallback(windowName,
                             self.draw_circle_for_MouseCallback, parameter_dic)

        opt.link_nodes(grid)
        self.draw_grid(grid)

        while(True):
            cv2.imshow(windowName, grid.get_image())

            # Update the value of the 'trackbar connect nodes' key of the dict
            # that is used in the Mouse callback function for it to know if the
            # grid needs to be linked when a node is added
            parameter_dic['trackbar connect nodes'] = \
                cv2.getTrackbarPos('Connect nodes', buttonWindow)

            """--------MANAGE TRACKBAR/SLIDER EVENTS--------
            """
            # Manage sliders events and detect if slider value changed
            # (slider having role of a button)

            # REMOVE LAST NODE TRACKBAR
            # Get value of the slider
            trackbar_remove_node_status = cv2.getTrackbarPos(
                'Remove last node',
                buttonWindow)
            # compare value of the slider with previous one, if change
            # happended, remove last node
            if Trackbar_remove_last_node_previous_status !=\
                    trackbar_remove_node_status:
                grid.clear_image()
                opt.remove_last_node(grid)
                if Trackbar_connect_node_status == 1:
                    self.draw_grid(grid)
                else:
                    self.draw_all_nodes(grid)
            Trackbar_remove_last_node_previous_status =\
                copy.deepcopy(trackbar_remove_node_status)

            # CONNECT NODES TRACKBAR
            Trackbar_connect_node_status = cv2.getTrackbarPos('Connect nodes',
                                                              buttonWindow)
            # Detect if Trackbar status changed and perform close only in this
            # case
            if Trackbar_connect_node_previous_status !=\
                    Trackbar_connect_node_status:
                grid.clear_image()
                opt.link_nodes(grid)
                if Trackbar_connect_node_status == 1:
                    self.draw_grid(grid)
                else:
                    self.draw_all_nodes(grid)
                    grid.clear_links()
                Trackbar_connect_node_previous_status =\
                    Trackbar_connect_node_status

            # FLIP RANDOM NODE TRACKBAR
                # Get value of the slider
            Trackbar_flip_random_node_status = cv2.getTrackbarPos(
                flip_random_node_node_type_trackbar_name,
                buttonWindow)
            # Compare value of the slider with previous one, if change
            # happended, remove last node
            if Trackbar_flip_random_node_previous_status !=\
                    Trackbar_flip_random_node_status:
                grid.clear_image()
                grid.flip_random_node()
                opt.link_nodes(grid)
                if Trackbar_connect_node_status == 1:
                    self.draw_grid(grid)
                else:
                    self.draw_all_nodes(grid)
            Trackbar_flip_random_node_previous_status =\
                copy.deepcopy(Trackbar_flip_random_node_status)

            """---------------KEYBORAD EVENTS-----------------"""

            # if "c" key is pressed, remove last enetered node of the list and
            # recompute the links
            if cv2.waitKey(self.keyboard_event_waitkey_delay) == 99:
                grid.clear_image()
                opt.remove_last_node(grid)
                self.draw_grid(grid)

            # if key "r" is pressed, clear grid nodes and links as well as
            # the picture
            if cv2.waitKey(self.keyboard_event_waitkey_delay) == 114:
                grid.clear_image()
                grid.clear_nodes_and_links()

            # If Esc key is pressed, break and close the image
            if cv2.waitKey(self.keyboard_event_waitkey_delay) == 27:
                grid.clear_image()
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                break

        cv2.destroyAllWindows()
        cv2.waitKey(1)

    def draw_circle_for_MouseCallback(self, event, x, y, flags, parameter_dic):
        """
        This function draws a circle on the image of a grid at the position
        given by the coordinates (x,y).

        Parameters
        ----------
        event: int
            cv2 mouseclick event.
        x : int
            The x-pixel-coordinate of the event.
        y : int
            The y-pixel-coordinate of the event.
        flags: int
            not used explicitely in the present code, the flags parameter
            is returned by the mousecallback function.
        parameter_dic: :obj:`dic`
            dictionary containing the Grid object and the status of the
            Trackbar_connected_node_status for the function to know if the
            newly computed grid has to be plotted with the links or not.
        """

        # Unfold parameter dictionnary
        grid = parameter_dic['grid']
        temp_image = grid.get_image()
        Trackbar_connect_node_status = parameter_dic['trackbar connect nodes']

        # MANAGE SINGLE LEFT CLICK EVENT
        # First detect that it is a left click
        if event == cv2.EVENT_LBUTTONDOWN:
            grid.set_image(temp_image)
            label = '0'
            while label in grid.get_nodes().index:
                label = str(int(label) + 1)
            grid.add_node(label=str(label),
                          pixel_x_axis=x,
                          pixel_y_axis=y,
                          node_type='household',
                          type_fixed=False,
                          segment='0')
            opt.link_nodes(grid)
            if Trackbar_connect_node_status == 1:
                self.draw_grid(grid)
            else:
                grid.clear_image()
                self.draw_all_nodes(grid)

        # MANAGE SINGLE RIGHT CLICK EVENT
        if event == cv2.EVENT_RBUTTONDOWN:
            grid.set_image(temp_image)
            if grid.get_nodes().shape[0] == 0:
                label = '0'
                while label in grid.get_nodes().index:
                    label = str(int(label) + 1)
                grid.add_node(label=label,
                              pixel_x_axis=x,
                              pixel_y_axis=y,
                              node_type='powerhub',
                              type_fixed=False,
                              segment='0')
            else:
                label = '0'
                while label in grid.get_nodes().index:
                    label = str(int(label) + 1)
                grid.add_node(label=label,
                              pixel_x_axis=x,
                              pixel_y_axis=y,
                              node_type='meterhub',
                              type_fixed=False,
                              segment='0')
            opt.link_nodes(grid)
            if Trackbar_connect_node_status == 1:
                self.draw_grid(grid)
            else:
                grid.clear_image()
                self.draw_all_nodes(grid)
