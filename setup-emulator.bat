@echo off
REM Setup script for Pub/Sub Emulator local development (Windows)

REM Point gcloud to Pub/Sub Emulator
set PUBSUB_EMULATOR_HOST=localhost:8085
set CLOUDSDK_API_ENDPOINT_OVERRIDES_PUBSUB=http://localhost:8085/
set CLOUDSDK_CORE_PROJECT=aegis-local
set PROJECT_ID=aegis-local
set EMULATOR_URL=http://localhost:8085/v1/projects/%PROJECT_ID%

echo Starting Pub/Sub Emulator...
docker-compose up -d pubsub-emulator

echo Waiting for emulator to be ready...
timeout /t 10 /nobreak

echo Creating topics (idempotent)...
call :ensure_topic aegis-test.test-generation.requested
call :ensure_topic aegis-test.test-generation.planning.started
call :ensure_topic aegis-test.test-generation.planning.completed
call :ensure_topic aegis-test.test-generation.planning.failed

echo Creating subscriptions (idempotent)...
call :ensure_subscription test-planner.aegis-test.test-generation.requested aegis-test.test-generation.requested
call :ensure_subscription orchestrator.aegis-test.test-generation.planning.started aegis-test.test-generation.planning.started
call :ensure_subscription orchestrator.aegis-test.test-generation.planning.completed aegis-test.test-generation.planning.completed
call :ensure_subscription orchestrator.aegis-test.test-generation.planning.failed aegis-test.test-generation.planning.failed

echo.
echo (✓) Pub/Sub Emulator is ready!
echo.
echo Your .env should have:
echo   AEGIS_MESSAGING_PUBSUB_PROJECT_ID=%PROJECT_ID%
echo   AEGIS_MESSAGING_PUBSUB_EMULATOR_HOST=localhost:8085
echo.
echo To run the agent:
echo   poetry run python main.py

goto :eof

:ensure_topic
echo Creating topic (idempotent): %1
curl -s -X PUT "%EMULATOR_URL%/topics/%1" >nul
goto :eof

:ensure_subscription
echo Creating subscription (idempotent): %1
curl -s -X PUT -H "Content-Type: application/json" -d "{\"topic\":\"projects/%PROJECT_ID%/topics/%2\"}" "%EMULATOR_URL%/subscriptions/%1" >nul
goto :eof
