#!/bin/bash
# Setup script for Pub/Sub Emulator local development

export PUBSUB_EMULATOR_HOST=localhost:8085
export CLOUDSDK_API_ENDPOINT_OVERRIDES_PUBSUB=http://localhost:8085/
export CLOUDSDK_CORE_PROJECT=aegis-local
PROJECT_ID=aegis-local
EMULATOR_URL="http://localhost:8085/v1/projects/${PROJECT_ID}"

echo "Starting Pub/Sub Emulator..."
docker-compose up -d pubsub-emulator

echo "Waiting for emulator to be ready..."
sleep 5

ensure_topic() {
  local topic="$1"
  echo "Creating topic (idempotent): $topic"
  curl -s -X PUT "$EMULATOR_URL/topics/$topic" >/dev/null
}

ensure_subscription() {
  local subscription="$1"
  local topic="$2"
  echo "Creating subscription (idempotent): $subscription"
  curl -s -X PUT -H "Content-Type: application/json" \
    -d "{\"topic\":\"projects/${PROJECT_ID}/topics/${topic}\"}" \
    "$EMULATOR_URL/subscriptions/$subscription" >/dev/null
}

echo "Creating topics (idempotent)..."
ensure_topic "aegis-test.test-generation.started"
ensure_topic "aegis-test.test-planning.completed"
ensure_topic "aegis-test.test-planning.failed"

echo "Creating subscriptions (idempotent)..."
ensure_subscription "test-planner.aegis-test.test-generation.started" "aegis-test.test-generation.started"
ensure_subscription "orchestrator.aegis-test.test-planning.completed" "aegis-test.test-planning.completed"
ensure_subscription "orchestrator.aegis-test.test-planning.failed" "aegis-test.test-planning.failed"

echo ""
echo "✅ Pub/Sub Emulator is ready!"
echo ""
echo "Your .env should have:"
echo "  AEGIS_MESSAGING_BACKEND=pubsub"
echo "  AEGIS_MESSAGING_PUBSUB_PROJECT_ID=${PROJECT_ID}"
echo "  AEGIS_MESSAGING_PUBSUB_EMULATOR_HOST=localhost:8085"
echo ""
echo "To run the agent:"
echo "  poetry run python main.py"
