
import cv2
import numpy as np
import pandas as pd
import random
import math
import os
import copy
import time
import statistics
import json
from munkres import Munkres
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from pulp import LpMinimize, LpProblem, LpVariable
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from multiprocessing import Pool

import sgdot.tools.io as io
import sgdot.tools.visualization as visu
import sgdot.tools.plot as plot

from shutil import copyfile


# ------------ CONNECT NODES USING TREE-STAR SHAPE ------------#


def link_nodes(grid, mst_algorithm="Prim's"):
    """
    This function create links between the nodes of the grid:
    it creates a link bewteen each household and the nearest meterhub
    (or using an allocation algorithm for capacitated hubs) and
    connect all meterhub together using Prim's minimum spanning tree
    method.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object

    mst_algorithm: str
        Algorithm to be used to compute the minimum spanning tree
        Possible values are:
            - "Prim's"
            - "Kruskal"
    """

    # First, clear links dataframe
    grid.clear_links()
    grid_allocation_capacity = grid.get_hubs()['allocation_capacity'].sum()
    if not grid.is_hub_capacity_constraint_too_strong() and\
            grid_allocation_capacity > 0:
        link_households_to_capacitated_hubs(
            grid)
    else:
        link_households_to_nereast_hubs(grid)

    link_hubs(grid, mst_algorithm)


# ------------ MINIMUM SPANNING TREE ALGORITHM ------------ #

def link_hubs(grid, mst_algorithm):
    """
    This  function creates links between all meterhubs following
    Prim's or Kruskal minimum spanning tree method depending on the
    mst_algorithm value.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object

    mst_algorithm: str
        Algorithm to be used to compute the minimum spanning tree
        Possible values are:
            - "Prim's"
            - "Kruskal"
    """
    if mst_algorithm == "Prims":
        link_hubs_using_MST_Prims(grid)
    elif mst_algorithm == "Kruskal":
        link_hubs_using_MST_Kruskal(grid)
    else:
        raise Exception("Invalid value provided for mst_algorithm.")


def link_hubs_using_MST_Prims(grid):
    """
    This  method creates links between all meterhubs following
    Prim's minimum spanning tree method. The idea goes as follow:
    a first node is selected and it is connected to the nearest neighbour,
    together they compose the a so-called forest. Then a loop
    runs over all node of the forest, the node that is the closest to
    the forest without being part of it is added to the forest and
    connected to the node of the forest it is the closest to.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object whose hubs shall be connected.
    """

    # create list to keep track of nodes that have already been added
    # to the forest

    for segment in grid.get_hubs()['segment'].unique():
        # Create dataframe containing the hubs from the segment
        # and add temporary column to keep track of wheter the
        # hub has already been added to the forest or not
        hubs = grid.get_hubs()[grid.get_hubs()['segment'] == segment]
        hubs['in_forest'] = [False] * hubs.shape[0]

        # Makes sure that there are at least two meterhubs in segment
        if hubs[- (hubs['in_forest'])].shape[0] > 0:
            # First, pick one meterhub and add it to the forest by
            # setting its value in 'in_forest' to True
            index_first_forest_meterhub =\
                hubs[- hubs['in_forest']].index[0]
            hubs.at[index_first_forest_meterhub, 'in_forest'] = True

            # while there are hubs not connected to the forest,
            # find nereast hub to the forest and connect it to the forest
            count = 0         # safety parameter to avoid staying stuck in loop
            while len(hubs[- hubs['in_forest']]) and\
                    count < hubs.shape[0]:

                # create variables to compare hubs distances and store best
                # candidates
                shortest_dist_to_meterhub_outside_forest =\
                    grid.distance_between_nodes(
                        hubs[hubs['in_forest']].index[0],
                        hubs[- hubs['in_forest']].index[0])
                index_closest_hub_in_forest = hubs[hubs['in_forest']].index[0]
                index_closest_hub_to_forest =\
                    hubs[- hubs['in_forest']].index[0]

                # Iterate over all hubs within the forest and over all the
                # ones outside of the forest and find shortest distance
                for index_hub_in_forest, row_forest_hub in\
                        hubs[hubs['in_forest']].iterrows():
                    for index_hub_outside_forest, row_hub_outside_forest in\
                            hubs[- hubs['in_forest']].iterrows():
                        if grid.distance_between_nodes(
                                index_hub_in_forest,
                                index_hub_outside_forest)\
                                <= shortest_dist_to_meterhub_outside_forest:
                            index_closest_hub_in_forest = index_hub_in_forest
                            index_closest_hub_to_forest =\
                                index_hub_outside_forest
                            shortest_dist_to_meterhub_outside_forest =\
                                grid.distance_between_nodes(
                                    index_closest_hub_in_forest,
                                    index_closest_hub_to_forest)
                # create a link between hub pair
                grid.add_link(index_closest_hub_in_forest,
                              index_closest_hub_to_forest)
                hubs.at[index_closest_hub_to_forest, 'in_forest'] = True
                count += 1


def link_hubs_using_MST_Kruskal(grid):
    """
    This  method creates links between all meterhubs following
    Kruskal's minimum spanning tree method from scpicy.sparse.csgraph.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object whose hubs shall be connected
    """

    # iterate over all segments and connect hubs using MST
    for segment in grid.get_hubs()['segment'].unique():
        hubs = grid.get_hubs()[grid.get_hubs()['segment'] == segment]

        # configure input matrix for calling csr_matrix function
        X = np.zeros((hubs.shape[0], hubs.shape[0]))
        for i in range(hubs.shape[0]):
            for j in range(hubs.shape[0]):
                if i > j:
                    index_node_i = hubs.index[i]
                    index_node_j = hubs.index[j]

                    X[j][i] = grid.distance_between_nodes(index_node_i,
                                                          index_node_j)
        M = csr_matrix(X)

        # run minimum_spanning_tree_function
        Tcsr = minimum_spanning_tree(M)
        A = Tcsr.toarray().astype(float)

        # Read output matrix and create corresponding links to grid
        for i in range(len(hubs.index)):
            for j in range(len(hubs.index)):
                if i > j:
                    if A[j][i] > 0:
                        index_node_i = hubs.index[i]
                        index_node_j = hubs.index[j]

                        grid.add_link(index_node_i, index_node_j)

# ------------------- ALLOCATION ALGORITHMS -------------------#


def link_households_to_nereast_hubs(grid):
    """
    This function create a link between each household
    and the nereast meterhub of the same segment.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.
    """

    # Iterate over all segment containing hubs
    for segment in grid.get_hubs()['segment'].unique():
        # Iterate over all households and connect each of them
        # to the closest meterhub or powerhub in the segment
        for index_node, row_node in\
                grid.get_households()[
                    grid.get_households()['segment']
                    == segment].iterrows():
            # This variable is a temporary variable that is used to find
            # the nearest meter hub to a node
            index_closest_meterhub =\
                grid.get_hubs()[grid.get_hubs()['segment']
                                == segment].index[0]
            shortest_dist_to_meterhub =\
                grid.distance_between_nodes(index_node,
                                            index_closest_meterhub)
            for index_meterhub, row_meterhub in\
                    grid.get_hubs()[grid.get_hubs()['segment']
                                    == segment].iterrows():
                # Store which meterhub is the clostest and what the
                # distance to it is
                if grid.distance_between_nodes(index_node, index_meterhub)\
                        < shortest_dist_to_meterhub:
                    shortest_dist_to_meterhub =\
                        grid.distance_between_nodes(index_node,
                                                    index_meterhub)
                    index_closest_meterhub = index_meterhub
            # Finally add the link to the grid
            grid.add_link(index_node, index_closest_meterhub)


def link_households_to_capacitated_hubs(grid):
    """
    This function assigns each household of a grid to a hub
    of the same segment taking into consideration the maximum
    capacity of the hub and minimizing the overall distribution
    line length. It is based on the Munkres algorithm from the munkres
    module.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.

    hub_capacity: int
        Maximum number of households that can be assigned to each hub.
    """

    for segment in grid.get_hubs()['segment'].unique():
        hubs_in_segment = grid.get_hubs()[grid.get_hubs()['segment']
                                          == segment]
        households_in_segment = grid.get_households()[
            grid.get_households()['segment']
            == segment]
        num_households = households_in_segment.shape[0]
        segment_hub_capacity = grid.get_segment_hub_capacity(segment)

        # if the hub capacity is too strong of a constraint to connect
        # all the households to the grid
        if segment_hub_capacity < num_households:
            raise Exception('hub capacity only allows '
                            + str(segment_hub_capacity)
                            + ' households to be connected to hubs of segment '
                            + str(segment) + ', but there are '
                            + str(num_households)
                            + ' households in the segment')
        else:
            # Create matrix containing the distances between the
            # households and the hus
            distance_matrix = []
            index_list = []
            for hub in hubs_in_segment.index:
                for allocation_slot in range(grid.get_hubs()[
                        'allocation_capacity'][hub]):
                    distance_list = [
                        grid.distance_between_nodes(hub, household)
                        for household in households_in_segment.index]
                    distance_list.extend([0] * (segment_hub_capacity
                                                - num_households))
                    distance_matrix.append(distance_list)
                    index_list.append(hub)
            # Call munkres_sol function for solveing allocation problem
            munkres_sol = Munkres()
            indices = munkres_sol.compute(distance_matrix)
            # Add corresponding links to the grid
            for x in indices:
                if x[1] < households_in_segment.shape[0]:
                    grid.add_link(
                        index_list[x[0]],
                        households_in_segment.index[int(x[1])])


# --------------------- SEGMENTATION ---------------------#

def propagate_segment_to_neighbours(grid, index, segment):
    """
    This function  is a helping function used to split a segment into two.
    It is a recursice function that sets the segment of a node to a given
    value and then does the same for all of it's neighbours that have a
    different segment index. The recursion starts at the node corresponding
    to the index given as parameter.

    Parameters
    ----------
    index: str
        index of the node the function should change the segment index.

    segment: str
        index (label) of the segment to be set for the nodes.

    """
    for index_neighbour in grid.get_links()[(grid.get_links()['from']
                                             == index)]['to']:
        if not grid.get_nodes()['segment'][index_neighbour] == segment:
            grid.set_segment(index_neighbour, segment)
            propagate_segment_to_neighbours(grid,
                                            index_neighbour,
                                            segment)
    for index_neighbour in grid.get_links()[(grid.get_links()['to']
                                             == index)]['from']:
        if not grid.get_nodes()['segment'][index_neighbour] == segment:
            grid.set_segment(index_neighbour, segment)
            propagate_segment_to_neighbours(grid,
                                            index_neighbour,
                                            segment)


def split_segment(grid, segment, min_segment_size, mst_algorithm="Prim's"):
    """
    This function splits a grid segment into two segments of size at least
    min_segment_size.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.

    segment: str
        Index of the segment to be split.

    min_segment_size: int
        Minimum allowed size of the two parts of the segments after split.

    mst_algorithm: str
        Algorithm to be used to compute the minimum spanning tree
        Possible values are:
            - "Prim's"
            - "Kruskal"

    Notes
    -----
        The current function performs temporary modifications to the grid
        nodes in order to connect all the nodes of the initial segment
        with a minimum spanning tree to see what is the longest node from
        the tree that can be removed, thus splitting the segment into two
        sub-segments of respective size at least min_segment_size. Once the
        segmentation is identified, the nodes are restored to their initial
        state and the segmentation is performed by setting the 'segment'
        property of the node to the ones identified earlier
    """
    # make sure that segment index matches a node segment
    if segment not in grid.get_nodes()['segment'].unique():
        raise Warning(
            "the segment index doesn't correspond to any grid segment")
        return

    # make sure that the initial segment is big enough to be split into
    # two subsegments of size at least min_segment_size
    if grid.get_nodes()[grid.get_nodes()['segment']
                        == segment].shape[0] < 2 * min_segment_size:
        return

    # Store grid's nodes in dataframe since the actual grid is modified during
    # function
    node_backup = grid.get_nodes()
    # filter nodes to keep only the ones belongging to the initial segment
    grid.set_nodes(grid.get_nodes()[grid.get_nodes()['segment']
                                    == segment])
    # changes all nodes into meterhubs
    grid.set_all_node_type_to_meterhubs()
    # Connect the nodes using MST
    grid.clear_links()

    link_hubs(grid, mst_algorithm)

    # Create list containing links index sorted by link's distance
    index_link_sorted_by_distance = [
        index for index in grid.get_links()[
            'distance'
        ].nlargest(grid.get_links().shape[0]).index]
    # Try to split the segment removing the longest link and see if
    # resulting sub-segments meet the minimum size criterion, if not,
    # try with next links (the ones just smaller) until criterion meet

    for link in index_link_sorted_by_distance:
        index_node_from = grid.get_links()['from'][link]
        index_node_to = grid.get_links()['to'][link]
        old_segment = grid.get_nodes()['segment'][index_node_from]
        segment_1 = grid.get_nodes()['segment'][index_node_from]
        segment_2 = grid.get_nodes()['segment'][index_node_to] + '_2'
        grid.set_segment(index_node_from, segment_2)
        grid.set_segment(index_node_to, segment_2)

        propagate_segment_to_neighbours(grid, index_node_to, segment_2)
        grid.set_segment(index_node_from, segment_1)

        if grid.get_nodes()[
                grid.get_nodes()['segment']
                == segment_1].shape[0] >= min_segment_size\
                and grid.get_nodes()[
                    grid.get_nodes()['segment']
                    == segment_2].shape[0] >= min_segment_size:
            break
        else:
            for node_label in grid.get_nodes().index:
                grid.set_segment(node_label, old_segment)

    segment_dict = {index: grid.get_nodes()['segment'][index]
                    for index in grid.get_nodes().index}

    grid.set_nodes(node_backup)
    for index in segment_dict:
        grid.set_segment(index, segment_dict[index])


def k_means_cluster_centers(grid, k_number_of_clusters):
    """
    This function uses a k-means clustering algorithm from sklearn
    to find the coordinates of the point corresponding to the
    center of the cluster centers on a grid object.

    Pamameters
    ----------
        grid: :class:`~.grids.Grid`
            Grid object
        k_number_of_cluster: int
            Defines the k-value for the k-means clustering.
            It gives the number of cluster to be considered.
    Output
    ------
        numpy.ndarray
        Array containing the coordinates of the cluster centers.
        Suppose there are two cluster with centers at respectively
        coordinates (x_1, y_1) and (x_2, y_2), the output arroy would
        look like
            array([
                   [x_1, y_1],
                   [x_2 , y_2]
                  ])
    """

    node_coord = []

    for node, row in grid.get_nodes().iterrows():
        node_coord.append([row['pixel_x_axis'], row['pixel_y_axis']])

    features, true_labels = make_blobs(
        n_samples=200,
        centers=3,
        cluster_std=2.75,
        random_state=42)

    features = node_coord
    kmeans = KMeans(
        init="random",
        n_clusters=k_number_of_clusters,
        n_init=10,
        max_iter=300,
        random_state=42)

    kmeans.fit(features)

    return kmeans.cluster_centers_


