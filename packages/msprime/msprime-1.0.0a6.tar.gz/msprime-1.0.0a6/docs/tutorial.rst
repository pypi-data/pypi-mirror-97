.. _sec_tutorial:

=============================
PORTING IN PROGRESS: Tutorial
=============================


Non-uniform recombination
-------------------------

The ``msprime`` API allows us to quickly and easily simulate data from an
arbitrary recombination map.
To do this, we can specify an external recombination map as a
:meth:`msprime.RecombinationMap` object.
We need to supply a list of ``positions`` in the map, and a list showing ``rates``
of crossover between each specified position.

In the example below, we specify a recombination map with distinct recombination rates between each 100th base.

.. code-block:: python

    # Making a simple RecombinationMap object.
    map_positions = [i*100 for i in range(0, 11)]
    map_rates = [0, 1e-4, 5e-4, 1e-4, 0, 0, 0, 5e-4, 6e-4, 1e-4, 0]
    my_map = msprime.RecombinationMap(map_positions, map_rates)
    # Simulating with the recombination map.
    ts = msprime.simulate(sample_size = 6, random_seed = 12, recombination_map = my_map)

The resulting tree sequence has no interval breakpoints between positions 400 and 700,
as our recombination map specified a crossover rate of 0 between these positions.

.. code-block:: python

    for tree in ts.trees():
        print("-" * 20)
        print("tree {}: interval = {}".format(tree.index, tree.interval))
        print(tree.draw(format="unicode"))

    # --------------------
    # tree 0: interval = (0.0, 249.0639823488891)
    #    11
    #  ┏━━┻━━┓
    #  ┃     9
    #  ┃   ┏━┻━┓
    #  8   ┃   ┃
    # ┏┻┓  ┃   ┃
    # ┃ ┃  ┃   7
    # ┃ ┃  ┃  ┏┻┓
    # ┃ ┃  6  ┃ ┃
    # ┃ ┃ ┏┻┓ ┃ ┃
    # 2 5 0 1 3 4
    #
    # --------------------
    # tree 1: interval = (249.0639823488891, 849.2285335049714)
    #    12
    # ┏━━━┻━━━┓
    # ┃      11
    # ┃    ┏━━┻━┓
    # ┃    9    ┃
    # ┃  ┏━┻━┓  ┃
    # ┃  ┃   7  ┃
    # ┃  ┃  ┏┻┓ ┃
    # ┃  6  ┃ ┃ ┃
    # ┃ ┏┻┓ ┃ ┃ ┃
    # 5 0 1 3 4 2
    #
    # --------------------
    # tree 2: interval = (849.2285335049714, 1000.0)
    #   12
    # ┏━━┻━━┓
    # ┃    11
    # ┃  ┏━━┻━┓
    # ┃  ┃   10
    # ┃  ┃  ┏━┻┓
    # ┃  ┃  ┃  7
    # ┃  ┃  ┃ ┏┻┓
    # ┃  6  ┃ ┃ ┃
    # ┃ ┏┻┓ ┃ ┃ ┃
    # 5 0 1 2 3 4


A more advanced example is included below.
In this example we read a recombination
map for human chromosome 22, and simulate a single replicate. After
the simulation is completed, we plot histograms of the recombination
rates and the simulated breakpoints. These show that density of
breakpoints follows the recombination rate closely.

.. code-block:: python

    import numpy as np
    import scipy.stats
    import matplotlib.pyplot as pyplot

    def variable_recomb_example():
        infile = "hapmap/genetic_map_GRCh37_chr22.txt"
        # Read in the recombination map using the read_hapmap method,
        recomb_map = msprime.RecombinationMap.read_hapmap(infile)

        # Now we get the positions and rates from the recombination
        # map and plot these using 500 bins.
        positions = np.array(recomb_map.get_positions()[1:])
        rates = np.array(recomb_map.get_rates()[1:])
        num_bins = 500
        v, bin_edges, _ = scipy.stats.binned_statistic(
            positions, rates, bins=num_bins)
        x = bin_edges[:-1][np.logical_not(np.isnan(v))]
        y = v[np.logical_not(np.isnan(v))]
        fig, ax1 = pyplot.subplots(figsize=(16, 6))
        ax1.plot(x, y, color="blue")
        ax1.set_ylabel("Recombination rate")
        ax1.set_xlabel("Chromosome position")

        # Now we run the simulation for this map. We simulate
        # 50 diploids (100 sampled genomes) in a population with Ne=10^4.
        tree_sequence = msprime.simulate(
            sample_size=100,
            Ne=10**4,
            recombination_map=recomb_map)
        # Now plot the density of breakpoints along the chromosome
        breakpoints = np.array(list(tree_sequence.breakpoints()))
        ax2 = ax1.twinx()
        v, bin_edges = np.histogram(breakpoints, num_bins, density=True)
        ax2.plot(bin_edges[:-1], v, color="green")
        ax2.set_ylabel("Breakpoint density")
        ax2.set_xlim(1.5e7, 5.3e7)
        fig.savefig("hapmap_chr22.svg")


.. image:: _static/hapmap_chr22.svg
   :width: 800px
   :alt: Density of breakpoints along the chromosome.


.. warning::
    Beware that this matrix might be very big (bigger than the tree
    sequence it's extracted from, in most realistically-sized
    simulations!)


Comparing to analytical results
*******************************

.. todo:: It's not clear whether it's worth having this content
    here in the msprime repo or we should have a separate tutorial
    for this sort of thing as part of the "tutorials" section of the
    overall website.

A common task for coalescent simulations is to check the accuracy of analytical
approximations to statistics of interest. To do this, we require many independent
replicates of a given simulation. ``msprime`` provides a simple and efficient
API for replication: by providing the ``num_replicates`` argument to the
:func:`.simulate` function, we can iterate over the replicates
in a straightforward manner. Here is an example where we compare the
analytical results for the number of segregating sites with simulations:

.. literalinclude:: examples/segregating_sites.py

Running this code, we get:

.. code-block:: python

    segregating_sites(10, 5, 100000)
    #          mean              variance
    # Observed      14.17893          53.0746740551
    # Analytical    14.14484          52.63903


Note that in this example we set :math:`N_e = 0.5` and
the mutation rate to :math:`\theta / 2` when calling :func:`.simulate`.
This works because ``msprime`` simulates Kingman's coalescent,
for which :math:`N_e` is only a time scaling;
since :math:`N_e` is the diploid effective population size,
setting :math:`N_e = 0.5` means that the mean time for two samples to coalesce
is equal to one time unit in the resulting trees.
This is helpful for converting the diploid per-generation time units
of msprime into the haploid coalescent units used in many
theoretical results. However, it is important to note that conventions
vary widely, and great care is needed with such factor-of-two
rescalings.



In the following example, we calculate the mean coalescence time for
a pair of lineages sampled in different subpopulations in a symmetric island
model, and compare this with the analytical expectation.


.. literalinclude:: examples/migration.py

Again, we set :math:`N_e = 0.5` to agree with convention in theoretical results,
where usually one coalescent time unit is, in generations, the effective number of *haploid* individuals.
Running this example we get:

.. code-block:: python

    migration_example()
    # Observed  = 3.254904176088153
    # Predicted = 3.25


.. _sec_advanced_features:

Dead sections
*************
