"""Plugin to load CSV and Parquet files from AWS S3 into atoti stores.

This package is required to load files with paths starting with ``s3://``.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[aws]

  * .. code-block:: bash

      conda install atoti-aws

Authentication is handled by the underlying AWS SDK for Java library.
Refer to their `documentation <https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html#setup-credentials-setting>`_  for the available options.

See Also:
    :func:`atoti.config.create_aws_config` to configure how atoti interacts with AWS.
"""

from ._version import VERSION as __version__