def set_k_means_configuration(grid, number_of_hubs):
    """
    This function modifies the grid given as input and set it's nodes
    so that the hub location correspond to the clostest node to the
    centers of the k-means clustering algorithm where k corresponds to
    number_of_hubs.

    Parameter
    ---------
    grid: :class:`~.grids.Grid`
        Grid the function is considering for computing the price.
    """

    nr_optimization(grid,
                    number_of_hubs=number_of_hubs,
                    number_of_relaxation_step=0,
                    first_guess_strategy='k_means',
                    save_output=False,
                    output_folder=None,
                    save_image=False,
                    save_opt_video=False,
                    plot_arrow_in_video=False,
                    plot_price_evolution=False,
                    print_progress_bar=False)


def get_expected_hub_number_from_k_means(grid):
    """
    This function computes the grid price of the configuration
    obtained using the k-means clustering algorithm from nr_optimization
    for different number of hubs. The function returns the
    number of hubs corresponding to the least price.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid the function considers for computing the price.

    Output
    ------
    type: float
        The function returns a float corresponding to the expected number
        of hubs minimizing the grid price.

    Notes
    -----
    The function assumes that the price of the configuration obtained using the
    k-means clustering algorithm as a function of the price is a striclty
    concave function. The function explores the prices associated with
    different number in both increasing and decreasing direction and
    stop 3 steps after the last minimum found.
    """

    # make a copy of grid and perform changes and grid copy
    grid_copy = copy.deepcopy(grid)

    # Set all node types to household
    for node_with_fixed_type in grid_copy.get_nodes().index:
        grid_copy.set_type_fixed(node_with_fixed_type, False)
    grid_copy.set_all_node_type_to_households()

    price_per_number_hub_df = pd.DataFrame()

    # start computing the price starting with a number of hubs
    # corresponding to a fifteenth of the number of nodes in the grid.
    num_nodes = grid_copy.get_nodes().shape[0]

    set_k_means_configuration(grid_copy, max(1, int(num_nodes / 10)))

    # initialize DataFrame to store number of hubs and according price
    price_per_number_hub_df = pd.DataFrame({"#hubs": [],
                                            "price": []})
    price_per_number_hub_df = price_per_number_hub_df.set_index("#hubs")

    price_per_number_hub_df.loc[
        f"{grid_copy.get_hubs().shape[0]}"] = grid_copy.price()

    # Create variable that is used to compare price corresponding to
    # different number of hubs
    tmp_price = grid_copy.price()

    # initialize counter to limit exploration of solution space to range
    # and avoid exploring number of hubs for increasing prices
    counter = 0

    # explore range with decreasing hub number and stop 3 steps after last
    # minimum found
    while (grid_copy.price() <= tmp_price
            or counter < 3) and grid_copy.get_hubs().shape[0] > 1:
        tmp_price = grid_copy.price()

        number_of_hubs = grid_copy.get_hubs().shape[0] - 1

        set_k_means_configuration(grid_copy, number_of_hubs)

        price_per_number_hub_df.loc[
            f"{grid_copy.get_hubs().shape[0]}"] = grid_copy.price()

        if grid_copy.price() > tmp_price:
            counter += 1
        else:
            counter = 0

    # identify number of hub corresponding to lowest price and explore
    # prices for higher number of hubs is a similar fashion
    min_price = price_per_number_hub_df['price'].min()

    min_index = price_per_number_hub_df[
        price_per_number_hub_df['price'] == min_price].index[0]

    number_of_hubs = int(min_index)
    counter = 0
    tmp_price = grid_copy.price() + 1
    grid_price = grid_copy.price()

    while grid_price < tmp_price or counter < 3:
        tmp_price = grid_price

        # only recompute k-means for new number of hubs
        number_of_hubs = number_of_hubs + 1
        if str(number_of_hubs) in price_per_number_hub_df.index:
            grid_price = price_per_number_hub_df['price'][
                str(number_of_hubs)]
        else:
            set_k_means_configuration(grid_copy, number_of_hubs)
            grid_price = grid_copy.price()

            price_per_number_hub_df.loc[f"{number_of_hubs}"] = grid_price

        if grid_price >= tmp_price:
            counter += 1
        else:
            counter = 0

    min_price = price_per_number_hub_df['price'].min()

    min_index = price_per_number_hub_df[
        price_per_number_hub_df['price'] == min_price].index[0]

    return int(min_index)


# -----------------------REMOVE NODE-------------------------#


def remove_last_node(grid):
    """
    Removes the last node added to a grid.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object
    """
    if grid.get_nodes().shape[0] > 0:
        grid.set_nodes(grid.get_nodes().drop(grid.get_nodes().index[-1]))
        if not grid.is_hub_capacity_constraint_too_strong():
            link_nodes(grid)


# -------------- MAKE GRID COMPLIANT WITH CONSTRAINTS -------------- #


def flip_households_until_hub_capacity_constraint_met(grid):
    """
    This function is ment to be called when the hub capacity constraint
    is too restrictive for the nodes. The function flips the node type of
    households until there are enough hubs in each segment to meet the hub
    capacity constraint.

    Returns
    ---------
    """

    if grid.get_default_hub_capacity() > 0:

        if grid.get_hubs().shape[0] == 0:
            grid.flip_random_node()

        if grid.is_hub_capacity_constraint_too_strong():
            for segment in grid.get_nodes()['segment'].unique():
                while grid.get_households()[grid.get_households()['segment']
                                            == segment].shape[0]\
                        > grid.get_segment_hub_capacity(segment):
                    random_number = np.random.rand()
                    num_households = grid.get_households()[
                        grid.get_households()['segment'] == segment].shape[0]
                    grid.flip_node(
                        grid.get_households()[grid.get_households()
                                              == segment].index[
                                                  int(random_number
                                                      * num_households)])

# ----------------------- GENETIC ALGORITHM -----------------------#

# Main GA function


