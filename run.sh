cat run.sh
#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

COMPOSE=(docker compose)

if ! docker compose version >/dev/null 2>&1; then
    if command -v docker-compose >/dev/null 2>&1; then
        COMPOSE=(docker-compose)
    else
        echo "Docker Compose is required. Install Docker Compose v2 or docker-compose." >&2
        exit 1
    fi
fi

echo "Stopping old AthenaCodex containers and removing orphans..."
"${COMPOSE[@]}" down --remove-orphans

echo "Building and starting AthenaCodex in the background..."
"${COMPOSE[@]}" up -d --build

echo
echo "AthenaCodex is starting. Current container status:"
"${COMPOSE[@]}" ps
echo
echo "Open the UI at: http://localhost:${NGINX_HTTP_PORT:-80}"
echo "View logs with: ${COMPOSE[*]} logs -f"
echo "Stop with: ${COMPOSE[*]} down"
