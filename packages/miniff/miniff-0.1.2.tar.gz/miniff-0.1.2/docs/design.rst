Miniff Design Documentation
===========================

Structure
---------

The project includes several modules performing energy and gradients computations, potential parameter optimization
through machine learning, simple geometry optimization and presentation utilities.

- ``potentials``: a core module implementing smooth classical interatomic potentials and descriptors. The module includes
  ``LocalPotentialFamily``: a factory for constructing parameterized ``LocalPotential`` objects which, in turn, include
  all necessary data and interfaces to compute atomic energies and gradients. Several pre-built potential forms are
  provided through instantiating ``LocalPotentialFamily``: for example, ``lj_potential_family`` (Lenard-Jones pair
  potential) or ``behler5_descriptor_family`` (Behler type 5 angular descriptor).

- ``kernel``: implements a ``NeighborWrapper`` class which computes neighbor information from atomic coordinate data and
  prepares contiguous data buffers which can be processed by ``LocalPotential``s.
  ``NeighborWrapper`` is implemented with 3D periodic boundary conditions in mind to model amorphous materials. However,
  it also supports molecular systems without any overhead. ``NeighborWrapper`` also implements a key interface
  ``NeighborWrapper.eval`` which, for a given structure and a list of potentials, computes total energy and gradients.
  ``NeighborWrapper.relax`` introduces a toy interface for structural relaxation using ``scipy`` minimizers.
 
- ``ml``: implements machine learning potentials.

  - ``ml.Dataset`` is the key container for atomic descriptors, energies and gradients. It ensures that all dataset pieces
    are ``torch.Tensor``s compatible with each other. ``ml.Dataset`` includes two large blocks of data, namely one
    ``ml.PerCellDataset`` block with target energies and energy gradients, and one or more ``ml.PerPointDataset``s with
    descriptor information.
  - ``ml.Normalization`` implements normalization of datasets in a physically reasonable way.
  - ``ml.learn_cauldron`` is a typical entry point for dataset creation which includes reasonable default values.
  - ``ml.SequentialSoleEnergyNN`` is Behler et al. suggestion for the neural network potential form.
  - ``ml.forward_cauldron`` is the core routine for machine-learning optimization. It combines dataset and neural-network
    models to produce the energy and gradients prediction.
  - ``ml.NNPotential`` is a neural-network potential subclassing ``potentials.LocalPotential``.
  
  ``miniff.ml`` is built around ``pytorch``.
  
- ``ml_util``: includes reasonable recipes for optimizing neural networks from ``ml``.

  - ``ml_util.simple_energy_closure`` provides defaults for running the optimization with `LBFGS`.
  - ``ml_util.*Workflow`` are workflow classes for optimizing neural-network potentials. These classes
    accumulate and re-distribute many parameters related to the dataset organization, potential form and optimizatin process.

- ``presentation``: various handy plotting routines to present potentials and visualize machine learning optimization
  process.

Deployment
----------

`miniff` can be deployed on high-performance computing (HPC) clusters.

Parallelism
^^^^^^^^^^^

- ``miniff`` takes a full advantage of GPU parallelism in ``pytorch``. Please note that it is often not enough to install
  pre-built bundles of ``pytorch`` as they support only a limited set of (very recent) GPU drivers. If your HPC hardware
  does not feature those you have several options:

  - It is best to ask your HPC support team for a suitable ``pytorch`` build specifically for the HPC machine. Such builds
    may be available through ``module`` script or other ways to manage the runtime environment on the cluster: please
    investigate such options first.
  - The second possibility is to use an older ``pytorch`` version which bundles kernels for older GPUs. ``miniff`` does its
    best to support a wide range of ``pytorch`` versions but you have to test the compatibility manually in your case.
  - The last possibility is to build ``pytorch`` manually. This is the most tedious approach, thus, not recommended for
    unexperienced users.

- OpenMP threading support is present in potential and gradient computations. This may be useful for computing energies
  and gradients in large atomic systems. The number of threads is controlled by usual means such as ``OMP_NUM_THREADS``
  environment variable. For small atomic systems ``~100`` atoms up to 2-4 threads are beneficial: make sure your parallel
  cluster setup is reasonable.
