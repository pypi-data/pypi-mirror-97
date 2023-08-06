Introduction
============

Glossary
--------

- **atom**, **point**: a vector in real (typically, 3D) space defining the location and the metadata associated with
  this location. This gives us information about an individual small object in space.

  .. figure:: /images/glossary/atom.svg

- **structure**, **cell**, **box**: a set of *points* enclosed into a parallelogram and representing a snapshot of
  atoms in media (molecular, solid, liquid, etc.). A **box** is a way to describe how multiple *atoms* share the
  same space. This can simply be a list of coordinates, for example. Related classes: ``miniff.kernel.Cell``,
  ``miniff.kernel.NeighborWrapper``.

  .. figure:: /images/glossary/structure.svg

- **potential**, **interaction**, **spring**: a protocol (a function) taking atomic coordinates of two or three *atoms*
  (optionally, matching a set of conditions) and producing a single floating-point number. For example, **potentials**
  may describe how strongly atoms interact with each other.

  .. figure:: /images/glossary/potential.svg

- **atomic environment**: a single *point* picked in a *structure*. **Atomic environment** is a very abstract way of
  telling which *interactions* are important and how *atoms* are grouped by these interactions.

  .. figure:: /images/glossary/environment.svg

- **partial energy**, **atomic energy**, **potential energy**: a sum of all *interaction* values the chosen atom participates
  in. The **potential energy** value may be subject to double-counting issues when a single *potential* is shared
  between many atoms. Related classes: ``miniff.potentials.LocalPotential``, ``miniff.ml.NNPotential``.

  .. figure:: /images/glossary/partial-energy.svg

- **machine learning (ML) potential**: a variant of the *partial energy* where the sum is replaced by a more complex
  process involving machine learning techniques.

  .. figure:: /images/glossary/ml-potential.svg

- **(total) energy**: a sum of all *atomic energies* defining the cumulative energy accumulated in the *structure* and
  originating from attractions and repulsions of individual *atoms*. Predicting **total energy** from **structures** is
  the primary purpose of this package.

  .. figure:: /images/glossary/total-energy.svg

- **(total) energy landscape**: *total energy* as a function of one or more parameters of a *structure*. It is simply a way
  to look at the *total energy* as a scalar function of many variables.

  .. figure:: /images/glossary/potential-landscape.svg

- **(total) energy minimum**: a *structure* and the corresponding *total energy* minimum of the *potential landscape*.
  Finding *potential energy minimum* is one of the primary purposes of the *total energy* description.

  .. figure:: /images/glossary/total-energy-minimum.svg

- **charge**: a scalar belonging to *atomic* metadata with the properties of *partial energy*. **Charges** are used to
  treat long-range *potentials* which cannot be described by *atomic environments*. **Charges** are not necessary
  physical (Coulomb) charges: they may also be electronegativities or any other scalar property of an *atom*.

- **force**, **stress**: negative gradients of the *total energy* with respect to coordinates describing *structures*.
  *Forces* indicate the direction in a multidimensional space where the *total energy* becomes smaller.

  .. figure:: /images/glossary/force.svg

- **descriptors**: a special sort of *potential energy* intended to describe *atomic environments*. Descriptors
  are typically defined by *local environments*. Unlike *potentials*, **descriptor** functions usually have a simple
  smooth form.