def ga_optimization(grid,
                    number_of_hubs='unspecified',
                    output_folder=None,
                    print_progress_bar=True,
                    save_output=True,
                    save_image=True,
                    plot_price=True,
                    number_of_generations=None,
                    population_size=None,
                    mutation_probability=None,
                    mutation_type_ratio=None,
                    number_of_elites=None,
                    number_of_survivors=None,
                    crossover_type=None,
                    parent_selection=None,
                    include_input_grid_as_chromosome=False,
                    initialization_strategy='random',
                    delta=None,
                    number_of_processors_for_parallelization=4,
                    runtime=3600):
    """
    This function uses the Genetic Algorithm method to find
    find the location of hubs and cables minimizing the price function.
    All the algorithm parameters are taken from the confi_alo.cfg config file.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.

    number_of_hubs: int
        Number of hubs in the grid the algorithm should consider.
        Default value is 'unspecified', meaning that the chromosomes
        can have different size (corresponding to grid with different
        number of hub). In this case, the size of the chromosome is determined
        using a normal distribution centered using the expected number of hubs
        n* obtained by the k-means clustering method.

    output_folder: str
        Path of the folder the grid output of the algorithm should be saved in.

    print_progress_bar: :obj:`bool`
        If True, the progress is displayed in the console.

    save_output: :obj:`bool`
        If True, the output (grid and population dataframe) are saved in
        output folder.

    save_image: :obj:`bool`
        If True and save_output also True, saves an image of the grid in the
        output folder.

    plot_price: :obj:`bool`
        If True, a plot of the grid is displayed in the console.

    number_of_generations: int
        Determines how many generations the GA should run for.

    population_size: int
        Determines the number of trial solutions in each iteration.

    mutation_probability: float (in [0, 1])
        Determines the chance of each gene in each individual solution
        to be replaced by a random value.

    mutation_type_ratio: float (in [0, 1])
        Determines the average ratio of mutations that consist on replacing
        a hub over mutations adding or removing a hub.
        For mutation_type_ratio = 0.5, on average, half of the mutation
        selected will be replacing mutations. A forth of the mutation will
        corespond to adding a hub and the last forth to removing a hub.
        For mutation_type_ratio = 1, all the mutations are mutations
        replacing hub indices.

    number_of_elites: int
        Determines the number of elites surviving in the population.
        The elites are the fittest chromosomes from each generation.
        They are copied to the next generation.

    number_of_survivors: int
        Determines the number of chromosomes that are not elites and will
        will survive to the next generation. They are randomly selected
        chromosomes of a given generation (elites excluded) and are copied
        to the next generation.

    crossover_type: str
        Determines the type of crossover (i.e. how the genes are transmitted
        from the parents to the offsprings).
        Possibilities are:
            - 'uniform': mix the genes from the parents at random and
            distributes among the offsprings.
            - 'neighbor_pair':
                        each hub (gene) from parent1 is allocated to a hub from
                        parent2 to form pairs that minimize the distance
                        between the hub of the pairs. For each pair, the hub
                        from parent1 will be passed to the offsrping1 with
                        probaility 50% and to offspring2 with the same
                        probability. The other hub from the pair is passed
                        to the other offspring.

    parent_selection: str
        Determines how parent chromosomes are being picked.
        Possibilites are:
            - 'linear_rank_selection': parent with rank k is picked with
                                       probability N-k+1)/S where N is the
                                       population size and S the sum of the
                                       first N natural numbers.

    include_input_grid_as_chromosome: bool
        Determines if the chromosome corresponding to the grid given as input
        is part of the chromosomes of the first generation.

    initialization_strategy: str
        Determines how the instances of the initial population are generated.
        Options are:
        - 'random':
            Initial population is generated at random except for first
            chromosome that corresponds to the configuration of the input grid
            if applicable.
        - 'NR':
            The chromosomes of the initial population are obtained calling the
            nr_optimization function on randomly generated initial grids.

    delta: float in [0, 1]
        This patameter is used to obtain the value of the standard deviation
        considered for determining the number of hubs in the chromosomes of
        the initial population. The standard deviation sigma is computed as
        follow:  sigma = n* / delta
                where n* is the expected number of hubs in the network computed
                using the function get_expected_hub_number_from_k_means().

    number_of_processors_for_parallelization: int
        Determines how many processors should be used in parallel for the
        concerned of the algorithm. The multiprocessing is done using
        the Pool function from the multiprocessing library.

    runtime: float
        Time is second after which no new generation step will start.
        The algorithm stops after and returns the fittest chromosome found.


    Notes
    -----

    Parent selection
        The parent selection is made using rank selection, if there are N
        chromosomes, the nth chromosome in term of fitness has chance (N-n+1)/S
        where S = n(n+1) / 2 is the sum of the N first natural numbers.
        For example for N = 5, we have S = 15 and the first chromosome has
        chance 5/15, to be picked, second 4/15 and so on.
    """
    # make sure that the number_of_processors_for_parallelization is valid
    # argument
    if number_of_processors_for_parallelization not in range(1, 1000):
        raise Exception("number_of_processors_for_parallelization "
                        + "should be a strictly positive integer")
    # Copy grid to use it to get grid's corresponding chromosome
    grid_copy = copy.deepcopy(grid)
    # Store number of fixed hubs in grid
    number_of_fixed_hubs = grid.get_hubs()[grid.get_hubs()['type_fixed']
                                           ].shape[0]

    # Ensure that number of nodes is positive integer, if not release
    # constraint by setting it to 'unspecified'
    if type(number_of_hubs) != int:
        number_of_hubs = 'unspecified'
    elif number_of_hubs <= 0:
        number_of_hubs = 'unspecified'

    if number_of_hubs != 'unspecified':
        # Ensure that the grid containing number_of_hubs hubs
        # can be connected (i.e. that the capacitated hub constraint
        # allows connecting the grid). Since there might be some hubs
        # with fixed type and capacity different from default hub capacity,
        # set all non-fixed nodes to households and flip some of them until
        # number of hub corresponds to number_of_hubs
        grid.set_all_node_type_to_households()
        while grid.get_hubs().shape[0] < number_of_hubs:
            grid.flip_node(grid.get_households().index[0])
        if grid.is_hub_capacity_constraint_too_strong():
            raise Exception('number_of_hubs is too small to allow grid to be'
                            + ' connected while respecting hub capacity')

    # Take actual time to monitor duration of algo
    start_time = time.time()

    # Read config_grid and config_algo parameters for undefinded parameters
    config_grid = ConfigParser()
    config_grid.read('config/config_grid.cfg')

    config_algo = ConfigParser()
    config_algo.read('config/config_algo.cfg')

    # Import all algorithm parameters that are not None from config_algo.cfg
    if number_of_generations is None:
        number_of_generations = config_algo.getint('GA',
                                                   'number_of_generations')
    if population_size is None:
        population_size = config_algo.getint('GA', 'population_size')
    if mutation_probability is None:
        mutation_probability = config_algo.getfloat('GA',
                                                    'mutation_probability')
    if mutation_type_ratio is None:
        mutation_type_ratio = config_algo.getfloat('GA',

                                                   'mutation_type_ratio')
    if number_of_elites is None:
        number_of_elites = config_algo.getint('GA', 'number_of_elites')
    if number_of_survivors is None:
        number_of_survivors = config_algo.getint('GA', 'number_of_survivors')
    if crossover_type is None:
        crossover_type = config_algo.get('GA', 'crossover_type')

    if parent_selection is None:
        parent_selection = config_algo.get('GA', 'parent_selection')

    if delta is None:
        delta = config_algo.getint('GA', 'delta')

    default_hub_capacity = config_grid.getint('constraints',
                                              'default_hub_capacity')

    if print_progress_bar:
        print(f"|{42 * '_'}| GENETIC ALOGRITHM |{42 * '_'}|\n")
        print(f"{35 * ' '}population size:       {population_size}")
        print(f"{35 * ' '}number of generations: {number_of_generations}")
        print(f"{35 * ' '}mutation_probability:  {mutation_probability}")
        print(f"{35 * ' '}mutation_type_ratio:   {mutation_type_ratio}")
        print(f"{35 * ' '}number_of_elites:      {number_of_elites}")
        print(f"{35 * ' '}number_of_survivors:   {number_of_survivors}")
        print(f"{35 * ' '}crossover_type:        {crossover_type}")
        print(f"{35 * ' '}runtime:               {runtime}\n\n")

        print("\rInitializing algorithm...", end="\r")

    # setup parameters for normal distribution used to determine number of
    # hubs in chromosomes of initial population
    fixed_capacity = grid.get_hubs()[
        grid.get_hubs()['type_fixed']]['allocation_capacity'].sum()

    if number_of_hubs == 'unspecified':
        if grid.get_total_hub_capacity() == 0:
            print("\rDetermining expected hub number...", end="")
            mu = max(1, get_expected_hub_number_from_k_means(grid))
            print(f'mu: {mu}, delta: {delta}')
            sigma = mu / delta
            min_threshold = 1
        else:
            mu = max(1, ((grid.get_nodes().shape[0] - fixed_capacity)
                         / default_hub_capacity))
            sigma = mu / delta
            min_threshold = np.ceil((grid.get_nodes().shape[0]
                                     - fixed_capacity)
                                    / default_hub_capacity)
    else:
        mu = max(1, number_of_hubs)
        sigma = 0
        min_threshold = 1

    if print_progress_bar:
        print("\rCreating initial population...", end="")
    if initialization_strategy == 'random':
        # If input grid fullfils criterion for hub capacity,
        # add the chromosome corresponding to input grid to initial population
        if(((not grid_copy.is_hub_capacity_constraint_too_strong()
             and grid_copy.get_hubs().shape[0] == number_of_hubs)
            or number_of_hubs == 'unspecified')
                and include_input_grid_as_chromosome):
            # Create random intital chromosomes
            initial_chromosomes = [ga_get_chromosome_from_grid(grid_copy)]
            counter = 0
            while (len(initial_chromosomes) < population_size):
                new_chromosome = sorted(list(np.random.choice(
                    grid_copy.get_non_fixed_nodes().index,
                    size=(
                                        ga_truncated_normal_distribution_draw(
                                            mu,
                                            sigma,
                                            min_threshold)
                                        - number_of_fixed_hubs),
                    replace=False)), key=int)

                # Add the chromosome corresponding to the input grid
                if (new_chromosome not in initial_chromosomes
                        or counter > population_size**2):
                    initial_chromosomes.append(new_chromosome)
                counter += 1

        else:
            # Create random intital chromosomes
            initial_chromosomes = [sorted(list(np.random.choice(
                grid.get_non_fixed_nodes().index,
                size=(
                    ga_truncated_normal_distribution_draw(
                        mu,
                        sigma,
                        min_threshold)
                    - number_of_fixed_hubs),
                replace=False)), key=int)
                for x in range(population_size)]

        with Pool(number_of_processors_for_parallelization) as p:
            fitness = p.starmap(
                ga_fitness_function,
                [(grid, chromosome) for chromosome in initial_chromosomes])

    elif initialization_strategy == 'NR':
        fitness = []
        initial_chromosomes = []
        for first_guess_strategy in (['k_means']
                                     + ['random'] * (population_size - 1)):
            nr_optimization(grid=grid,
                            number_of_hubs=number_of_hubs,
                            number_of_relaxation_step=5,
                            damping_factor=0.5,
                            weight_of_attraction='constant',
                            first_guess_strategy=first_guess_strategy,
                            save_output=False,
                            number_of_steps_bewteen_random_shifts=0,
                            output_folder=None,
                            save_opt_video=False,
                            plot_arrow_in_video=False,
                            plot_price_evolution=False,
                            print_progress_bar=False)
            initial_chromosomes.append(ga_get_chromosome_from_grid(grid))
            fitness.append(- grid.price())

    population_df = pd.DataFrame({'chromosome': initial_chromosomes,
                                  'price': [-x for x in fitness],
                                  'fitness': fitness,
                                  'relative_fitness': fitness,
                                  'generation': pd.Series([0] * len(fitness),
                                                          dtype=int),
                                  'rank_in_generation': pd.Series(
                                      [0] * len(fitness), dtype=int),
                                  'role': pd.Series(['initial_population']
                                                    * len(fitness),
                                                    dtype=str),
                                  'birth_time': time.time() - start_time,
                                  'parents': pd.Series(['-'] * len(fitness),
                                                       dtype=str)
                                  })
    # compute relative_fitness
    lowest_fitness_in_generation = population_df['fitness'].min()
    for index, row in population_df.iterrows():
        population_df.loc[index, 'relative_fitness'] -=\
            lowest_fitness_in_generation
    # Add ranking according to fitness
    for chromosome_iter in range(population_size):
        population_df.at[
            population_df[population_df['generation'] == 0].sort_values(
                by=['fitness'], ascending=False).index[chromosome_iter],
            'rank_in_generation'] = chromosome_iter + 1

    for generation in range(1, number_of_generations + 1):
        # exit loop if current runtime exeeds runtime
        if time.time() - start_time > runtime:
            break

        if print_progress_bar:
            display_progress_bar(current=generation - 1,
                                 final=number_of_generations,
                                 message=f" generation: {generation}")
        potential_parents = population_df[population_df['generation']
                                          == generation - 1].copy()

        elites = potential_parents.sort_values(
            by='fitness',
            ascending=False)[:number_of_elites].copy()

        # Copy elites to current generation
        for index, row in elites.iterrows():
            elites.loc[index, 'generation'] = generation
            elites.loc[index, 'relative_fitness'] = 0
            elites.loc[index, 'rank_in_generation'] = 0
            elites.loc[index, 'role'] = 'elite'
        population_df = population_df.append(elites, ignore_index=True)

        # Copy randomly selected parents to current generation (avoiding elits)
        survivors = (potential_parents.sort_values(
            by='fitness',
            ascending=False)[number_of_elites:]
        ).sample(n=number_of_survivors,
                 random_state=1).copy()

        for index, row in survivors.iterrows():
            survivors.loc[index, 'generation'] = generation
            survivors.loc[index, 'relative_fitness'] = 0
            survivors.loc[index, 'rank_in_generation'] = 0
            survivors.loc[index, 'role'] = 'survivor'
            # mutate surviving parent
            if np.random.rand() < mutation_probability:
                if number_of_hubs == 'unspecified':
                    survivors.loc[index, 'chromosome'] =\
                        ga_random_mutation(
                        grid=grid,
                        chromosome=survivors.loc[index, 'chromosome'],
                        mutation_type_ratio=mutation_type_ratio)
                else:
                    survivors.loc[index, 'chromosome'] = ga_gene_swap(
                        grid,
                        survivors.loc[index, 'chromosome'])
            survivors.loc[index, 'fitness'] = ga_fitness_function(
                grid,
                survivors.loc[index, 'chromosome'])
            survivors.loc[index, 'price'] = - survivors.loc[index, 'fitness']

        population_df = population_df.append(survivors.copy(),
                                             ignore_index=True)

        # Select parent pairs for crossovers
        if parent_selection == 'linear_rank_selection':
            index_weighted_list = []
            for chromosome_index in population_df[population_df['generation']
                                                  == generation - 1].index:
                for rank in range(
                    population_size + 1
                    - population_df['rank_in_generation'][
                        chromosome_index]):
                    index_weighted_list.append(
                        population_df['chromosome'][chromosome_index])
            random.shuffle(index_weighted_list)
        else:
            raise Exception("invalid parent_selection")

        # Create list of parent pairs chosen

        # First ensure that there is more than one distinct chromosome in
        # index_weighted_list. In such a case, all parents will be the
        # same chromosome.
        if len([index for index in index_weighted_list
                if index != index_weighted_list[0]]) == 0:
            a_parents = [index_weighted_list[0]] * (
                population_size
                - number_of_elites
                - number_of_survivors)
            b_parents = a_parents
        # Otherwise, choose two different chromosomes to form parent pairs
        else:
            a_parents = [random.choice(index_weighted_list)
                         for i in range(int(np.ceil((
                                        population_size
                                        - number_of_elites
                                        - number_of_survivors)/2)))]

            b_parents = [random.choice(
                [index for index in index_weighted_list
                 if index != a])
                for a in a_parents]
        parent_pairs = [[a, b] for a, b in zip(a_parents, b_parents)]

        offspring_pairs = [ga_crossover(grid=grid,
                                        parent1=pair[0],
                                        parent2=pair[1],
                                        crossover_type=crossover_type)
                           for pair in parent_pairs]

        offsprings = [offspring for offsprings_pair in offspring_pairs
                      for offspring in offsprings_pair]
        # mutate offspings
        if number_of_hubs == 'undefined':
            offsprings = [ga_random_mutation(grid=grid,
                                             chromosome=chromosome,
                                             mutation_type_ratio=mutation_type_ratio)
                          for chromosome in offsprings]
        else:
            offsprings = [ga_gene_swap(grid, chromosome)
                          for chromosome in offsprings]

        with Pool(number_of_processors_for_parallelization) as p:
            fitness_offsprings = p.starmap(
                ga_fitness_function,
                [(grid, chromosome) for chromosome in offsprings])

        # Add offsprings to population_df with respective fitness and with
        # its parents. (the double comprehension list is required to format
        # the parent list so that it matches with the offspring list)
        counter = 1
        current_time = time.time() - start_time
        for offspring, fitness, parents in zip(
                offsprings,
                fitness_offsprings,
                [parent for pair in [[parent_pair, parent_pair]
                                     for parent_pair in parent_pairs]
                 for parent in pair]):
            counter += 1

            population_df.loc[len(population_df)] =\
                [offspring,                  # chromosomes (genes)
                 -fitness,                   # grid price (= -fitness)
                 fitness,                    # fitness
                 0,                          # relative_fitness unknown
                 generation,                 # generation
                 0,                          # rank_in_generation unknown
                 'offspring',                # role
                 current_time,               # birth_time
                 f'({parents[0]}, {parents[1]})']  # parents

        # In case the population size went beyond the population_size
        # parameter, remove less fit chromosomes

        if population_df[population_df['generation']
                         == generation].shape[0] > population_size:
            population_df = population_df.drop(
                population_df[population_df['generation']
                              == generation].sort_values(
                    by='fitness',
                    ascending=False).index[-1],
                axis=0)
        # Compute relative_fitness of new generation chromosomes

        lowest_fitness_in_generation =\
            population_df[population_df['generation']
                          == generation]['fitness'].min()

        for index, row in population_df[population_df['generation']
                                        == generation].iterrows():
            population_df.loc[index, 'relative_fitness'] =\
                population_df.loc[index, 'fitness'] - \
                lowest_fitness_in_generation
            population_df.loc[index, 'birth_time'] = current_time

        # Compute rank_in_generation of new generation chromosomes
        for chromosome_iter in range(population_size):
            population_df.at[
                population_df[population_df['generation']
                              == generation].sort_values(
                    by=['fitness'],
                    ascending=False
                ).index[chromosome_iter],
                'rank_in_generation'] = chromosome_iter + 1

    if time.time() - start_time > runtime:
        message = "max runtime exeeded"
    else:
        message = ""
    display_progress_bar(current=1,
                         final=1,
                         message=message)

    index_fitter_chromosome = population_df.sort_values(
        by='price',
        ascending=True).index[0]
    fitter_chromosome = population_df['chromosome'][index_fitter_chromosome]
    price_grid_fitter_chromosome =\
        population_df['price'][index_fitter_chromosome]
    grid.set_all_node_type_to_households()
    for index in fitter_chromosome:
        grid.set_node_type(index, 'meterhub')
    print(f'\n\nBest chromosome found:\n{fitter_chromosome}\n')
    print(f'Price of corresponding grid: {price_grid_fitter_chromosome} $\n\n')

    if plot_price:
        plot.plot_price_evolution_for_ga_run(population_df)

    if save_output:
        if output_folder is None:
            # Create output folder if not already existing
            output_folder = f'data/output/{grid.get_id()}/GA'

        io.make_folder(output_folder)

        run_name = (grid.get_id()
                    + f'_pop{population_size}_gen{number_of_generations}')
        if os.path.exists(output_folder + '/' + run_name):
            counter = 1
            while os.path.exists(f'{output_folder}/{run_name}_{counter}'):
                counter += 1
            run_name = f'{run_name}_{counter}'
        path = f'{output_folder}/{run_name}'
        io.make_folder(path)

        copyfile(
            './config/config_algo.cfg', path + '/config_algo.cfg')
        copyfile(
            './config/config_grid.cfg', path + '/config_grid.cfg')
        population_df.to_csv(path + '/population.csv')
        link_nodes(grid)
        visu.draw_grid(grid)
        io.export_grid(grid=grid,
                       folder=output_folder,
                       backup_name=run_name,
                       save_image=save_image,
                       allow_saving_in_existing_backup_folder=True)
        # create json file containing about dictionary

        about_dict = {
            'grid id': grid.get_id(),
            'number_of_hubs': number_of_hubs,
            'output_folder': output_folder,
            'print_progress_bar': print_progress_bar,
            'save_output': save_output,
            'plot_price': plot_price,
            'number_of_generations': number_of_generations,
            'population_size': population_size,
            'mutation_probability': mutation_probability,
            'number_of_elites': number_of_elites,
            'number_of_survivors': number_of_survivors,
            'crossover_type': crossover_type,
            'parent_selection': parent_selection,
            'initialization_strategy': initialization_strategy
        }

        json.dumps(about_dict)

        with open(output_folder + '/' + run_name + '/about_run.json',
                  'w') as about:
            about.write(json.dumps(about_dict))


def ga_get_offsprings_with_fitness(grid, parents):
    """
    This function returns a dictionary containing two offsprings chromomsomes
    and their respective fitness. This function is used for the parallelization
    of the ga_optimization.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know
        compute the fitness of the offsprings.

    parents: list
        List of two parents chromosomes. A chromosomes being a list of hub
        str indices.
    """
    offsprings = ga_crossover(grid, parents[0], parents[1], 'neighbor_pair')
    return {'offspring1': offsprings[0],
            'offsrping2': offsprings[1],
            'fitness_offspring1': ga_fitness_function(grid, offsprings[0]),
            'fitness_offspring2': ga_fitness_function(grid, offsprings[1])}

# GA gene mutation function


def ga_remove_gene(grid, chromosome):
    """
    This function removes a gene from a chromosome. A chromosome being a list
    with hub indices, the function just removes a hub index picked at random
    from the chromosome

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know what
        the indices of the new hub can be.
    chromosome: obj:`list`
        List of indices corresponding to the node that are non-fixed meterhubs.
        A chromosome is an instance of a population of the GA.

    Return
    ------
    list
        Chromosome with one hub index less.

    Note
    ----
        If removing a node from the grid would lead to too few hubs to link
        the nodes, the function does nothing.
    """
    if len(chromosome) > 1:
        config_grid = ConfigParser()
        config_grid.read('config/config_grid.cfg')

        default_hub_capacity = config_grid.getint('constraints',
                                                  'default_hub_capacity')
        chromosome_copy = chromosome
        fixed_hubs = grid.get_hubs()[grid.get_hubs()['type_fixed']]
        fixed_allocation_capacity = fixed_hubs['allocation_capacity'].sum()
        if default_hub_capacity == 0:
            if len(chromosome) > 1:
                chromosome_copy.pop(random.randrange(len(chromosome_copy)))

        else:
            if (fixed_allocation_capacity + (len(chromosome_copy) - 1)
                * default_hub_capacity)\
                    >= grid.get_nodes().shape[0] - (fixed_hubs.shape[0]
                                                    + len(chromosome_copy)
                                                    - 1):
                chromosome_copy.pop(random.randrange(len(chromosome_copy)))
            else:
                warning_message = "Impossible to remove gene from chromosome, "
                warning_message += "resulting chromosome would have too little"
                warning_message += " hubs for connecting the node"
                raise Warning(warning_message)
        return chromosome_copy
    else:
        return chromosome


def ga_append_gene(grid, chromosome):
    """
    This function adds a gene to a chromosome. A chromosome being a list
    with hub indices, the function just appends a new hub index to the
    chromosome$.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know what
        the indices of the new hub can be.
    chromosome: obj:`list`
        List of indices corresponding to the node that are non-fixed meterhubs.
        A chromosome is an instance of a population of the GA.

    Return
    ------
    list
        chromosome with additional hub index
    """

    chromosome_copy = chromosome
    possible_new_hub_index = [x for x in grid.get_non_fixed_nodes().index
                              if x not in chromosome]
    chromosome_copy.append(random.choice(possible_new_hub_index))
    if chromosome_copy is None:
        print('ga_append_gene returned None chromosome')
    return chromosome_copy


