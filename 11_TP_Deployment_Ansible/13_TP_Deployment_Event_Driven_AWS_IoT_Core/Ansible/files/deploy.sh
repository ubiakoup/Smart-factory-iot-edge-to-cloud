#!/bin/bash

set -euo pipefail

LOG_FILE="/home/vagrant/deploy.log"
PROJECT_DIR="/home/vagrant/edge-stack"

# -------------------------------
# Logging
# -------------------------------
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') | $1" | tee -a "$LOG_FILE"
}

log "Starting deployment"

# -------------------------------
# Go to project directory
# -------------------------------
cd "$PROJECT_DIR" || {
    log "❌ Failed to access project directory"
    exit 1
}

# -------------------------------
# Save current commit (rollback)
# -------------------------------
OLD_COMMIT=$(git rev-parse HEAD)
log "Current commit: $OLD_COMMIT"

# -------------------------------
# Pull latest code
# -------------------------------
log "🔄 Pulling latest version..."
sleep 2  # Simulate delay for testing anti-spam
git pull origin main

NEW_COMMIT=$(git rev-parse HEAD)
log "New commit: $NEW_COMMIT"

# -------------------------------
# Check if update needed
# -------------------------------
if [ "$OLD_COMMIT" = "$NEW_COMMIT" ]; then
    log "✅ No changes detected, skipping deployment"
    exit 0
fi

# -------------------------------
# Deploy
# -------------------------------
log "🚀 Deploying new version..."

if docker compose up -d --build; then
    log "✅ Deployment successful"
else
    log "❌ Deployment failed → rolling back..."

    git reset --hard "$OLD_COMMIT"

    docker compose up -d --build

    log "↩️ Rollback applied"
    exit 1
fi

# -------------------------------
# Cleanup
# -------------------------------
log "🧹 Cleaning unused images..."
docker image prune -f

log "✅ Deployment finished successfully"