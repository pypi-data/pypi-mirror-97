Datasets
=========

Ageing Drosophila Brain
~~~~~~~~~~~~~~~~~~~~~~

This is sourced from `Davie et al.`_ (*Cell* 2018, `GSE 107451`_) and contains scRNA-seq data from a collection of fly brain cells along with each cell's age (in days). It is a useful dataset for exploring a common scenario in multi-modal integration: scRNA-seq data aligned to a 1-dimensional secondary modality.

.. code-block:: Python

   import schema
   adata = schema.datasets.fly_brain()


Next Datasets
~~~~~~~~~~~~~

.. code-block:: Python

    from schema import SchemaQP

Coming soon: example datasets from Sci-CAR,  10x ATAC+scRNA, SlideSeq etc. 



.. _Davie et al.: https://doi.org/10.1016/j.cell.2018.05.057
.. _GSE 107451: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE107451