def ga_gene_swap(grid, chromosome):
    """
    This function mutates a chromosome gene (i.e. changes one of the hub
    position) corresponding to the grid given as parameter.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know what
        the indices of the new hub can be.
     chromosome: obj:`list`
        List of indices corresponding to the node that are non-fixed meterhubs.
        A chromosome is an instance of a population of the GA.

    Output
    ------
    obj:`list`
        New chromosome.

    Notes
    -----
        The function is selecting one of the genes (i.e. elements from the
        chromosome list) and changes the index for one of the index of
        the nodes that is not yet part of genes (elements )from the chromosome.
    """

    if len(chromosome) > 0:
        # Select list index of the gene to be modified
        randomly_selected_gene_number =\
            np.random.choice(range(len(chromosome)))
        # Get list of possible candidates for new hub index
        list_of_possible_new_hubs = [
            index for index in grid.get_non_fixed_nodes().index
            if index not in chromosome]

        # Pick one of the hub indices
        new_hub_index = np.random.choice(list_of_possible_new_hubs)

        chromosome_copy = copy.deepcopy(chromosome)
        # replace gene
        chromosome_copy[randomly_selected_gene_number] = new_hub_index

        # reorder genes
        chromosome_copy = sorted(chromosome_copy, key=int)

        return chromosome_copy

    else:
        raise Warning(
            f"Invalid chromosome {chromosome} for ga_gene_swap function")


def ga_random_mutation(grid, chromosome, mutation_type_ratio):
    """
    This function performs one of the three chromosome mutation
    (remove a gene, append a gene or mutate a gene) on the chromosome
    by calling one of the three following function selected at random
    taking into consideration the mutation_type_ratio:
    ga_remove_gene, ga_append_gene or ga_gene_swap.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know what
        the indices of the new hub can be.

    chromosome: obj:`list`
        List of indices corresponding to the node that are non-fixed meterhubs.
        A chromosome is an instance of a population of the GA.

    mutation_type_ratio: float (in [0, 1])
        Determines the average ratio of mutations that consist on replacing
        a hub over mutations adding or removing a hub.
        For mutation_type_ratio = 0.5, on average, half of the mutation
        selected will be replacing mutations. A forth of the mutation will
        corespond to adding a hub and the last forth to removing a hub.
        For mutation_type_ratio = 1, all the mutations are mutations
        replacing hub indices.
    Return
    ------
        list
            Returnes the mutated chromosome.
    """
    # Three mutation_types considered
    # 'replace hub' -> Mutation replacing a hun index
    # 'add hub'     -> Mutation adding a hun index
    # 'remove hub'  -> Mutation removing a hun index

    if np.random.rand() < mutation_type_ratio:
        mutation_chosen = 'replace hub'
    else:
        if np.random.rand() < 0.5:
            mutation_chosen = 'add hub'
        else:
            mutation_chosen = 'remove hub'

    chromosome_copy = copy.deepcopy(chromosome)

    if mutation_chosen == 'remove hub':
        config_grid = ConfigParser()
        config_grid.read('config/config_grid.cfg')

        default_hub_capacity = config_grid.getint('constraints',
                                                  'default_hub_capacity')

        fixed_hubs = grid.get_hubs()[grid.get_hubs()['type_fixed']]
        fixed_allocation_capacity =\
            grid.get_hubs()[
                grid.get_hubs()['type_fixed']]['allocation_capacity'].sum()
        if default_hub_capacity == 0:
            if len(chromosome_copy) > 1:
                return ga_remove_gene(grid, chromosome_copy)
            else:
                return chromosome_copy
        elif (fixed_allocation_capacity + (len(chromosome_copy) - 1)
              * default_hub_capacity)\
                >= grid.get_nodes().shape[0] - (fixed_hubs.shape[0]
                                                + len(chromosome_copy)
                                                - 1):
            return ga_remove_gene(grid, chromosome_copy)
        else:
            return chromosome_copy

    elif mutation_chosen == 'add hub':
        return ga_append_gene(grid, chromosome_copy)

    elif mutation_chosen == 'replace hub':
        return ga_gene_swap(grid, chromosome_copy)


def ga_crossover(grid, parent1, parent2, crossover_type='uniform'):
    """
    This function mixes the genes of two parents and returns
    a list constaining the two offspring (children) according
    to the crossover_type parameter.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object. This parameter is required for the function to know what
        the indices of the new hub can be.

    parent1: list
        First parent for crossover. List of indices of hubs in a grid.

    parent2: list
        Second parent for crossover. List of indices of hubs in a grid.

    crossover_type: str
        Specifies the type of crossover.
        Currently implemented crossover types
        are:
            - 'uniform':
                        for each gene, flip a coin, to decide if the gene
                        of the first (resp. second) parent should be transmitted
                        to the first (resp. second) offspring or if gene of first
                        (resp. second) parent should be transmitted to second
                        (resp. first) offspring.
            - 'neighbor_pair':
                        each hub (gene) from parent1 is allocated to a hub from
                        parent2 to form pairs that minimize the distance
                        between the hub of the pairs. For each pair, the hub
                        from parent1 will be passed to the offsrping1 with
                        probaility 50% and to offspring2 with the same
                        probability. The other hub from the pair is passed
                        to the other offspring.

    Return:
        List constaining the two offspring chromosomes.
    """
    # UNIFORM CROSSOVER
    if crossover_type == 'uniform':
        # Identify genes that are common to parent1 and parent2 and pass
        # those genes to offsprings
        common_genes = [gene for gene in parent1
                        if gene in parent1 and gene in parent2]
        offspring1 = common_genes.copy()
        offspring2 = common_genes.copy()

        remaining_genes_to_pass_parent_1 = [gene for gene in parent1
                                            if gene not in common_genes]
        remaining_genes_to_pass_parent_2 = [gene for gene in parent2
                                            if gene not in common_genes]
        remaining_genes_to_pass = (remaining_genes_to_pass_parent_1
                                   + remaining_genes_to_pass_parent_2)

        offspring1 += list(np.random.permutation(
            remaining_genes_to_pass
        )[:len(remaining_genes_to_pass_parent_1)])
        offspring2 += [x for x in remaining_genes_to_pass
                       if x not in offspring1]
        try:
            return[sorted(offspring1, key=int), sorted(offspring2, key=int)]
        except ValueError:
            return[sorted(offspring1), sorted(offspring2)]

    # SELECTION FROM NEIGHBOR PAIRS
    elif crossover_type == 'neighbor_pair':
        # set parent1 to parent chromosome with the most number of genes
        if len(parent1) < len(parent2):
            parent1, parent2 = parent2, parent1

        # Create matrix with distance between hubs from parent1 and parent2
        distance_matrix = []
        for hub_parent1 in parent1:
            distance_matrix.append([grid.distance_between_nodes(
                                    hub_parent1,
                                    hub_parent2) for hub_parent2 in parent2])
        munkres_sol = Munkres()
        indices = munkres_sol.compute(distance_matrix)

        # pass genes from pairs to the offsprings
        neighbor_pairs =\
            [[parent1[index[0]], parent2[index[1]]] for index in indices]

        offspring1, offspring2 = [], []
        for pair in neighbor_pairs:
            if np.random.rand() < 0.5:
                offspring1.append(pair[0])
                offspring2.append(pair[1])
            else:
                offspring1.append(pair[1])
                offspring2.append(pair[0])

        # The lonely_hubs list is a list of all the hubs that are not
        # part of a pair
        lonely_hubs = [hub for hub in parent1 + parent2
                       if hub not in (offspring1 + offspring2)]

        # Distribute the lonely hubs to the offspring uniformly at random
        for hub in lonely_hubs:
            if np.random.rand() < 0.5:
                offspring1.append(hub)
            else:
                offspring2.append(hub)

        try:
            return [sorted(offspring1, key=int), sorted(offspring2, key=int)]
        except ValueError:
            return [sorted(offspring1), sorted(offspring2)]

# GA Fitness function


def ga_fitness_function(grid, chromosome):
    """
    This function computes the fitness of the chromosome
    for the grid given as parameter. The fitness correspond to minus the
    price of the grid (with hubs located at position given by the chromosome
    parameter).

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.

    chromosome: obj:`list`
        List of indices corresponding to the node that should be set to
        'meterhub'. All other nodes will have node type 'household'.
    """

    # Import parameters from config_grid.cfg and config_algo.cfg
    config_grid = ConfigParser()
    config_grid.read('config/config_grid.cfg')

    config_algo = ConfigParser()
    config_algo.read('config/config_algo.cfg')

    # Set all node types to household
    grid.set_all_node_type_to_households()

    # Loop over the genes (elements) of the chromosome (list) and set type
    # of given nodes to meterhub
    for hub_index in chromosome:
        grid.set_node_type(hub_index, 'meterhub')

    # now link nodes
    link_nodes(grid)

    return - grid.price()


# GA progress bar


def ga_printProgressBar(iteration,
                        total,
                        prefix='',
                        suffix='',
                        generation=0,
                        decimals=1,
                        length=100,
                        fill='█',
                        printEnd="\r"):
    """
    Call in a loop to create terminal progress bar.

    Parameters
    ----------
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent
                                  complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

        Notes
        -----
            Funtion inspired from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/30740258 # noqa: E501
    """
    if iteration > total:
        iteration = total
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}, generation: {generation}',
          end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

# Other functions GA


def ga_get_chromosome_from_grid(grid):
    """
    This function returns a chromosome for the genetic algorithm corresponding
    to the hub indices of the grid given as parameter.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object

    Return
    ------
    obj: :`list`
        chromosome corresponding to the grid (list with indices of hubs with
        type_fixed equal False)
    """

    chromosome = [index for index in grid.get_hubs().index
                  if not grid.get_hubs()['type_fixed'][index]]

    return chromosome


def ga_truncated_normal_distribution_draw(mu, sigma, min_threshold):
    """
    This function returns a draw of a normal distribution bigger
    or equal to min_threshold.

    Parameters
    ----------
    mu: float
        Expectation value of normal law
    sigma: float
        Standard deviation of normal distribution
    min_treshold: float
        Minimum value returned by the function, if value drwan is  smaller,
        pick another one
    """
    draw = - np.infty
    if mu <= 0 or sigma < 0:
        raise Warning("ga_truncated_normal_distribution_draw cannot draw"
                      + " values for mu <= 0 or sigma < 0."
                      + f"mu: {mu}, sigma:{sigma}")
    while draw < min_threshold:
        draw = np.random.normal(mu, sigma)

    return max(1, int(np.rint(draw)))

# ---------------------VIDEO OF OPTIMIZING ALGORITHM --------------------#

# Main SA function


