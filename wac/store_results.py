import logging

from . import config, kafka, pgsql

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def kafka_to_postgres(sql_conn, topic: str = config.KAFKA_TOPIC):
    consumer = kafka.get_consumer()
    # Note: Should run infinitely
    for msg in consumer:
        logger.info(f"Storing: {msg.value}")
        # Set up DB transaction
        with sql_conn:
            with sql_conn.cursor() as cursor:
                pgsql.insert_data(cursor, **msg.value)
                consumer.commit()


def main():
    logger.info(f"Monitoring Kafka Topic {config.KAFKA_TOPIC}")
    sql_conn = pgsql.connect()
    # Try-finally to make sure connection closes on unhandled exception
    try:
        pgsql.setup_table(sql_conn)
        kafka_to_postgres(sql_conn)
    finally:
        sql_conn.close()


if __name__ == "__main__":
    main()
