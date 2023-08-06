"""Plugin to load real time Kafka streams into atoti stores.

This package is required to use :meth:`atoti.store.Store.load_kafka`.

It can be installed with pip or conda:

  * .. code-block:: bash

      pip install atoti[kafka]

  * .. code-block:: bash

      conda install atoti-kafka
"""

from ._custom import create_deserializer
from ._deserializer import JSON_DESERIALIZER as _JSON_DESERIALIZER
from ._version import VERSION as __version__

JSON_DESERIALIZER = _JSON_DESERIALIZER
"""Core JSON deserializer.

Each JSON object corresponds to a row of the store, keys of the JSON object must match columns of the store.
"""

__all__ = ["create_deserializer", "JSON_DESERIALIZER"]
