# Aegis Test Agents

Autonomous, event-driven Python agents for the Aegis Test platform.

## Quick Start

### 1. Setup Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

### 2. Configure for Pub/Sub (GCP)

#### Prerequisites
- GCP project with Pub/Sub enabled
- Service account JSON credentials

#### Environment Setup

Edit `.env`:

```env
AEGIS_MESSAGING_BACKEND=pubsub
AEGIS_MESSAGING_PUBSUB_PROJECT_ID=your-gcp-project-id
```

Set GCP credentials:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

#### Create Topic and Subscription (GCP Console or gcloud CLI)

```bash
# Create topic
gcloud pubsub topics create aegis-test.test-generation.started

# Create subscription
gcloud pubsub subscriptions create test-planner.aegis-test.test-generation.started \
  --topic=aegis-test.test-generation.started
```

### 3. Run the Agent

```bash
poetry run python main.py
```

The agent will now listen for messages on the `test-planner.aegis-test.test-generation.started` subscription.

---

## Testing Locally with Pub/Sub Emulator

### Install and Start Emulator

```bash
# Install gcloud CLI and emulator
gcloud components install pubsub-emulator

# Start emulator in another terminal
gcloud beta emulators pubsub start --host-port=localhost:8085
```

### Configure Emulator in .env

```env
AEGIS_MESSAGING_BACKEND=pubsub
AEGIS_MESSAGING_PUBSUB_PROJECT_ID=test-project
AEGIS_MESSAGING_PUBSUB_EMULATOR_HOST=localhost:8085
```

### Create Topic and Subscription (Emulator)

```bash
# Create topic
gcloud pubsub topics create aegis-test.test-generation.started \
  --project=test-project

# Create subscription
gcloud pubsub subscriptions create test-planner.aegis-test.test-generation.started \
  --topic=aegis-test.test-generation.started \
  --project=test-project
```

### Publish Test Message

```bash
gcloud pubsub topics publish aegis-test.test-generation.started \
  --message='{"execution_id": "test-123", "specification_id": "spec-456"}' \
  --project=test-project
```

### Run Agent

```bash
poetry run python main.py
```

---

## Switching Backends

### RabbitMQ

```env
AEGIS_MESSAGING_BACKEND=rabbitmq
AEGIS_MESSAGING_RABBITMQ_HOST=localhost
AEGIS_MESSAGING_RABBITMQ_PORT=5672
AEGIS_MESSAGING_RABBITMQ_USER=guest
AEGIS_MESSAGING_RABBITMQ_PASSWORD=guest
```

Then run:

```bash
poetry run python main.py
```

---

## Architecture

```
src/aegis_agents/
├── shared/
│   └── messaging/
│       ├── topics.py          # Centralized topic definitions
│       ├── config.py          # Configuration from env vars
│       ├── factory.py         # Factory to create pub/sub clients
│       ├── interfaces.py      # Abstract interfaces
│       └── backends/
│           ├── rabbitmq.py    # RabbitMQ implementation
│           └── pubsub.py      # Google Cloud Pub/Sub implementation
│
├── test_planner/              # Test planner agent
├── test_generator/            # Test generator agent
├── test_executor/             # Test executor agent
└── test_analyzer/             # Test analyzer agent
```

---

## Adding New Topics

Edit [src/aegis_agents/shared/messaging/topics.py](src/aegis_agents/shared/messaging/topics.py) and add a new `MessagingDestination`:

```python
class Topics:
    MY_NEW_TOPIC = MessagingDestination(
        name="my-new-topic",
        rabbitmq=RabbitMQDestination(
            queue="aegis-test.my-topic.started",
            exchange="aegis-test.my-topic.exchange",
            routing_key="my.topic.started",
        ),
        pubsub=PubSubDestination(
            topic="aegis-test.my-topic.started",
            subscription="my-agent.aegis-test.my-topic.started",
        ),
    )
```

---

## Publishing Messages

```python
from aegis_agents.shared.messaging import MessagingFactory, Topics

publisher = MessagingFactory.create_publisher()
await publisher.connect()

await publisher.publish(
    Topics.TEST_GENERATION_STARTED,
    {"execution_id": "123", "specification_id": "456"},
    correlation_id="corr-789"
)

await publisher.disconnect()
```

---

## Subscribing to Topics

```python
from aegis_agents.shared.messaging import MessagingFactory, Topics

async def my_handler(message: dict, correlation_id: str | None):
    print(f"Received: {message}")

subscriber = MessagingFactory.create_subscriber()
await subscriber.connect()
await subscriber.subscribe(Topics.TEST_GENERATION_STARTED, my_handler)
await subscriber.start_consuming()
```

---

## Development

Install dependencies:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

Format code:

```bash
poetry run black src tests
```

Lint code:

```bash
poetry run ruff check src tests
```
