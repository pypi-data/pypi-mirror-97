from __future__ import annotations

from typing import TYPE_CHECKING, Mapping, Optional

from atoti._sources import DataSource

from ._custom import CustomDeserializer
from ._deserializer import JSON_DESERIALIZER, KafkaDeserializer

if TYPE_CHECKING:
    from atoti._java_api import JavaApi
    from atoti.store import Store


class KafkaDataSource(DataSource):
    """Kafka data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "KAFKA")

    def load_kafka_into_store(
        self,
        store: Store,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        value_deserializer: KafkaDeserializer,
        batch_duration: int,
        consumer_config: Mapping[str, str],
    ):
        """Consume a Kafka topic and stream its records in an existing store."""
        params = {
            "bootstrapServers": bootstrap_servers,
            "topic": topic,
            "consumerGroupId": group_id,
            "keyDeserializerClass": "org.apache.kafka.common.serialization.StringDeserializer",
            "batchDuration": batch_duration,
            "additionalParameters": consumer_config,
        }
        if isinstance(value_deserializer, CustomDeserializer):
            params["pythonValueDeserializer"] = value_deserializer
            params["batchSize"] = value_deserializer.batch_size
        else:
            params["valueDeserializerClass"] = value_deserializer.name
        self.load_data_into_store(store.name, None, False, True, False, params)


def load_kafka(
    self: Store,
    bootstrap_server: str,
    topic: str,
    *,
    group_id: str,
    batch_duration: int = 1000,
    consumer_config: Optional[Mapping[str, str]] = None,
    deserializer: KafkaDeserializer = JSON_DESERIALIZER,
):  # noqa: D417
    """Consume a Kafka topic and stream its records in the store.

    Note:
        This method requires the :mod:`atoti-kafka <atoti_kafka>` plugin.

    The records' key deserializer default to `StringDeserializer <https://kafka.apache.org/21/javadoc/org/apache/kafka/common/serialization/StringDeserializer.html>`_.

    Args:
        bootstrap_server: ``host[:port]`` that the consumer should contact to bootstrap initial cluster metadata.
        topic: Topic to subscribe to.
        group_id: The name of the consumer group to join.
        batch_duration: Milliseconds spent batching received records before publishing them to the store.
            If ``0``, received records are immediately published to the store.
            Must not be negative.
        consumer_config: Mapping containing optional parameters to set up the KafkaConsumer.
            The list of available params can be found `here <https://kafka.apache.org/10/javadoc/index.html?org/apache/kafka/clients/consumer/ConsumerConfig.html>`_.
        deserializer: Deserialize Kafka records' value to atoti store rows.
            Use :meth:`atoti_kafka.create_deserializer` to create custom ones.
    """
    KafkaDataSource(
        self._java_api  # pylint: disable=protected-access
    ).load_kafka_into_store(
        self,
        bootstrap_server,
        topic,
        group_id,
        deserializer,
        batch_duration,
        consumer_config if consumer_config is not None else {},
    )
