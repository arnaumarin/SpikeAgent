#!/bin/bash

# Helper script to restart SpikeAgent container with additional volume mounts
# This script will:
# 1. Stop the current spikeagent container
# 2. Get any existing volume mounts
# 3. Restart with existing mounts + new mounts

set -e

CONTAINER_NAME="spikeagent"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for help flag
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "Usage: $0 [new_path1] [new_path2] ..."
    echo ""
    echo "This script restarts the SpikeAgent container with additional volume mounts."
    echo "It preserves any existing mounts and adds the new paths you specify."
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/new/data"
    echo "  $0 /path/to/data1 /path/to/data2"
    echo ""
    exit 0
fi

# Check if container exists
if ! docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "❌ Container '${CONTAINER_NAME}' not found."
    echo "   Start it first with: ./run-spikeagent.sh"
    exit 1
fi

# Get existing volume mounts from the running container
echo "🔍 Checking existing volume mounts..."
EXISTING_MOUNTS=()
while IFS= read -r mount; do
    if [[ -n "$mount" ]]; then
        # Extract source path from mount (format: /host/path:/container/path)
        source_path=$(echo "$mount" | cut -d':' -f1)
        if [[ "$source_path" == /* ]]; then
            EXISTING_MOUNTS+=("$mount")
        fi
    fi
done < <(docker inspect ${CONTAINER_NAME} --format='{{range .Mounts}}{{.Source}}:{{.Destination}} {{end}}' 2>/dev/null || true)

# Parse new volume mount arguments
NEW_MOUNTS=()
for path in "$@"; do
    # Check if path exists
    if [ ! -e "$path" ]; then
        echo "⚠️  Warning: Path does not exist: $path"
        echo "   It will still be mounted, but may not be accessible."
    fi
    # Convert to absolute path
    if [[ "$path" = /* ]]; then
        abs_path="$path"
    else
        abs_path="$(cd "$(dirname "$path")" 2>/dev/null && pwd)/$(basename "$path")" || abs_path="$(pwd)/$path"
    fi
    NEW_MOUNTS+=("-v" "$abs_path:$abs_path")
done

# Combine existing and new mounts
ALL_MOUNTS=()
for mount in "${EXISTING_MOUNTS[@]}"; do
    source_path=$(echo "$mount" | cut -d':' -f1)
    dest_path=$(echo "$mount" | cut -d':' -f2)
    ALL_MOUNTS+=("-v" "$source_path:$dest_path")
done
ALL_MOUNTS+=("${NEW_MOUNTS[@]}")

# Get the image name from the current container
IMAGE=$(docker inspect ${CONTAINER_NAME} --format='{{.Config.Image}}' 2>/dev/null || echo "ghcr.io/arnaumarin/spikeagent-cpu:latest")

# Get environment file location (assume .env in script directory)
ENV_FILE="${SCRIPT_DIR}/.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Warning: .env file not found at $ENV_FILE"
    echo "   Container may not start without API keys."
fi

echo ""
echo "🔄 Restarting container with mounts..."
echo "   Image: ${IMAGE}"
echo "   Existing mounts: ${#EXISTING_MOUNTS[@]}"
echo "   New mounts: ${#NEW_MOUNTS[@]}"
echo ""

# Stop and remove existing container
echo "🛑 Stopping existing container..."
docker stop ${CONTAINER_NAME} > /dev/null 2>&1 || true
docker rm ${CONTAINER_NAME} > /dev/null 2>&1 || true

# Start new container with all mounts
echo "🚀 Starting container with all mounts..."
if [ -f "$ENV_FILE" ]; then
    if docker run --rm -d \
        -p 8501:8501 \
        --name ${CONTAINER_NAME} \
        --env-file "$ENV_FILE" \
        "${ALL_MOUNTS[@]}" \
        ${IMAGE} > /dev/null 2>&1; then
        echo "✅ Container restarted successfully!"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
else
    echo "⚠️  Starting without .env file (using environment variables)..."
    if docker run --rm -d \
        -p 8501:8501 \
        --name ${CONTAINER_NAME} \
        "${ALL_MOUNTS[@]}" \
        ${IMAGE} > /dev/null 2>&1; then
        echo "✅ Container restarted successfully!"
    else
        echo "❌ Failed to start container"
        exit 1
    fi
fi

echo ""
echo "📍 Access the application at: http://localhost:8501"
echo ""
echo "📝 Useful commands:"
echo "   View logs:        docker logs -f ${CONTAINER_NAME}"
echo "   Stop container:   docker stop ${CONTAINER_NAME}"
echo ""
