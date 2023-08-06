Tutorial
========

This tutorial will guide you through the basics of **Qty**.

#. Install **Qty** (see :ref:`Installation`).
#. Import the relevant classes from the ``qty`` module. This tutorial uses units of energy.

   .. code-block:: python
      :lineno-start: 1

      >>> from qty import Energy

#. Instantiate a quantity object.

   .. code-block:: python
      :lineno-start: 2

      >>> quantity = Energy()

#. Assign a value to the quantity object using one of the available units. Each unit is implemented as a descriptor that includes a setter and a getter. The setter converts and stores the quantity to the base units of the class. For example, the base units of the ``Energy`` class are joules (J). The getter converts and returns the quantity in the desired units.

   .. code-block:: python
      :lineno-start: 3

      >>> quantity.meV = 1600.

   .. note::
      The units are implemented as descriptors and are therefore assigned and accessed without arguments.

#. To obtain the quantity in different units, simply access the corresponding attribute.

   .. code-block:: python
      :lineno-start: 4

      >>> quantity.nm
      774.9012402075016
   