def sa_optimization(grid,
                    runtime=None,
                    omega=0.1,
                    starting_temperature='auto',
                    ratio_temperatue_at_two_third_of_steps=1/20,
                    flip_rep=None,
                    swap_rep=None,
                    swap_option=None,
                    print_log=False,
                    print_progress_bar=True,
                    plot_price_curve=True,
                    save_output=True,
                    save_image=True,
                    save_opt_video=True,
                    output_folder=None
                    ):
    """
    This function runs a Simulated Annealing (SA) algorithm on the grid to
    minimize the price function. See more detail about the algorithm in
    the Notes section bellow.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid the algorithm should be performed on in order to find
        solution to the grid price optimization problem.

    runtime: float (in sec)
        Runtime in seconds for the algo. Algorithm is
        interupted at the end of the runtime.

    omega: float in [0, 1]
        Parameter used to determine the staring temperature as explained in
        the Notes of the function description.

    starting_temperature: float or str
        This parameter specifies the starting temperature of the SA.
        If parameter is 'auto', an initial temperature is computed using
        the omega paramter as explained in the Notes of the function
        description.

    flip_rep: int
        Number of repetition of "flip" transition per temperature
        step.

    swap_rep: int
        Number of repetition of "swap" transition per temperature
        step.

    swap_option: str
        Determines which variant of the swap transition should be used.
        Possibilities are:
            -'random':
                for each swap transition, the household and hub to be
                swaped are selected at random.
            -'nearest_neighbour':
                picks the closest household to the randomly selected meterhub.

    print_log: :obj:`bool`
        Parameter that specifies whether the detail of the run should be
        written in the console (when value is True) or not.

    print_progress_bar: :obj:`bool`
        Determines wheter or not the progress bar should be print in the console.

    plot_price_curve: :obj:`bool`
        Parameters that specifies wheter the curve of the price evolution
        during the run should be plotted in the console at the end of the run.

    save_output: obj: `bool`
        Determines whether or not the output grid should be saved in a folder,
        the parameter output_folder specifies the path of the folder the
        output should be saved in.

    save_image: obj: `bool`
        Determines whether or not the image of the grid should be saved in the
        output folder. The image is only saved if the parameter save_output is
        True.

    save_opt_video: :obj:`bool`
        Determines whether or not a video of the evolution of the algorithm
        should be created and saved in the folder where the output grid
        is saved. The optimization video can only be saved if the parameter
        save_output is True.

    output_folder: str
        Path of the folder the grid output of the algorithm should be
        saved in.



    Notes
    -----
    This function used the parameters defined in the config_algo.cfg file from
    the config folder. For the following parameters, when value is None,
    the parameter takes the value from the config_algo.cfg file:
        t_0, number_of_temperature_steps, cooling_rate, flip_rep, swap_rep,
        swap_option

    Simulated Annealing (SA) algorithm:
        During the algorithm, a number of temperature steps corresponding
        to the temperature_steps parameter will be performed. Each temperature
        steps is composed of a number of flips and of swaps corresponding to
        respectively flip_rep and swap_rep. The possible transitions (flip and
        swap) are performed at each step and the new configuration is kept only
        if the new grid price is lower than at the previous step or according
        to the so-called Metropolis accpetance probability given as
        exp(-Delta/temperature) where Delta is the price difference between
        former and new configuration.

        The initialization of the starting temperature uses the price of the
        approximation grid obatined using the k-means clustering method and
        the average price of randomly generated grids with the same number of
        hubs and the omega paramter. Let's denote these prices price_k_means
        and avg_price respectively, the price difference is denoted
        delta = (avg_price - price_k_means).
        The starting temperature is given by
            starting_temperature = omega * detla

        After each temperature step, the
        temperature is decreased by a factor corresponding to the cooling_rate
        parameter.

        The possible swap options are:
            - 'random':
                when performing a swap transition, the household to be
                swapped with the meterhub is selected unifromly at random.
            - 'nearest_neighbour':
                when performing a swap transition, the selected household
                to be swapped with the meterhub is necessarily the nearest
                household to the selected meterhub.
    """

    start_time = time.time()

    # Print bar is not printed if plrint_log is True
    if print_log:
        print_progress_bar = False

    # -------------------- Import config parameters --------------#
    # Grid config parameters

    # IMPORT ALGO PARAMETERS
    config_algo = ConfigParser()
    config_algo.read('./config/config_algo.cfg')

    # IMPORT cv2 CONFIG PARAMETRS
    config_cv2 = ConfigParser()
    config_cv2.read('./config/config_cv2.cfg')

    # For parameters that are None, import value from config_algo.cfg

    # Set up temperature parameter
    if omega is None:
        omega = config_algo.getfloat(
            'SA',
            'omega')
    # Set up number of flip transitions per temperature steps
    if flip_rep is None:
        flip_rep = config_algo.getint('SA', 'flip_rep')
    # Set up number of swap transitions per temperature steps
    if swap_rep is None:
        swap_rep = config_algo.getint('SA', 'swap_rep')
    if runtime is None:
        runtime = config_algo.getint('SA', 'runtime')

    if save_output:
        # Create output folder if not already existing
        if output_folder is None:
            folder = 'data/output/' + grid.get_id() + '/' + 'SA'
        else:
            folder = output_folder

        io.make_folder(folder)

        if flip_rep == 0 and grid.is_hub_capacity_constraint_too_strong():
            raise Warning("Hub capacity parameter doesn't allow grid to be"
                          + " optimized without performing flips")
            return 'SA algorithm aborted because of too low hub capacity'

        backup_name = (grid.get_id()
                       + f'_runtime{runtime}_'
                       + f'omega{omega}'.replace('.', '-'))

        if os.path.exists(folder + '/' + backup_name):
            counter = 1
            while os.path.exists(folder + '/' + backup_name + f'_{counter}'):
                counter += 1
            backup_name = backup_name + f'_{counter}'

        io.make_folder(folder + '/' + backup_name)

        # Create a video
        if save_opt_video:
            fourcc = cv2.VideoWriter_fourcc(*'MP42')
            video_path = (folder + '/' + backup_name + '/'
                          + grid.get_id() + '_' + 'SA' + '.avi')
            video = cv2.VideoWriter(video_path,
                                    fourcc,
                                    float(config_cv2.getint('video', 'FPS')),
                                    (grid.get_image().shape[1],
                                     grid.get_image().shape[0]))
        copyfile('./config/config_algo.cfg',
                 folder + '/' + backup_name + '/config_algo.cfg')
        # Store inital price for about_run file
        inital_price = grid.price()

    while grid.get_hubs().shape[0] == 0:
        grid.set_node_type_randomly(0.1)

    # Display algo parameters in console
    swap_option = config_algo.get('SA', 'swap_option')
    print(f"|{42 * '_'}| SIMULATED ANNEALING |{42 * '_'}|\n")
    print(f"runtime:             {str(runtime)}")
    print("omega:                           "
          + f"{str(omega)}")
    print(f"flip rep:                       {str(flip_rep)}")
    print(f"swap rep:                       {str(swap_rep)}")
    print(f"household selection for swap:   {swap_option}\n")

    print('\rinitializing starting temperature ...', end='')

    if starting_temperature == 'auto':
        starting_temperature, cooling_rate =\
            sa_compute_starting_temp_and_cooling_rate(
                grid,
                omega=omega,
                runtime=runtime,
                number_of_configuratio_to_compute_avg_price=10,
                ratio_temperatue_at_two_third_of_steps=1/20,
                number_of_flips=flip_rep,
                number_of_swaps=swap_rep)
    temperature = starting_temperature

    print(f"\rinitial temperature:          {str(round(temperature, 2))}")
    print("\n\n")

    # Write the actual grid image as the first frame of the video
    flip_households_until_hub_capacity_constraint_met(grid)
    link_nodes(grid)
    visu.draw_grid(grid)
    if save_opt_video and save_output:
        video.write(grid.get_image())
    # Store smaller grid price and node DataFrame (at this point it
    # corresponds of the input grid but it will be modified during run)
    lower_grid_price = grid.price()
    nodes_df_corresponding_to_lower_price = grid.get_nodes()
    # Create Dataframe with namely price evolution during the algorithm run
    # that will be saved as csv in folder
    performance_list = ['price',
                        'temperature',
                        'time',
                        'good flip',
                        'bad flip',
                        'good swap',
                        'bad swap',
                        'interhub_cable_length',
                        'distribution_cable_length']
    algo_run_log = pd.DataFrame(
        0,
        index=np.arange(1),
        columns=performance_list)
    algo_run_log['price'][0] = grid.price()
    algo_run_log['temperature'][0] = temperature
    algo_run_log['time'][0] = float(0)
    algo_run_log['interhub_cable_length'][0] =\
        grid.get_interhub_cable_length()
    algo_run_log['distribution_cable_length'][0] =\
        grid.get_distribution_cable_length()
    start_time = time.time()
    # make sure that the grid has enough hubs per semgment to meet
    # hub capacity constraint, if not the case, flip randomly chosen
    # households in each segment until capacity constraint is respected
    flip_households_until_hub_capacity_constraint_met(grid)
    # Save all nodes in a DF
    grid_nodes_init = grid.get_nodes()
    # Create empty DF that will contain the nodes of each segment
    # after SA run on the segment. The nodes will be added
    grid_nodes_final = grid.get_nodes().drop(
        [label for label in grid.get_nodes().index],
        axis=0)
    if print_progress_bar:
        display_progress_bar(
            0,
            1,
            f"price: {grid.price()}, temperature: {round(temperature, 2)}")
        counter_segment = 0
    for segment in grid.get_nodes()['segment'].unique():
        if print_log and len(grid.get_nodes()['segment'].unique()) > 0:
            print(f'\n\nsegment: {segment}\n')
        grid.set_nodes(
            grid_nodes_init[grid_nodes_init['segment'] == segment])
        step_counter = 0
        while time.time() - start_time < runtime:
            number_of_good_flips = 0
            number_of_bad_flips = 0

            number_of_good_swaps = 0
            number_of_bad_swaps = 0

            if print_log is True:
                if flip_rep != 0:
                    print('\nflip at temperature ' + str(int(temperature)))
            for f in range(flip_rep):
                if print_progress_bar:
                    message = (f"price: {grid.price()}, "
                               + f"temperature: {round(temperature, 2)}")
                    display_progress_bar(
                        (time.time() - start_time)/runtime,
                        1,
                        message)
                algo_status = sa_flip_step(grid=grid,
                                           temperature=temperature)
                if algo_status == 'good flip accepted':
                    number_of_good_flips += 1
                    if save_opt_video and save_output:
                        visu.draw_grid(grid)
                        video.write(grid.get_image())
                elif algo_status == 'bad flip accepted':
                    number_of_bad_flips += 1
                    if save_opt_video and save_output:
                        visu.draw_grid(grid)
                        video.write(grid.get_image())
                else:
                    algo_status = ''
                if print_log is True:
                    print('step: ' + str(step_counter) + " progress:"
                          + f'{int(time.time() - start_time) / runtime}%'
                          + '    f: ' + str(f + 1)
                          + '/' + str(flip_rep) + "   " + str(grid.price())
                          + "    " + algo_status)
                if grid.price() < lower_grid_price:
                    lower_grid_price = grid.price()
                    nodes_df_corresponding_to_lower_price = grid.get_nodes()
            if print_log is True:
                print('\nswap at temperature ' + str(int(temperature)))
            for s in range(swap_rep):
                if print_progress_bar:
                    message = (f"price: {grid.price()}, "
                               + f"temperature: {round(temperature, 2)}")
                    display_progress_bar(
                        (time.time() - start_time)/runtime,
                        1,
                        message=message)
                algo_status = sa_swap_step(grid=grid,
                                           temperature=temperature,
                                           swap_option=swap_option)
                if algo_status == 'good swap accepted':
                    number_of_good_swaps += 1
                    link_nodes(grid)
                    if save_opt_video and save_output:
                        visu.draw_grid(grid)
                        video.write(grid.get_image())
                elif algo_status == 'bad swap accepted':
                    number_of_bad_swaps += 1
                    link_nodes(grid)
                    if save_opt_video and save_output:
                        visu.draw_grid(grid)
                        video.write(grid.get_image())
                else:
                    algo_status = ''
                if print_log is True:
                    print('step: ' + str(step_counter) + " progress:"
                          + f'{int(time.time() - start_time) / runtime}%'
                          + '    s: ' + str(f + 1)
                          + '/' + str(swap_rep) + "   " + str(grid.price())
                          + "    " + algo_status)
                if grid.price() < lower_grid_price:
                    lower_grid_price = grid.price()
                    nodes_df_corresponding_to_lower_price = grid.get_nodes()

            algo_run_log.loc[str(algo_run_log.shape[0])] = [
                grid.price(),
                temperature,
                time.time() - start_time,
                number_of_good_flips,
                number_of_bad_flips,
                number_of_good_swaps,
                number_of_bad_swaps,
                grid.get_interhub_cable_length(),
                grid.get_distribution_cable_length()
            ]

            # compute temperature at current time. The cooling scheme is such
            # that the temperature is a decaying exponential starting at the
            # starting temperature and reaching
            # ratio_temperatue_at_two_third_of_steps * starting_temperature
            # at two third of the runtime
            current_time = time.time() - start_time
            temperature = (starting_temperature
                           * ratio_temperatue_at_two_third_of_steps**(
                               (3 * current_time)/(2 * runtime)))

        if print_progress_bar:
            message = (f"price: {grid.price()}, "
                       + f"temperature: {round(temperature, 2)}")
            display_progress_bar(1, 1, message=message)

            print(f"\n\nFinal price estimate: {grid.price()} $\n")

        # print detail of sa transitions accepted
        if print_log:
            print('\nNumber of good flips: '
                  + str(algo_run_log['good flip'].sum()))
            print('Number of bad flips:  '
                  + str(algo_run_log['bad flip'].sum()))
            print('Number of good swaps: '
                  + str(algo_run_log['good swap'].sum()))
            print('Number of bad swaps:  '
                  + str(algo_run_log['bad swap'].sum()) + '\n')
        grid_nodes_final = pd.concat([grid_nodes_final, grid.get_nodes()])
        grid.clear_nodes_and_links()
        grid.set_nodes(grid_nodes_final)
        link_nodes(grid)
        visu.draw_grid(grid)
        if print_progress_bar:
            counter_segment += 1
    if save_output:
        if save_opt_video:
            video.write(grid.get_image())
            video.write(grid.get_image())
            video.write(grid.get_image())
            video.release()
        algo_run_log = algo_run_log[algo_run_log['price'] != 0]
        algo_run_log.to_csv(folder + '/' + backup_name + '/log.csv')

        if lower_grid_price < grid.price():
            grid.set_nodes(nodes_df_corresponding_to_lower_price)
            link_nodes(grid)
            visu.draw_grid(grid)

        io.export_grid(grid,
                       folder=folder,
                       backup_name=backup_name,
                       save_image=save_image,
                       allow_saving_in_existing_backup_folder=True)

        # create a json file containing about dictionary
        about_dict = {
            'grid id': grid.get_id(),
            't_0': temperature,
            'number_of_temperature_steps'
            'flip_rep': flip_rep,
            'swap_rep': swap_rep,
            'swap_option': swap_option,
            'print_log': print_log,
            'print_progress_bar': print_progress_bar,
            'plot_price_curve': plot_price_curve,
            'save_output': save_output,
            'save_opt_video': save_opt_video,
            'output_folder': output_folder,
            'initial_price': inital_price,
            'final_price': grid.price()
        }

        json.dumps(about_dict)

        with open(folder + '/' + backup_name + '/about_run.json',
                  'w') as about:
            about.write(json.dumps(about_dict))
    if plot_price_curve is True:
        print('\n')
        plot.plot_price_evolution_for_sa_run(sa_log=algo_run_log)


def sa_compute_starting_temp_and_cooling_rate(
        grid,
        omega,
        runtime,
        number_of_configuratio_to_compute_avg_price,
        ratio_temperatue_at_two_third_of_steps,
        number_of_flips,
        number_of_swaps):
    """
    This function computes an intial temperature and a cooling_rate for
    the function sa_optimization. The temperature is computed by
    consideing an average price for several randomly generated configurations
    and the price of the grid obatined using applying the k_means clustering
    method used in nr_optimization(). The cooling ratio is computed so that the
    temperature at two third of the time is equal to the inital temperature
    times ratio_temperatue_at_two_third_of_steps.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object used for computing the initial temperature.

    omega: float
        This parameter will determine the value of the starting temperature t_0
        using the following expression
        t_0 = (avg_price - price_k_means) * omega
        where avg_price is the average price of the randomly generated
        configurations and price_k_means is the price of the configuration
        obatined using the k_means clustering method.

    runtime: int
        Runtime in seonds of the sa_optimization run after the initial
        temperature is determined.

    number_of_configuratio_to_compute_avg_price: int
        Number of transitions performed to obtain an average price difference.

    ratio_temperatue_at_two_third_of_steps: float in [0,1]
        Ratio of the temperature at two third of the runtime over initial
        temperature that determines the value of the cooling ratio.
        The temperature at time x is given by
        temperature(x) = t_0 * alpha**x
        and alpha is the cooling ratio given by
        alhpa = (ratio_temperatue_at_two_third_of_steps)**(3/(2*runtime))

    Output
    ------
    (float,float)
    initial temperature, cooling ratio.
    """

    # Monitor time spent in function to compute the number of temperature steps
    # so that the sa_optimization function runs for runtime seconds
    nodes = grid.get_nodes().copy()
    links = grid.get_links().copy()

    grid_prices = []
    number_of_hubs = get_expected_hub_number_from_k_means(grid)

    for i in range(number_of_configuratio_to_compute_avg_price):
        grid.set_all_node_type_to_households()
        while grid.get_hubs().shape[0] < number_of_hubs:
            household_picked = random.choice(grid.get_households().index)
            grid.flip_node(household_picked)
        link_nodes(grid)
        grid_prices.append(grid.price())

    nr_optimization(grid,
                    number_of_hubs=number_of_hubs,
                    number_of_relaxation_step=0,
                    first_guess_strategy='k_means',
                    save_output=False,
                    output_folder=None,
                    save_image=False,
                    save_opt_video=False,
                    plot_arrow_in_video=False,
                    plot_price_evolution=False,
                    print_progress_bar=False)

    price_k_means = grid.price()
    avg_price = statistics.mean(grid_prices)

    delta_price = np.absolute(avg_price - price_k_means)
    starting_temperature = delta_price * omega

    cooling_rate = ratio_temperatue_at_two_third_of_steps**(3/(2 * runtime))

    grid.set_nodes(nodes)
    grid.set_links(links)

    return starting_temperature, cooling_rate


# Transitions form one grid configuration to another


