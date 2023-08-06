"""Plugin to load CSV and parquet files from Google Cloud Storage into atoti stores.

This package is required to load files with GCP paths starting with ``gs://``.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[gcp]

  * .. code-block:: bash

      conda install atoti-gcp

Authentication is handled by the underlying GCS SDK for Java library.
Automatic credentials retrieval is explained in `their documentation <https://cloud.google.com/docs/authentication/production#automatically>`_.
"""

from ._version import VERSION as __version__
