import logging
import time

import click
import requests
import schedule

from . import config, kafka

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def monitor_to_kafka(producer: kafka.KafkaProducer, url: str):
    data = check_url(url)
    producer.send(config.KAFKA_TOPIC, data)


def check_url(url: str) -> dict:
    data = {"url": url, "timestamp": time.time()}
    try:
        response = requests.get(url, timeout=config.CHECK_TIMEOUT)
    except requests.RequestException as e:
        data["error"] = repr(e)
        logger.exception(f"Error fetching status")
    else:
        data["status_code"] = response.status_code
        data["response_time"] = response.elapsed.total_seconds()
        logger.info(
            f"Status code: {response.status_code}, response time: {data['response_time']}"
        )
    return data


@click.command()
@click.argument("url")
@click.option("--period", default=10, help="Check every X seconds.")
def main(url: str, period: int):
    logger.info(f"Monitoring {url} every {period} seconds ...")
    producer = kafka.get_producer()

    # Run once to avoid waiting 10 seconds for first results
    monitor_to_kafka(producer=producer, url=url)

    schedule.every(10).seconds.do(monitor_to_kafka, producer=producer, url=url)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
