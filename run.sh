#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

COMPOSE=(docker compose)

if ! docker compose version >/dev/null 2>&1; then
  if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE=(docker-compose)
  else
    echo "Docker Compose is required." >&2
    exit 1
  fi
fi

usage() {
  echo "Usage: $0 {up|down|restart|build|clean|logs|status}"
  echo "  up        Build and start all services"
  echo "  down      Stop all services (keep images/volumes)"
  echo "  restart   Rebuild and restart all services"
  echo "  build     Rebuild images without starting"
  echo "  clean     Stop and remove containers, images, volumes, networks"
  echo "  logs      Follow logs for all services"
  echo "  status    Show running services"
  exit 1
}

[[ $# -eq 0 ]] && usage

case "$1" in
  up)
    echo ">>> Building and starting all services..."
    "${COMPOSE[@]}" up -d --build
    echo ">>> Done."
    ;;
  down)
    echo ">>> Stopping all services..."
    "${COMPOSE[@]}" down --remove-orphans
    echo ">>> Done."
    ;;
  restart)
    echo ">>> Rebuilding and restarting all services..."
    "${COMPOSE[@]}" down --remove-orphans
    "${COMPOSE[@]}" up -d --build
    echo ">>> Done."
    ;;
  build)
    echo ">>> Rebuilding all images..."
    "${COMPOSE[@]}" build
    echo ">>> Done."
    ;;
  clean)
    echo ">>> Cleaning all containers, images, volumes, and networks..."
    "${COMPOSE[@]}" down --rmi all --volumes --remove-orphans
    echo ">>> Done."
    ;;
  logs)
    "${COMPOSE[@]}" logs -f
    ;;
  status)
    "${COMPOSE[@]}" ps
    ;;
  *)
    echo "Unknown command: $1"
    usage
    ;;
esac
