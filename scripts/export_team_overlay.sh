#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MANIFEST="$REPO_ROOT/overlay/manifest.yaml"
OVERLAY_ROOT="$REPO_ROOT/overlay_files"

if [[ ! -f "$MANIFEST" ]]; then
    echo "Missing overlay manifest at $MANIFEST" >&2
    exit 1
fi

if [[ ! -d "$OVERLAY_ROOT" ]]; then
    echo "Missing overlay files directory at $OVERLAY_ROOT" >&2
    exit 1
fi

DEST_ROOT="${1:-$REPO_ROOT/_overlay_export}"

rm -rf "$DEST_ROOT"
mkdir -p "$DEST_ROOT"

cp -R "$OVERLAY_ROOT" "$DEST_ROOT/overlay_files"
mkdir -p "$DEST_ROOT/overlay" "$DEST_ROOT/runtime_profiles" "$DEST_ROOT/scripts"
cp "$REPO_ROOT/overlay/manifest.yaml" "$DEST_ROOT/overlay/manifest.yaml"
cp "$REPO_ROOT/runtime_profiles/LOCAL_MAC.env" "$DEST_ROOT/runtime_profiles/LOCAL_MAC.env"
cp "$REPO_ROOT/runtime_profiles/CLOUD_SIM.env" "$DEST_ROOT/runtime_profiles/CLOUD_SIM.env"
cp "$REPO_ROOT/scripts/rehydrate_workspace.sh" "$DEST_ROOT/scripts/rehydrate_workspace.sh"
cp "$REPO_ROOT/scripts/export_team_overlay.sh" "$DEST_ROOT/scripts/export_team_overlay.sh"

cat > "$DEST_ROOT/README.md" <<'EOF'
# Team Overlay Export

This export contains only the team overlay.

Use `scripts/rehydrate_workspace.sh` from the export to create a runnable workspace from NVIDIA upstream plus `overlay_files/`.
EOF

echo "Overlay export created at: $DEST_ROOT"
