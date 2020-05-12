# website-availability-checker

Services to check availability and send messages via Kafka, consumer storing in Postgres.

## Development

These services were developed against Python 3.8. Please configure your editor to use the `black` formatter, with `flake8` linter rules.

### Pre-commit Hooks

To ensure quality code, please install pre-commit:
1. `pip install pre-commit`
2. `pre-commit install`


## Systems setup

This relies on Kafka and Postgres. You can set them up using a DBaaS provider such as Aiven, or run locally. By default, SSL connections are enabled for Kafka.

1. Set up Kafka and Postgres.
2. Download Kafka CA and Certificates into the `certs` directory. There should be three files:
    - `ca.pem`
    - `service.cert`
    - `service.key`
3. Set up the topic on Kafka that you want to use (e.g. `website-monitoring`).
4. Set up environment variables, for instance in a `.env` file:
    - `KAFKA_ENDPOINT`: Full URL, including port, of the Kafka service.
    - `POSTGRES_ENDPOINT`: Full URL, including username, password, and port, of the Postgres service.


## Environment Variables

The following environment variables can be used to configure the services:

- `KAFKA_ENDPOINT`: Full URL, including port, of the Kafka service.
- `KAFKA_CERT_DIR`: Directory containing the 3 certificates needed to connect to Kafka. Defaults to `./certs`.
- `KAFKA_TOPIC`: Kafka topic for the consumers/producers to use. Defaults to: `website-monitoring`.
- `KAFKA_CLIENT_ID`: Kafka client ID. Defaults to `website-monitoring-client`.
- `KAFKA_GROUP_ID`: Kafka group ID. Defaults to `website-monitoring-group`.
- `KAFKA_USE_SSL`: Flag to enable/disable SSL connections to Kafka. Set to `false` to disable SSL, defaults to enabled.
- `CHECK_TIMEOUT`: Floating-point seconds before timing out the connection to the website. Defaults to 1 second.
- `POSTGRES_ENDPOINT`: Full URL, including username, password, and port, of the Postgres service.

## Running

### Locally

0. Set up a Python 3 virtual environment if you haven't already
1. Install dependencies with `pip install -r requirements.txt`
2. Run `python3 -m wac.monitor <url>` where `<url>` is the URL you want to monitor.

You can also specify a different interval with `--period` and the number of seconds (default is equivalent to `--period 10`)

### Docker

With docker-compose, you can run the entire application by running `docker-compose up`.
This will load the current directory, into the container, including the source code, so put the certificates in the `certs` directory.
See the "Systems setup" section above.


## Design Decisions

### Single codebase

Normally, it's best to split code to focus on a single concern. In this case, there are effectively two apps: The monitoring code and the DB storage code.
In order to keep things simple enough for this demo, there's some shared code and it's all in a single repo and single deliverable.

If this project were to grow, at some point the two sub-systems would be split to allow for independence, but the trade-off would be time spent maintaining
infrastructure that manages the credentials to Kafka, packaging and delivering the two components, and so on.

### Shared Docker Image

Similarly, a shared Docker image allows for easier packaging, a single requirements file, and more closely matching the dev environment.
Again, for better dependency management, it would make sense to split these if the project were to grow. The Postgres dependency isn't needed
for the website monitoring, and the requests library isn't needed to store Kafka messages in Postgres, but for simplicity it's quick enough
to just bundle it all together right now as a proof-of-concept. It also keeps the CI/CD pipeline much easier for now.
