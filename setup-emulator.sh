#!/bin/bash
# Setup script for Pub/Sub Emulator local development

export PUBSUB_EMULATOR_HOST=localhost:8085
export CLOUDSDK_API_ENDPOINT_OVERRIDES_PUBSUB=http://localhost:8085/

echo "Starting Pub/Sub Emulator..."
docker-compose up -d pubsub-emulator

echo "Waiting for emulator to be ready..."
sleep 5

echo "Creating topic: aegis-test.test-generation.started"
gcloud pubsub topics create aegis-test.test-generation.started \
  --project=local-project

echo "Creating subscription: test-planner.aegis-test.test-generation.started"
gcloud pubsub subscriptions create test-planner.aegis-test.test-generation.started \
  --topic=aegis-test.test-generation.started \
  --project=local-project

echo ""
echo "✅ Pub/Sub Emulator is ready!"
echo ""
echo "Your .env should have:"
echo "  AEGIS_MESSAGING_BACKEND=pubsub"
echo "  AEGIS_MESSAGING_PUBSUB_PROJECT_ID=local-project"
echo "  AEGIS_MESSAGING_PUBSUB_EMULATOR_HOST=localhost:8085"
echo ""
echo "To run the agent:"
echo "  poetry run python main.py"
