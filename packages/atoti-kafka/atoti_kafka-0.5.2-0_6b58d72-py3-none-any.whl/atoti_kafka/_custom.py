import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from ._deserializer import KafkaDeserializer


@dataclass(frozen=True)
class CustomDeserializer(KafkaDeserializer):
    """Deserializer implemented in Python."""

    callback: Callable[[str], Mapping[str, Any]]
    batch_size: int

    def deserialize(self, data: str) -> str:
        """Deserialize JSON bytes in a string.

        Args:
            data: String that can be parsed as JSON.
                Keys are ids and values are strings containing Kafka value's message part.

        Returns:
            Stringified array of strings: ``{1: {field_1: ***, field_2: ***, ...}, 2: {***}, ...}``.
        """
        data_json = json.loads(data)

        try:
            result = {}
            for row_id, json_row in data_json.items():
                row = self.callback(json_row)
                result[row_id] = row
            return json.dumps(result)
        except KeyError as error:
            raise ValueError(
                "Error in custom deserializer: Missing field in datastore"
            ) from error

    def toString(self) -> str:  # pylint: disable=invalid-name
        """Get the name of the deserializer."""
        return self.name

    class Java:
        """Code needed for Py4J callbacks."""

        implements = ["io.atoti.loading.kafka.impl.serialization.IPythonDeserializer"]


def create_deserializer(
    callback: Callable[[str], Mapping[str, Any]], *, batch_size: int = 1
) -> KafkaDeserializer:
    """Return a custom Kafka deserializer.

    Example:
        Considering a store with colums ``c_1``, ``c_2`` and  ``c_3``, for Kafka records shaped like:

        * ``{"c_1": v_1, "c_2": v_2, "c_3": v_3}``, this callback would work::

            columns = store.columns
            def callback(record: str):
                values = json.loads(record)
                return {column: values[column] for column in columns}

        * ``v_1, v_2, v_3``, this callback would work::

            columns = store.columns
            def callback(record: str):
                values = record.split(", ")
                return {column: values[index] for index, column in enumerate(columns)}

    Args:
        callback: Function taking the record as a string and returning a mapping from a store column name to its value.
        batch_size: Size of the batch of records.

            If ``batch_size > 1`` the records will be batched then deserialized when either the batch size is reached or the `batch_duration` passed in :meth:`atoti.store.Store.load_kafka` has ellapsed.
            A bigger batch size means a higher latency but less store transactions so often better performance.
    """
    return CustomDeserializer("PythonDeserializer", callback, batch_size)
