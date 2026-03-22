#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$REPO_ROOT/overlay/manifest.yaml"
OVERLAY_ROOT="$REPO_ROOT/overlay_files"

if [[ ! -f "$MANIFEST" ]]; then
    echo "Missing manifest: $MANIFEST" >&2
    exit 1
fi

if [[ ! -d "$OVERLAY_ROOT" ]]; then
    echo "Missing overlay files directory: $OVERLAY_ROOT" >&2
    exit 1
fi

TARGET_DIR="${1:-$REPO_ROOT/../g1-teleop-workspace}"

UPSTREAM_URL="$(awk '/remote_url:/ {print $2}' "$MANIFEST")"
PINNED_REF="$(awk '/pinned_ref:/ {print $2}' "$MANIFEST")"

if [[ -z "$UPSTREAM_URL" || -z "$PINNED_REF" ]]; then
    echo "Could not read upstream_url or pinned_ref from $MANIFEST" >&2
    exit 1
fi

if [[ -e "$TARGET_DIR" ]]; then
    echo "Target already exists: $TARGET_DIR" >&2
    exit 1
fi

echo "Cloning upstream into: $TARGET_DIR"
git clone "$UPSTREAM_URL" "$TARGET_DIR"

cd "$TARGET_DIR"
git checkout "$PINNED_REF"

echo "Applying overlay files"
cp -R "$OVERLAY_ROOT"/. "$TARGET_DIR"/
cp -R "$REPO_ROOT/runtime_profiles" "$TARGET_DIR/runtime_profiles"
mkdir -p "$TARGET_DIR/overlay"
cp "$MANIFEST" "$TARGET_DIR/overlay/manifest.yaml"

cat <<EOF

Workspace ready: $TARGET_DIR

Next steps:

1. Fetch large files if needed:
   cd "$TARGET_DIR"
   git lfs pull

2. Mac host:
   source runtime_profiles/LOCAL_MAC.env
   bash run_quest3_server.sh

3. Cloud host:
   source runtime_profiles/CLOUD_SIM.env
   export QUEST3_ZMQ_HOST=<mac-lan-ip>
   cd gear_sonic_deploy
   bash deploy.sh --runtime-profile CLOUD_SIM --zmq-host "\$QUEST3_ZMQ_HOST" sim
EOF
