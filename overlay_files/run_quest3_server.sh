#!/usr/bin/env bash
# Terminal 3 — Launch Quest 3 VR teleop manager
# Usage: bash run_quest3_server.sh [--vis-vr3pt] [--no-ssl] [...]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

resolve_lan_ip() {
    if [[ -n "${QUEST3_PUBLIC_HOST:-}" ]]; then
        echo "$QUEST3_PUBLIC_HOST"
        return 0
    fi

    if command -v python3 >/dev/null 2>&1; then
        python3 - <<'PY'
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    s.close()
except Exception:
    print("127.0.0.1")
PY
        return 0
    fi

    if command -v hostname >/dev/null 2>&1; then
        hostname -I 2>/dev/null | awk '{print $1}'
        return 0
    fi

    echo "127.0.0.1"
}

PROFILE="${TELEOP_RUNTIME_PROFILE:-LOCAL_MAC}"
ZMQ_BIND_PORT="${QUEST3_ZMQ_PORT:-5556}"
ZMQ_FEEDBACK_HOST="${QUEST3_ZMQ_FEEDBACK_HOST:-${QUEST3_DEBUG_HOST:-localhost}}"
ZMQ_FEEDBACK_PORT="${QUEST3_ZMQ_FEEDBACK_PORT:-${QUEST3_ZMQ_OUT_PORT:-5557}}"
HTTP_PORT="${QUEST3_HTTP_PORT:-8443}"
WS_PORT="${QUEST3_WS_PORT:-8765}"
IP="$(resolve_lan_ip)"

if [[ -d ".venv_teleop" ]]; then
    # shellcheck disable=SC1091
    source .venv_teleop/bin/activate
elif [[ -d ".venv_sim" ]]; then
    # shellcheck disable=SC1091
    source .venv_sim/bin/activate
else
    echo "No virtual environment found. Run bash install_scripts/install_quest3.sh first." >&2
    exit 1
fi

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  Quest 3 Teleop Server"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "  PREREQUISITE — Quest 3 Guardian Setup (one-time):"
echo ""
echo "    If you haven't set up the play boundary yet:"
echo "    1. On Quest 3: Press Meta button > Settings > Physical Space"
echo "    2. Tap 'Set Floor' — point controller at the floor, confirm"
echo "    3. Tap 'Create Boundary' — draw your play area, confirm"
echo "    Without this, 'Start VR' will fail with a reference space error."
echo ""
echo "  ──────────────────────────────────────────────────────────"
echo ""
echo "  On the Quest 3 headset:"
echo ""
echo "    1. Make sure Quest 3 is on the SAME Wi-Fi as this machine"
echo "    2. Open Meta Quest Browser"
echo "    3. Go to:  https://${IP}:${HTTP_PORT}"
echo "    4. Accept the self-signed certificate (Advanced -> Proceed)"
echo "    5. Also visit https://${IP}:${WS_PORT} and accept that cert too"
echo "    6. Go back to https://${IP}:${HTTP_PORT}"
echo "    7. Tap 'Connect WS' (status turns green)"
echo "    8. Tap 'Start VR' to begin streaming tracking data"
echo ""
echo "  ──────────────────────────────────────────────────────────"
echo ""
echo "  Runtime profile: ${PROFILE}"
echo "  ZMQ publish port: ${ZMQ_BIND_PORT}"
echo "  Feedback host: ${ZMQ_FEEDBACK_HOST}"
echo "  Feedback port: ${ZMQ_FEEDBACK_PORT}"
if [[ -n "${QUEST3_CLOUD_DEPLOY_HOST:-}" ]]; then
echo "  Cloud deploy host: ${QUEST3_CLOUD_DEPLOY_HOST}"
fi
echo ""
echo "  For cloud deploy:"
echo "    Terminal 1/2 should run on the GPU machine."
echo "    Start deploy there with:"
echo "      cd gear_sonic_deploy && bash deploy.sh --runtime-profile CLOUD_SIM --zmq-host ${IP} sim"
echo ""
echo "  ──────────────────────────────────────────────────────────"
echo ""
echo "  Controls (Quest 3 controllers):"
echo "    Y          = Start (calibrate + engage policy)"
echo "    A          = Emergency Stop"
echo "    X          = Toggle VR 3PT (arms follow your hands)"
echo "    Left Stick  = Move direction"
echo "    Right Stick = Yaw / heading"
echo "    A+B / X+Y  = Next / Previous locomotion mode"
echo "    Triggers   = Hand grasp (in VR 3PT mode)"
echo "    Grips      = Hand grip (in VR 3PT mode)"
echo ""
echo "  Workstation IP: ${IP}"
echo ""
echo "══════════════════════════════════════════════════════════════"
echo ""

python gear_sonic/scripts/quest3_manager_thread_server.py \
    --port "${ZMQ_BIND_PORT}" \
    --ws-port "${WS_PORT}" \
    --http-port "${HTTP_PORT}" \
    --zmq-feedback-host "${ZMQ_FEEDBACK_HOST}" \
    --zmq-feedback-port "${ZMQ_FEEDBACK_PORT}" \
    "$@"