def sa_flip_step(grid, temperature):
    """
    This function perform a step of the Simulated Annealing (SA)
    algorithm on a Grid object. It picks a node uniformly at random
    and flips its 'node_type' status (i.e. if node_type is
    meterhub, change it to household, if node_type is household,
    change it to meterhub) and keep the new configuration according
    to the SA algorithm. This function is used as a transition step
    of the optimizing algorithm 'sa_optimization' of
    the tools.optimization module for the SA algorithm.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid upon which the Simulated Annealing step should be performed

    Notes
    -----
        The SA algorithm is based on random modifications to the grid
        similar to a Metropolis Monte Carlo optimization model
        based on Markov chain with acceptance probabilty
        A(X->Y) = min(1, exp(-delta_price/temperature))
        where delta_price denotes the price difference between
        the two configurations X and Y and where temperature is a
        parameter of the model that decreases thanks to the cooling_ratio
        parameter. See documentation for more info.
    """
    # Make sure that the node dataframe with non-fixed nodes is
    # not empty
    if grid.get_nodes()[
            grid.get_nodes()['node_type'] != 'powerhub'].shape[0] > 0:
        # Pick random number to be compared with price delta
        random_number = np.random.rand()
        # Save the price of the grid as it is before changinig
        # anything
        initial_price = grid.price()
        # Save the node dataframe in case the change performed
        # doesn't improve the price
        backup_grid_nodes = grid.get_nodes()
        backup_grid_links = grid.get_links()
        grid.flip_random_node()
        # Reject flip if new configuration doesn't meet hub capacity constraint
        if grid.is_hub_capacity_constraint_too_strong():
            grid.set_nodes(backup_grid_nodes)
            grid.set_links(backup_grid_links)
            return 'bad flip rejected'
        else:
            link_nodes(grid)
        # delta_price is the price difference between the former
        # and new configuration
        delta_price = abs(grid.price()-initial_price)
        if grid.price() < initial_price:
            return 'good flip accepted'
        # SA algorithm accept new config with higher price
        # with probability exp(-delta_price/temperature)
        if temperature > 0:
            if random_number < math.exp(- delta_price / temperature):
                return 'bad flip accepted'

            else:
                grid.set_nodes(backup_grid_nodes)
                grid.set_links(backup_grid_links)
                return 'bad flip rejected'
        else:
            grid.set_nodes(backup_grid_nodes)
            grid.set_links(backup_grid_links)
            return 'bad flip rejected'
    else:
        raise Exception("ERROR: invalid 'algorithm' parameter "
                        + "given as input for "
                        + "Grid.flip_random_node method")


def sa_swap_step(grid, temperature, swap_option):
    """
    This function picks a meterhub uniformly at random and, accroding
    to the alogrithm given as input, swaps its 'node_type'
    with the one of a household picked according to the
    swap_option parameter.
    This function is used as a step of the optimizing function
    'sa_optimization'.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid object.

    swap_option: str
        If swap_option is 'nearest_neighbour', the household that is picked is
        necessarily the one that is the clostest to the picked meterhub.
        If swap_option  is 'random', the household to be swaped with the
        meterhub is selected uniformly at random.

    algorithm: str
        This parameter specifies the algorithm to be used when this function
        is called in an optimization process. The options for the algortihm
        are the following:
            - None
                If no algorithm is given, the method performs the swap
                and doesn't revert it regardless of the grid price.

            - 'strict price improvement'
                This quite simple algorithm tries to swap the two nodes
                picked and  revert the swap if the overall grid price
                was better before the swap.

            - 'metropolis'
                The algorithm is based on random modifications to the grid
                similar to a Metropolis Monte Carlo optimization model
                based on Markov chain with acceptance probabilty
                A(X->Y) = min(1, exp(-delta_price/temperature))
                where delta_price denotes the price difference between
                the two configurations X and Y and wheretemperature is a
                parameter of the model that is fixed.
    """
    # Make sure that the grid contains at least one meterhub and one household
    if grid.get_nodes()[
            grid.get_nodes()['node_type'] == 'meterhub'].shape[0] > 0:

        # Pick random number number to be compared with price delta
        random_number = np.random.rand()
        # Store the price of the grid as it is before
        # changinig anything
        initial_price = grid.price()
        # Store the node dataframe in case the swap performed
        # doesn't improve the gird price
        backup_grid_nodes = grid.get_nodes()
        backup_grid_links = grid.get_links()
        grid.swap_random(swap_option=swap_option)
        link_nodes(grid)
        # delta_price is the price difference between the former
        # and new configuration
        delta_price = grid.price() - initial_price
        if grid.price() < initial_price:
            return "good swap accepted"
        # Metropolis algorithm accept new config with higher price
        # with probability exp(-delta_price/t)
        if temperature > 0:
            if random_number < math.exp(-delta_price/temperature):
                return 'bad swap accepted'
            else:
                grid.set_nodes(backup_grid_nodes)
                grid.set_links(backup_grid_links)
                initial_price = grid.price()
                return 'bad swap rejected'
        else:
            grid.set_nodes(backup_grid_nodes)
            grid.set_links(backup_grid_links)
            initial_price = grid.price()
            return 'bad swap rejected'

# SA Progress bar


