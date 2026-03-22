# Mac + Cloud Runtime

This repo now supports a `reliable first` split for Quest 3 teleoperation:

- **Mac**: Quest 3 browser session and Quest manager (`run_quest3_server.sh`)
- **Cloud GPU machine**: MuJoCo sim, `gear_sonic_deploy`, TensorRT, ONNX models

This is the recommended setup when you want Quest 3 on a Mac but the heavy policy stack on an NVIDIA GPU machine.

## Why this split

Quest 3 input already crosses machines cleanly through WebXR/WebSocket and ZMQ. MuJoCo sim does **not**: the current sim path exchanges low-level robot traffic with deploy over Unitree DDS topics such as `rt/lowcmd` and `rt/lowstate`. Keep MuJoCo and deploy on the same machine for v1.

## Runtime profiles

Two profile files are provided:

- `runtime_profiles/LOCAL_MAC.env`
- `runtime_profiles/CLOUD_SIM.env`

### Mac terminal

```bash
source runtime_profiles/LOCAL_MAC.env
bash run_quest3_server.sh
```

The script prints the browser URL for the Quest 3 and binds the ZMQ Quest-manager publisher on port `5556`.

### Cloud terminal 1

Run MuJoCo on the GPU machine:

```bash
source .venv_sim/bin/activate
python gear_sonic/scripts/run_sim_loop.py
```

### Cloud terminal 2

Point deploy at the Mac-hosted Quest manager:

```bash
source runtime_profiles/CLOUD_SIM.env
export QUEST3_ZMQ_HOST=<mac-lan-ip>
cd gear_sonic_deploy
bash deploy.sh --runtime-profile CLOUD_SIM --zmq-host "$QUEST3_ZMQ_HOST" sim
```

## Debug backhaul

The deploy side publishes debug output on port `5557` by default. Use that for visualization or forwarding back to the Mac:

```bash
python visualize_motion.py --realtime_debug_url tcp://<cloud-host>:5557
```

## If you later need Mac-local MuJoCo

Do not try to stretch the current DDS sim path over WAN. Build a dedicated remote sim bridge:

- deploy -> sim: low-level command packets over TCP/ZMQ
- sim -> deploy: joint state, IMU, odometry, optional hand state

That is a transport refactor, not a deploy-script tweak.
