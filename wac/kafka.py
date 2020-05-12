from pathlib import Path

import msgpack
from kafka import KafkaConsumer, KafkaProducer

from . import config


def get_ssl_args() -> dict:
    ssl_dir = Path(config.KAFKA_CERT_DIR)
    return (
        {
            "security_protocol": "SSL",
            "ssl_cafile": str(ssl_dir / "ca.pem"),
            "ssl_certfile": str(ssl_dir / "service.cert"),
            "ssl_keyfile": str(ssl_dir / "service.key"),
        }
        if config.KAFKA_USE_SSL
        else {}
    )


def get_producer() -> KafkaProducer:
    ssl_args = get_ssl_args()
    return KafkaProducer(
        bootstrap_servers=config.KAFKA_ENDPOINT,
        max_block_ms=10000,
        value_serializer=msgpack.packb,
        **ssl_args
    )


def get_consumer() -> KafkaConsumer:
    ssl_args = get_ssl_args()
    return KafkaConsumer(
        config.KAFKA_TOPIC,
        auto_offset_reset="earliest",
        bootstrap_servers=config.KAFKA_ENDPOINT,
        client_id=config.KAFKA_CLIENT_ID,
        enable_auto_commit=False,  # Commit will happen after each message to sync with DB
        group_id=config.KAFKA_GROUP_ID,
        value_deserializer=msgpack.unpackb,
        **ssl_args
    )