def printProgressBar(iteration,
                     total,
                     prefix='',
                     suffix='',
                     decimals=1,
                     length=100,
                     fill='█',
                     printEnd="\r",
                     price=None):
    """
    Call in a loop to create terminal progress bar.

    Parameters
    ----------
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent
                                  complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

        Notes
        -----
            Funtion inspired from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console/30740258 # noqa: E501
    """
    percent = ("{0:." + str(decimals) + "f}").format(
        100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    if price is None:
        print(f'\r{prefix} |{bar}| {percent}% {suffix}',
              end=printEnd)
    else:
        print(f'\r{prefix} |{bar}| {percent}% {suffix}, price: {price} $',
              end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def display_progress_bar(current, final, message=''):
    """
    This function displays a progress bar on the console. The progress is
    displayed in percent and corresponds to current/final. The message
    parameter is appended  after the progress bar.

    Parameters
    ----------
    current: float
        Current iteration.

    final: float
        Final iteration.

    message: str
        Diplayed after the progress bar.

    """
    if current > final:
        final = current

    current_in_percent = int(current / final * 50)
    remaining = 50 - current_in_percent

    bar = '█' * current_in_percent + '-' * remaining
    print(f"\r|{bar}|  {int(current / final * 100)}%   {message}",
          end='')

# --------------- LINEAR PROGRAMMING SOLVER BASED FUNCTIONS --------------- #


# Main Linear Programming (LP) function


def lp_optimization(grid,
                    hub_capacity='from_config_file',
                    relax_constraint_10=True,
                    output_folder=None,
                    save_image=True):
    """
    This function uses the PULP solver to find a lower bound for a solution to
    the design optimization problem of building a tree-star shaped network
    minimizing cable costs from the grid given as parameter.

    Parameters
    ----------
    grid: :class:`~.grids.Grid`
        Grid the algorithm should be performed on in order to find
        solution to the grid price optimization problem.

    hub_capacity: int or str
        Maximum number of households that can be allocated to each hub.

        If hub_capacity is 'uncapacitated', the capacity for each new hub
        is set to the number of nodes in the grid.

        If hub_capacity is 'from_config_file', the capacity is the one
        given in the config_grid.cfg file.

    relax_constraint_10: bool
        When True, Constraint (10) is ignored (relaxed).

    output_folder: str
        Path of the folder the grid output of the algorithm should be
        saved in.

    save_image: :obj:`bool`
        Determines whether or not the image of the grid should be saved in the
        output folder.

    Output
    ------
    obj: :`dic` containing:
        - lower_bound: float
            Price of the solution to the relaxed problem.
        - optimal_solution_feasible: bool
            Indicates whether or not the solution found satisfies the spanning
            constraint.

    Notes
    -----
        In case the solution found doesn't represent a spanning grid
        (in which case solution cannot be accepted), all nodes 'node_type'
        are set to 'household'.
    """

    starting_time = time.time()

    config_grid = ConfigParser()
    config_grid.read('config/config_grid.cfg')

    if hub_capacity == 'from_config_file':
        hub_capacity = config_grid.getint('constraints',
                                          'default_hub_capacity')
        if hub_capacity == 0:
            hub_capacity = grid.get_nodes().shape[0]

    if hub_capacity == 'uncapacitated':
        hub_capacity = grid.get_nodes().shape[0]

    # number of nodes in the grid
    number_of_nodes = grid.get_nodes().shape[0]

    # distance list
    distance_list = []
    for node_i, row_i in grid.get_nodes().iterrows():
        for node_j, row_j in grid.get_nodes().iterrows():
            distance_list.append(grid.distance_between_nodes(node_i, node_j))

    distribution_cable_price = config_grid.getfloat(
        'price',
        'distribution_cable_per_meter')
    interhub_cable_price = config_grid.getfloat(
        'price',
        'interhub_cable_per_meter')
    price_meterhub = config_grid.getfloat('price', 'meterhub')
    price_household = config_grid.getfloat('price', 'household')

    # Create helping functions from passing from list to matrix indices
    def k_lu(i, j): return lp_lu_to_list(i, j)                 # noqa: E731
    def i_lu(k): return lp_list_to_lu(k)[0]                    # noqa: E731
    def j_lu(k): return lp_list_to_lu(k)[1]                    # noqa: E731
    def ij(i, j): return i * number_of_nodes + j               # noqa: E731

    # Create the linear programming model
    model = LpProblem(name="small-problem", sense=LpMinimize)

    # ------------------Initialize the decision variables---------------#

    # x(i, j) = x[i * n + j] variable -> 1 iff node i is household
    # assigned to hub j (n = number_of_nodes)
    x = []
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            if i == j:
                x.append(0)
            if i != j:
                x.append(LpVariable(
                    name=f'x({grid.get_nodes().index[i]},'
                         + f'{grid.get_nodes().index[j]})',
                    lowBound=0,
                    upBound=1,
                    cat="Integer"))

    # y(i, j) = y[i * n + j] -> 1 iff node i is a hub assigned to hub j
    y = []
    for i in range(number_of_nodes):
        for j in range(i + 1):
            y.append(LpVariable(
                name=f'y({grid.get_nodes().index[i]},'
                + f'{grid.get_nodes().index[j]})',
                lowBound=0,
                upBound=1, cat="Integer"))

    # ---------------Add the objective function to the model---------------#

    obj_func = (
        (distribution_cable_price
         * sum([x_k * d_k for x_k, d_k in zip(x, distance_list)]))
        + (interhub_cable_price
           * sum([y[k] * distance_list[ij(i_lu(k), j_lu(k))]
                  for k in range(len(y))])
           )
        + price_meterhub * sum(
            [y[k_lu(i, i)] for i in range(number_of_nodes)]
        )
        + price_household * (number_of_nodes
                             - sum([y[k_lu(i, i)]
                                    for i in range(number_of_nodes)]))
    )
    model += obj_func

    # -------------------Add the constraints to the model-------------------#

    # Constraint (1)
    #       node i is either a household or a hub
    #       & if i is a household, it cannot be allocated to multiple hubs
    for i in range(number_of_nodes):
        model += (sum([x[ij(i, j)]
                       for j in range(number_of_nodes)]
                      ) + y[k_lu(i, i)] == 1,
                  f'(1) node {i} is either a household or a hub')

    # Constraint (2) if household i is allocated to j, then j must be a hub
    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            model += (x[ij(i, j)] <= y[k_lu(j, j)],
                      f'(2) if node {i} is allocated to node {j},'
                      + f' then {j} is a hub')

    # Constraint (3) there are one less inter-hub link than hubs in the grid
    model += (sum(y) == 2 * sum([y[k_lu(i, i)]
                                 for i in range(number_of_nodes)]) - 1,
              '(3) there are one less inter-hub link than hubs in the grid')

    # Constraint (4) Each hub is connected to at least one other hub
    for i in range(number_of_nodes):
        model += (sum([y[k_lu(i, j)] for j in range(i)])
                  + sum([y[k_lu(j, i)]
                         for j in range(i + 1, number_of_nodes)]
                        ) >= y[k_lu(i, i)],
                  f'(4) hub {i} is connected to at least one other hub')

    # Constraint (5) each i must be a hub if y_ij > 1 for all j
    for i in range(number_of_nodes):
        model += (
            (sum([y[k_lu(i, j)] for j in range(i)])
             + sum([y[k_lu(j, i)] for j in range(i + 1, number_of_nodes)])
             <= y[k_lu(i, i)] * number_of_nodes),
            f'(5) hub {i} is a hub if there is at least a j so that y_ij > 0')

    # ---------------------Solve the problem---------------------#
    status = model.solve()

    if status != 1:
        raise Warning("The LP solver didn't find any solution")

    grid.set_all_node_type_to_households()
    grid.clear_links()

    # first set nodes for which y(i, i) == 1 to meterhubs
    for var in model.variables():
        if var.value() != 0.0:
            variable, node_i, node_j = lp_decompose_output_str(var.name)
            if variable == 'y' and node_i == node_j:
                grid.set_node_type(node_i, 'meterhub')

    # Then add links to the grid according to output values
    for var in model.variables():
        if var.value() != 0.0:
            variable, node_i, node_j = lp_decompose_output_str(var.name)
            if node_i != node_j:
                grid.add_link(node_i, node_j)

    visu.draw_grid(grid)

    if output_folder is None:
        folder = f'data/output/{grid.get_id()}/LP'
    else:
        folder = output_folder
    backup_name = f'{grid.get_id()}_LP'

    if os.path.exists(f'{folder}/{backup_name}'):
        counter = 1
        while os.path.exists(f'{folder}/{backup_name}_{counter}'):
            counter += 1
        backup_name += f'_{counter}'

    grid_connected = True
    for segment in grid.get_nodes()['segment'].unique():
        if not grid.is_segment_spanning_tree(segment):
            print(
                "The solution found by lp_optimization doesn't fullfil the"
                + " graph connectivity criterion..")
            grid_connected = False

    if not grid_connected:
        backup_name = backup_name + '_DISCONNECTED'

    io.export_grid(grid,
                   folder=folder,
                   backup_name=backup_name,
                   save_image=save_image)
    # Save log containing the runtime as csv file
    runtime = time.time() - starting_time

    runtime_df = pd.DataFrame({'runtime': [runtime],
                               'price': [grid.price()],
                               'connected': [grid_connected]})

    runtime_df.to_csv(f'{folder}/{backup_name}/log.csv')

    if grid_connected:
        return {'lower_bound_price [$]': model.objective.value(),
                'optimal_solution_feasible': True}
    else:
        return {'lower_bound_price [$]': model.objective.value(),
                'optimal_solution_feasible': False}


# Helping functions used for Linear Programming


def lp_list_to_lu(k):
    """
    Helping function that helps getting the matrix indices corresponding
    to list index representing a lower-diagonal matrix. The list comports
    all matrix entries for j < i (i and j denoting the column and row
    indices respectively).

    Parameters
    ----------
    k: int
        Index of the list representing a lower-diagonal matrix.

    Output
    ------
    list(int, int)
        Row and column indices of the matrix.
    """

    def s(k): return int(k*(k+1)/2)               # noqa: E731
    def s_inv(k): return (-1 + np.sqrt(1+8*k))/2   # noqa: E731

    i = np.floor(s_inv(k))
    j = k - s(i + 1) + i + 1
    return int(i), int(j)


def lp_lu_to_list(i, j):
    """
    Helping function that help getting the list element corresponding to
    the matrix indices at row i and column j. The list comports
    all matrix entries for j < i (i and j denoting the column and row
    indices respectively).

    Parameters
    ----------

    i: int
        Row index of the lower-diagonal matrix.
    j: int
        Column index of the lower-diagonal matrix.
    Output
    ------
    list(int, int)
        List inices of the list representing the matrix."""

    def s(k): return int(k*(k+1)/2)               # noqa: E731

    if j > i:
        raise Warning("invalid matrix values. j <= i must hold."
                      + f" value given are (i, j) = ({i}, {j}) ")
    return s(i + 1) - i + j - 1


def lp_decompose_output_str(string_var):
    """
    This function decomposes string variable from the output of the LP
    solver into a list.

    Parameter
    ---------
    string_var: str
        string variable from the output of the LP solver, typically looks like
        x(2, 17).

    Output
    ------
    list of str
        Decomposition of the input string. If input is x(2, 17),
        output is [x, 2, 17].
    """
    return string_var.replace('(', '/').replace(',', '/').replace(
        ')', '/').split('/')[0:3]

# --------------- NETWORK RELAXATION FUNCTIONS --------------- #


def nr_optimization(grid,
                    number_of_hubs,
                    number_of_relaxation_step,
                    damping_factor=0.5,
                    weight_of_attraction='constant',
                    first_guess_strategy='random',
                    number_of_steps_bewteen_random_shifts=0,
                    number_of_hill_climbers_runs=0,
                    save_output=True,
                    output_folder=None,
                    save_image=True,
                    save_opt_video=True,
                    plot_arrow_in_video=False,
                    plot_price_evolution=True,
                    print_progress_bar=True):
    """
    This function can be used to find a approximate solution
    to the price minimization of the grid layout. It is based on
    an iterative process. The core idea is to consider the links
    at a hub as pulling strings exercing a force on each hub.
    To this end, virtual hubs are added to the grid and all other
    non-fixed hubs are considered as households. The virtual hubs
    are free to locate wherever on the image and at each iteration
    step, they are shifted in the direction of the resulting "strength"
    from the nodes they are linked with.

    Parameters
    ----------
        grid: :class:`~.grids.Grid`
            Grid object.

        number_of_hubs: int
            Number of hubs in the grid.

        number_of_relaxation_step: int
            Number of iteration in relaxation process.

        damping_factor: int
            Factor determining by how much the virtual hubs are shifted
            together with shortest distance between pair of nodes.

        weight_of_attraction: str
            Defines how strong each link attracts/pulls the hub.
            Possibilites are:
                - 'constant':
                    Only depends on the type of link.
                - 'distance':
                    Depends on the type of link and is proportional to the
                    distance of the link. (i.e. long links pull stronger).

        first_guess_strategy: str
            Defines the stategy that should be used to get the starting
            configuration.
            Possibilites are:
                - 'k_means': (default)
                    Virtual hubs are initially located at center of cluster
                    obtained using a k_means clustering algorithm from the
                    sklearn library.
                - 'random':
                    Virtual nodes are randomly located in box containing all
                    grid nodes.
                - 'relax_input_grid':
                    The starting configuration is the one of the grid given as
                    input.

        number_of_steps_bewteen_random_shifts: int
            Determines how often a random shift of one of the hubs should
            occur.

        save_output: bool
            Determines whether or not the output grid and the log should be
            saved in the output_folder.

        number_of_hill_climbers_runs: int
            When larger than 0, local price optimization is performed after the
            relaxation. The local price optimization process computes
            in which direction each hub should be shifted in order to improve
            the price and performs the according shift. The process is repeated
            number_of_hill_climbers_runs times.

        output_folder: str
            Path of the folder the grid output of the algorithm should be
            saved in.

        save_image: :obj:`bool`
            If True and save_output also True, saves an image of the grid in
            the output folder.

        save_opt_video: bool
            Determines whether or not a video of the optimization algorithm run
            should be saved in the output_folder.

        plot_arrow_in_video: bool
            Determines whether or not arrows representing the "attraction" of
            each hub by the links should be drawn on the image.

        plot_price_evolution: bool
            Determines whether or not the evolution of the price as a function
            of the runtime of the algorithm should be plotted in the console.

        print_progress_bar: bool
            Determines whether or not the progress bar should be displayed in
            the console.

    Output
    ------
        class:`pandas.core.frame.DataFrame`
            log Dataframe containg the detail of the run as well as the,
            time evolution, the virtual_price (see notes for more info)
            evolution and a measure of how much the hubs are shifted at
            each step.
    Notes
    -----
        The virtual price is the price of the grid containing the freely
        located virtual hubs. Since, during the process, the layout is
        not a feasible solution (the virtual hubs are not located at house
        location), the price that is computed cannot be interpreted as the
        price of a feasible grid layout
    """
    if save_output:
        print(f"|{42 * '_'}| NETWORK RELAXATION |{42 * '_'}|\n")
        print(f"{35 * ' '}number of hubs:{8 * ' '} {number_of_hubs}\n")
        print(
            f"{35 * ' '}number of steps:{8 * ' '}{number_of_relaxation_step}")
        print('\n')
        print(
            f"{35 * ' '}first guess strategy:{3 * ' '}{first_guess_strategy}")
        print(f"\n{35 * ' '}weight of attraction:{3 * ' '}"
              + f"{weight_of_attraction}\n\n")

    # import and  initialize parameters
    arrow_color = (0, 255, 200)
    thickness = 10
    config_grid = ConfigParser()
    config_grid.read('./config/config_grid.cfg')
    allocation_capacity = config_grid.getint('constraints',
                                             'default_hub_capacity')
    price_household = config_grid.getfloat('price', 'household')

    config_grid = ConfigParser()
    config_grid.read('config/config_grid.cfg')
    # IMPORT cv2 CONFIG PARAMETRS
    config_cv2 = ConfigParser()
    config_cv2.read('./config/config_cv2.cfg')

    if save_output:
        # Create run video and folder for saving output
        if save_opt_video:
            fourcc = cv2.VideoWriter_fourcc(*'MP42')

        if output_folder is None:
            path_to_folder = f'data/output/{grid.get_id()}/NR'
        else:
            path_to_folder = output_folder
        io.make_folder(path_to_folder)

        folder_name = (f'{grid.get_id()}_NR_{number_of_hubs}'
                       + f'_hubs_{number_of_relaxation_step}steps'
                       + f'_attr-{weight_of_attraction[:4]}')

        if os.path.exists(f'{path_to_folder}/{folder_name}'):
            counter = 1
            while os.path.exists(f'{path_to_folder}/{folder_name}_{counter}'):
                counter += 1
            folder_name_with_path = f'{path_to_folder}/{folder_name}_{counter}'
            folder_name = f'{folder_name}_{counter}'
            io.make_folder(folder_name_with_path)
        else:
            folder_name_with_path = f'{path_to_folder}/{folder_name}'
            io.make_folder(folder_name_with_path)
        if save_opt_video:
            video_path =\
                (f'{folder_name_with_path}/NR_run_{grid.get_id()}.avi')
            video = cv2.VideoWriter(
                video_path,
                fourcc,
                3 * float(config_cv2.getint('video', 'FPS')),
                (grid.get_image().shape[1],
                 grid.get_image().shape[0]))

    # Create copy of grid so that the algorithm runs on that copy
    # and that the grid is set to the grid copy at the end of the algorithm
    # (the motivation is to avoid having grid with virtual nodes in case the
    # function is interrupted)
    grid_copy = copy.deepcopy(grid)

    grid_copy.clear_image()

    # find out what x and y coordinat ranges the nodes are in
    x_range = [grid_copy.get_nodes()['pixel_x_axis'].min(),
               grid_copy.get_nodes()['pixel_x_axis'].max()]
    y_range = [grid_copy.get_nodes()['pixel_y_axis'].min(),
               grid_copy.get_nodes()['pixel_y_axis'].max()]
    # Create log dataframe that will store info about run
    algo_run_log = pd.DataFrame({'time': pd.Series(
        [0]
        * number_of_relaxation_step,
        dtype=float),
        'virtual_price': pd.Series(
        [0]
        * number_of_relaxation_step,
        dtype=float),
        'norm_longest_shift': pd.Series(
        [0]
        * number_of_relaxation_step,
        dtype=float)})
    # Define number of virtual hubs
    number_of_virtual_hubs = (number_of_hubs
                              - grid_copy.get_hubs()[
                                  grid_copy.get_hubs()[
                                      'type_fixed']].shape[0]
                              )
    if first_guess_strategy == 'random':
        # flip all non-fixed hubs from the grid for the optimization
        for hub, row in grid_copy.get_hubs().iterrows():
            if not row['type_fixed']:
                grid_copy.flip_node(hub)

        # Create virtual hubs and add them at locations within
        # square containing all nodes
        for i in range(number_of_virtual_hubs):
            grid_copy.add_node(label=f'V{i}',
                               pixel_x_axis=random.randint(x_range[0],
                                                           x_range[1]),
                               pixel_y_axis=random.randint(y_range[0],
                                                           y_range[1]),
                               node_type='meterhub',
                               segment='0',
                               allocation_capacity=allocation_capacity)

    elif first_guess_strategy == 'k_means':
        # flip all non-fixed hubs from the grid for the optimization
        for hub, row in grid_copy.get_hubs().iterrows():
            if not row['type_fixed']:
                grid_copy.flip_node(hub)

        # Create virtual hubs and add them at centers of clusters
        # given by the k_means_cluster_centers() function

        cluster_centers = k_means_cluster_centers(
            grid=grid_copy,
            k_number_of_clusters=number_of_virtual_hubs)

        count = 0
        for coord in cluster_centers:
            grid_copy.add_node(label=f'V{count}',
                               pixel_x_axis=int(coord[0]),
                               pixel_y_axis=int(coord[1]),
                               node_type='meterhub',
                               segment='0',
                               allocation_capacity=allocation_capacity)
            count += 1

    elif first_guess_strategy == 'relax_input_grid':
        counter = 0
        intial_hub_indices = grid_copy.get_hubs().index

        for hub in intial_hub_indices:
            grid_copy.add_node(
                label=f'V{counter}',
                pixel_x_axis=grid_copy.get_hubs()['pixel_x_axis'][hub],
                pixel_y_axis=grid_copy.get_hubs()['pixel_y_axis'][hub],
                node_type='meterhub',
                type_fixed=False,
                segment='0',
                allocation_capacity=allocation_capacity)
            grid_copy.set_node_type(hub, 'household')
            counter += 1

    else:
        raise Warning("invalid first_guess_strategy parameter, possibilities "
                      + "are:\n- 'random'\n- 'k_means'\n- 'relax_input_grid'")

    if save_opt_video and save_output:
        link_nodes(grid_copy)
        visu.draw_grid(
            grid_copy,
            grid_price=grid_copy.price() - (number_of_virtual_hubs
                                            * price_household))
        grid_image = grid_copy.get_image()
        video.write(grid_image)

    link_nodes(grid_copy)
    start_time = time.time()
    # ---------- STEP 0 - Initialization step -------- #
    if print_progress_bar:
        printProgressBar(0, 1)
    # Compute new relaxation_df
    relaxation_df = nr_compute_relaxation_df(grid_copy, weight_of_attraction)
    norm_longest_vector = nr_get_norm_of_longest_vector_resulting(
        relaxation_df)
    # Store vector resulting from current and previous step in order
    # to adapt the damping_factor value at each step. At each step, the
    # scalar product between the vector_resulting form the previous
    # and current step will be computed and used to adapt the damping_factor
    # value
    list_resulting_vectors_previous_step =\
        nr_compute_relaxation_df(grid_copy,
                                 weight_of_attraction)['vector_resulting']
    list_resulting_vectors_current_step =\
        nr_compute_relaxation_df(grid_copy,
                                 weight_of_attraction)['vector_resulting']
    meter_per_pixel_ratio = grid_copy.get_meter_per_pixel_ratio()
    household_cost = config_grid.getfloat('price', 'household')

    # Compute damping_factor such that:
    # The norm of the longest 'vector_resulting' of the relaxation_df at
    # step 0 is equal to half the distance of the smallest link

    smaller_link_distance = min(
        [x for x in grid_copy.get_links()['distance'] if x > 0]
    )

    # Apply damping_factor to vector_resulting for each hub
    for hub, row in relaxation_df.iterrows():
        row['vector_resulting'] =\
            [(x / norm_longest_vector * smaller_link_distance * damping_factor)
             for x in row['vector_resulting']]
    # Add new image with arrows to video
    visu.draw_grid(grid=grid_copy,
                   grid_price=int(grid_copy.price()
                                  - number_of_virtual_hubs * price_household))
    grid_image = grid_copy.get_image()
    if plot_arrow_in_video and save_output:
        for hub, row_hub in grid_copy.get_hubs().iterrows():
            start_point = (row_hub['pixel_x_axis'], row_hub['pixel_y_axis'])
            end_point = (int(start_point[0]
                             + 2 * (relaxation_df['vector_resulting'][hub][0]
                                    / meter_per_pixel_ratio)),
                         int(start_point[1]
                             + 2 * (relaxation_df['vector_resulting'][hub][1]
                                    / meter_per_pixel_ratio)))
            grid_image = cv2.arrowedLine(grid_image,
                                         start_point,
                                         end_point,
                                         arrow_color,
                                         thickness)
    if save_opt_video and save_output:
        video.write(grid_image)
    # Shift virtual hubs in direction 'vector_resulting'
    for hub, row_hub in grid_copy.get_hubs()[
            - grid_copy.get_hubs()['type_fixed']].iterrows():
        vector_resulting = relaxation_df['vector_resulting'][hub]
        grid_copy.shift_node(node=hub,
                             delta_x=(vector_resulting[0]
                                      / meter_per_pixel_ratio),
                             delta_y=(vector_resulting[1]
                                      / meter_per_pixel_ratio),
                             allow_shifting_node_outside_boundary=True)

    link_nodes(grid_copy)
    algo_run_log['time'][0] = time.time() - start_time
    # The solution have number_of_virtual_hubs households less than the
    # intermediate layout containing virtual hubs
    algo_run_log['virtual_price'][0] = (
        grid_copy.price()
        - number_of_virtual_hubs * household_cost)
    algo_run_log['norm_longest_shift'][0] = (norm_longest_vector
                                             / smaller_link_distance)
    if print_progress_bar:
        printProgressBar(1, number_of_relaxation_step + 1)

    # ------------ STEP n + 1 - ITERATIVE STEP ------------- #
    for n in range(1, number_of_relaxation_step + 1):
        if number_of_steps_bewteen_random_shifts > 0:
            if n % (number_of_steps_bewteen_random_shifts) == 0:
                hub_to_shift = np.random.choice(grid_copy.get_hubs().index)
                coord_hub = (
                    grid_copy.get_hubs()['pixel_x_axis'][hub_to_shift],
                    grid_copy.get_hubs()['pixel_y_axis'][hub_to_shift])
                random_household =\
                    np.random.choice(grid_copy.get_households().index)
                coord_household = (
                    grid_copy.get_households()['pixel_x_axis'][
                        random_household],
                    grid_copy.get_households()['pixel_y_axis'][
                        random_household])
                grid_copy.shift_node(hub_to_shift,
                                     coord_household[0] - coord_hub[0],
                                     coord_household[1] - coord_hub[1],
                                     allow_shifting_node_outside_boundary=True)

        relaxation_df = nr_compute_relaxation_df(grid_copy,
                                                 weight_of_attraction)
        list_resulting_vectors_current_step =\
            relaxation_df['vector_resulting']
        # For each hub, compute the scalar product of the resulting vector
        # from the previous and current step. The values will be used to
        # adapt the damping value
        list_scalar_product_vectors = \
            [x[0] * y[0] + x[1] * y[1] for x, y in zip(
                list_resulting_vectors_current_step,
                list_resulting_vectors_previous_step)]
        if min(list_scalar_product_vectors) >= 0:
            damping_factor = damping_factor * 2.5
        else:
            damping_factor = damping_factor / 1.5
        for hub, row in relaxation_df.iterrows():
            row['vector_resulting'] =\
                [(x / norm_longest_vector * smaller_link_distance
                  * damping_factor)
                 for x in row['vector_resulting']]

        # Add new image with arrows to video
        if save_output and save_opt_video:
            visu.draw_grid(grid=grid_copy,
                           grid_price=int(grid_copy.price()
                                          - (number_of_virtual_hubs
                                             * price_household)))
            grid_image = grid_copy.get_image()
            for hub, row_hub in grid_copy.get_hubs().iterrows():
                start_point =\
                    (row_hub['pixel_x_axis'], row_hub['pixel_y_axis'])
                end_point =\
                    (int(start_point[0]
                         + 2 * relaxation_df['vector_resulting'][hub][0]),
                     int(start_point[1]
                         + 2 * relaxation_df['vector_resulting'][hub][1]))
                grid_image = cv2.arrowedLine(grid_image,
                                             start_point,
                                             end_point,
                                             arrow_color,
                                             thickness)
            video.write(grid_image)

        # Shift virtual hubs in direction 'vector_resulting'
        for hub, row_hub in grid_copy.get_hubs()[
                - grid_copy.get_hubs()['type_fixed']].iterrows():
            vector_resulting = relaxation_df['vector_resulting'][hub]
            grid_copy.shift_node(
                node=hub,
                delta_x=vector_resulting[0] / meter_per_pixel_ratio,
                delta_y=vector_resulting[1] / meter_per_pixel_ratio,
                allow_shifting_node_outside_boundary=True)

        link_nodes(grid_copy)
        algo_run_log['time'][n] = time.time() - start_time
        algo_run_log['virtual_price'][n] = (grid_copy.price()
                                            - (number_of_virtual_hubs
                                               * household_cost))
        algo_run_log['norm_longest_shift'][n] = \
            nr_get_norm_of_longest_vector_resulting(
                relaxation_df) * meter_per_pixel_ratio
        if print_progress_bar:
            printProgressBar(n + 1, number_of_relaxation_step + 1,
                             price=(grid_copy.price() - (number_of_virtual_hubs
                                                         * household_cost)))
        list_resulting_vectors_previous_step =\
            list_resulting_vectors_current_step

    # if number_of_hill_climbers_runs is non-zero, perform hill climber runs
    if number_of_hill_climbers_runs > 0 and print_progress_bar:
        print('\n\nHill climber runs...\n')
    for i in range(number_of_hill_climbers_runs):
        printProgressBar(iteration=i,
                         total=number_of_hill_climbers_runs,
                         price=(grid_copy.price() - (number_of_virtual_hubs
                                                     * household_cost)))
        counter = 0
        for hub in grid_copy.get_hubs().index:
            counter += 1
            gradient = nr_compute_local_price_gradient(grid_copy, hub)
            nr_shift_hub_toward_minus_gradient(grid=grid_copy,
                                               hub=hub,
                                               gradient=gradient)
            if save_output:
                algo_run_log.loc[f'{algo_run_log.shape[0]}'] = [
                    time.time() - start_time,
                    grid_copy.price() - (number_of_virtual_hubs
                                         * household_cost),
                    0]

                # Save frame in video
                if save_opt_video:
                    visu.draw_grid(
                        grid=grid_copy,
                        grid_price=int(grid_copy.price()
                                       - (number_of_virtual_hubs
                                          * price_household)))
                    video.write(grid_copy.get_image())
            printProgressBar(
                iteration=i + ((counter + 1) / grid_copy.get_hubs().shape[0]),
                total=number_of_hill_climbers_runs,
                price=(grid_copy.price() - (number_of_virtual_hubs
                                            * household_cost)))

    # Set closest node to every virtual hub to meterhubs and remove virtual
    # hubs
    node_choosen_to_be_hubs = []
    for hub in grid_copy.get_hubs()[
            - grid_copy.get_hubs()['type_fixed']].index:
        closest_node = grid_copy.get_households().index[0]
        distance_to_closest_node = grid_copy.distance_between_nodes(
            hub,
            closest_node)
        for node in grid_copy.get_households().index:
            if grid_copy.distance_between_nodes(hub, node) <\
                    distance_to_closest_node:
                distance_to_closest_node = grid_copy.distance_between_nodes(
                    hub,
                    node)
                closest_node = node
        node_choosen_to_be_hubs.append(closest_node)
        grid_copy.remove_node(hub)

    for node_chosen in node_choosen_to_be_hubs:
        grid_copy.flip_node(node_chosen)
    link_nodes(grid_copy)
    visu.draw_grid(grid=grid_copy,
                   grid_price=int(grid_copy.price()))
    n_final = number_of_relaxation_step + 1
    algo_run_log['time'][n_final] = time.time() - start_time
    algo_run_log['virtual_price'][n_final] = grid_copy.price()
    algo_run_log['norm_longest_shift'][n_final] =\
        nr_get_norm_of_longest_vector_resulting(
            relaxation_df) * meter_per_pixel_ratio
    if save_output:
        if save_opt_video:
            grid_image = grid_copy.get_image()
            video.write(grid_image)
            video.write(grid_image)
            video.write(grid_image)
            video.write(grid_image)
            video.release()
        print(f"\n\nFinal price: {grid_copy.price()} $\n")

        algo_run_log.to_csv(path_to_folder + '/' + folder_name + '/log.csv')
        io.export_grid(grid=grid_copy,
                       backup_name=folder_name,
                       folder=path_to_folder,
                       save_image=save_image,
                       allow_saving_in_existing_backup_folder=True)

        # create json file containing about dictionary
        about_dict = {
            'grid id': grid_copy.get_id(),
            'number_of_hubs': number_of_hubs,
            'number_of_relaxation_step': number_of_relaxation_step,
            'damping_factor': damping_factor,
            'weight_of_attraction': weight_of_attraction,
            'first_guess_strategy': first_guess_strategy,
            'number_of_steps_bewteen_random_shifts':
                number_of_steps_bewteen_random_shifts,
            'number_of_hill_climbers_runs': number_of_hill_climbers_runs,
            'save_output': save_output,
            'output_folder': output_folder,
            'save_opt_video': save_opt_video,
            'plot_arrow_in_video': plot_arrow_in_video,
            'plot_price_evolution': plot_price_evolution,
            'print_progress_bar': print_progress_bar
        }

        json.dumps(about_dict)

        with open(path_to_folder + '/' + folder_name + '/about_run.json',
                  'w') as about:
            about.write(json.dumps(about_dict))

    if plot_price_evolution:
        plot.plot_price_evolution_for_nr_run(algo_run_log)

    # set grid equal to grid_copy

    grid.set_nodes(grid_copy.get_nodes())
    grid.set_links(grid_copy.get_links())


def nr_get_norm_of_longest_vector_resulting(relaxation_df):
    """
    This function returns the norm of the longest vector_resulting
    from the relaxation df DataFrame.

    Parameter
    ---------
        relaxation_df : :class:`pandas.core.frame.DataFrame`
            DataFrame containing all relaxation vectors for each invidiuda
            hubs.

    Output
    ------
        float
            Norm of the longest vector in vector_resulting.
    """

    norm_longest_vector = 0.0

    for index, row in relaxation_df.iterrows():
        if np.sqrt(row['vector_resulting'][0]**2
                   + row['vector_resulting'][1]**2) > norm_longest_vector:
            norm_longest_vector = np.sqrt(row['vector_resulting'][0]**2
                                          + row['vector_resulting'][1]**2)
    return norm_longest_vector


def nr_get_smaller_distance_between_nodes(grid):
    """
    This functions returns the distance between the two nodes
    from the grid that are the closest.

    Parameter
    ---------
    grid: :class:`~.grids.Grid`
        Grid object.

    Output
    ------
        float
             distance between the two nodes in [m] from the grid that are the
             closest.
    """

    smaller_distance = grid.distance_between_nodes(grid.get_nodes().index[0],
                                                   grid.get_nodes().index[1])

    node_indices = grid.get_households().index
    for i in range(len(node_indices)):
        for j in range(len(node_indices)):
            if i > j:
                if grid.distance_between_nodes(
                        node_indices[i],
                        node_indices[j]) < smaller_distance:
                    smaller_distance =\
                        grid.distance_between_nodes(node_indices[i],
                                                    node_indices[j])
    return smaller_distance


def nr_compute_relaxation_df(grid, weight_of_attraction='constant'):
    """
    This function computes the vectors between all hubs and the nodes
    that are connected to it. The Series 'vector_resulting' is the
    sum of the vector multiplied by the appropriate price per cable
    length (i.e. distribution_cable_per_meter for distribution links
    and interhub_cable_per_meter for inter-hub links).

    Parameters
    ----------
        grid: :class:`~.grids.Grid`
            Grid object.
    Output
    ------
         class:`pandas.core.frame.DataFrame`
            DataFrame containing all relaxation vectors for each invidiudal
            hubs.
    """
    # Importing required parameters

    interhub_cable_price = config_grid.getfloat('price',
                                                'interhub_cable_per_meter')
    distribution_cable_price = config_grid.getfloat(
        'price',
        'distribution_cable_per_meter')

    relaxation_df = pd.DataFrame({
        'hub': pd.Series([]),
        'connected_households': pd.Series([]),
        'connected_hubs': pd.Series([]),
        'relative_position_households': pd.Series([]),
        'relative_position_hubs': pd.Series([]),
        'vector_households': pd.Series([]),
        'vector_hubs': pd.Series([]),
        'vector_resulting': pd.Series([])
    })
    relaxation_df = relaxation_df.set_index('hub')

    for hub, row_hub in grid.get_hubs().iterrows():
        relaxation_df.loc[hub] = [
            [],
            [],
            [],
            [],
            [0, 0],
            [0, 0],
            [0, 0]]
        for link, row_link in grid.get_links().iterrows():
            if row_link['from'] == hub:
                if row_link['to'] in grid.get_hubs().index:
                    relaxation_df['connected_hubs'][hub].append(row_link['to'])
            if row_link['to'] == hub:
                if row_link['from'] in grid.get_hubs().index:
                    relaxation_df[
                        'connected_hubs'][hub].append(row_link['from'])

            if row_link['from'] == hub:
                if row_link['to'] in grid.get_households().index:
                    relaxation_df[
                        'connected_households'][hub].append(row_link['to'])
            if row_link['to'] == hub:
                if row_link['from'] in grid.get_households().index:
                    relaxation_df[
                        'connected_households'][hub].append(row_link['from'])

    for hub, row_hub in grid.get_hubs().iterrows():
        for household in relaxation_df['connected_households'][hub]:
            delta_x = (grid.get_nodes()['pixel_x_axis'][household]
                       - grid.get_nodes()['pixel_x_axis'][hub])
            delta_y = (grid.get_nodes()['pixel_y_axis'][household]
                       - grid.get_nodes()['pixel_y_axis'][hub])
            relaxation_df[
                'relative_position_households'][hub].append([delta_x, delta_y])
            relaxation_df['vector_households'][hub][0] += delta_x
            relaxation_df['vector_households'][hub][1] += delta_y

            relaxation_df['vector_resulting'][hub][0] +=\
                (delta_x * distribution_cable_price / interhub_cable_price)
            relaxation_df['vector_resulting'][hub][1] +=\
                (delta_y * distribution_cable_price / interhub_cable_price)

        for hub_2 in relaxation_df['connected_hubs'][hub]:
            delta_x = (grid.get_nodes()['pixel_x_axis'][hub_2]
                       - grid.get_nodes()['pixel_x_axis'][hub])
            delta_y = (grid.get_nodes()['pixel_y_axis'][hub_2]
                       - grid.get_nodes()['pixel_y_axis'][hub])
            relaxation_df['relative_position_hubs'][hub].append(
                [delta_x, delta_y])
            relaxation_df['vector_hubs'][hub][0] += delta_x
            relaxation_df['vector_hubs'][hub][1] += delta_y

            relaxation_df['vector_resulting'][hub][0] += delta_x
            relaxation_df['vector_resulting'][hub][1] += delta_y

    return relaxation_df


def nr_compute_local_price_gradient(grid, hub, delta=1):
    """
    This function computes the price of four neighboring configurations
    obatined by shifting the hub given as input by delta respectively
    in the positive x direction, in the negative x directtion, in the positive
    y direction and in the negative y direction. The gradient vector is
    computed as follow:
    (f(x + d, y) * e_x - f(x - d, y) * e_x
     + f(x, y + d) * e_y - f(x, y -d) * e_y)/d
     where d = delta, e_x and e_y are respectively the unit vectors in
     direction x and y and f(x, y) is the price of the grid with the hub
     given as input located at (x, y).

     Parameters
     ----------
     grid: :class:`~.grids.Grid`
        Grid object.

    hub: str
        index of the hub whose gradient is computed.

    delta: float
        Pixel distance used for computing the gradient.
    """

    # compute price of configuration with hub shifted from (delta, 0)
    grid.shift_node(node=hub,
                    delta_x=delta,
                    delta_y=0,
                    allow_shifting_node_outside_boundary=True)
    link_nodes(grid)
    price_pos_x = grid.price()

    # compute price of configuration with hub shifted from (- delta, 0)
    grid.shift_node(node=hub,
                    delta_x=- 2 * delta,
                    delta_y=0,
                    allow_shifting_node_outside_boundary=True)
    link_nodes(grid)
    price_neg_x = grid.price()

    # compute price of configuration with hub shifted from (0, delta)
    grid.shift_node(node=hub,
                    delta_x=delta,
                    delta_y=delta,
                    allow_shifting_node_outside_boundary=True)
    link_nodes(grid)
    price_pos_y = grid.price()

    # compute price of configuration with hub shifted from (0, - delta)
    grid.shift_node(node=hub,
                    delta_x=0,
                    delta_y=- 2 * delta,
                    allow_shifting_node_outside_boundary=True)
    link_nodes(grid)
    price_neg_y = grid.price()

    # Shift hub back to initial position
    grid.shift_node(node=hub,
                    delta_x=0,
                    delta_y=delta,
                    allow_shifting_node_outside_boundary=True)
    link_nodes(grid)

    gradient = ((price_pos_x - price_neg_x) / delta,
                (price_pos_y - price_neg_y) / delta)

    return gradient


def nr_shift_hub_toward_minus_gradient(grid, hub, gradient):
    """
    This function compares the price of the grid if hub is shifted by different
    amplitudes toward the negative gradient direction and performs shift
    that result in better price improvement.

    Parameters
     ----------
     grid: :class:`~.grids.Grid`
        Grid object.

    hub: str
        Index of the hub whose gradient is computed:

    gradient: tuple
        Two-dimensional vector pointing in price gradient direction.
    """

    # Store initial coordinates of hub to be shifted
    nodes = grid.get_nodes()
    links = grid.get_links()

    amplitude = 15
    price_after_shift = grid.price()
    price_before_shift = grid.price()

    counter = 0
    while price_after_shift <= price_before_shift and counter < 20:
        nodes = grid.get_nodes()
        links = grid.get_links()
        price_before_shift = grid.price()
        grid.shift_node(hub,
                        - amplitude * gradient[0],
                        - amplitude * gradient[1],
                        allow_shifting_node_outside_boundary=True)
        link_nodes(grid)
        amplitude *= 3
        counter += 1

        price_after_shift = grid.price()
    grid.set_nodes(nodes)
    grid.set_links(links)
    link_nodes(grid)
