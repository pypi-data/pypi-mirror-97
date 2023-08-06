r"""Plugin to load CSV and parquet files from Azure Blob Storage into atoti stores.

This package is required to load files with path like ``https://{ACCOUNT_NAME}.blob.core.windows.net/path/to/data-*``.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[azure]

  * .. code-block:: bash

      conda install atoti-azure

Authentication is done with a `connection string <https://docs.microsoft.com/en-us/azure/storage/common/storage-configure-connection-string?toc=/azure/storage/blobs/toc.json#store-a-connection-string>`_ that will be read from the ``AZURE_CONNECTION_STRING`` environment variable or, if it does not exist, from the file at ``~/.azure/credentials`` (``C:\\Users\\{USERNAME}\\.aws\\credentials`` on Windows).

See Also:
    :func:`atoti.config.create_azure_config` to configure how atoti interacts with Azure.
"""

from ._version import VERSION as __version__
