# `g1-teleop`

This repo is a **small overlay repo** for your team's Quest 3 teleop workflow on top of NVIDIA `GR00T-WholeBodyControl`.

You do not run this repo directly. First rehydrate a runnable workspace from NVIDIA upstream, then run from that workspace.

## What This Repo Contains

- Quest 3 teleop files
- Mac -> cloud runtime wrapper scripts
- Mac -> real robot wrapper scripts
- overlay metadata
- a rehydrate script

## 1. Download This Repo

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
```

## 2. Rehydrate a Runnable Workspace

This clones NVIDIA upstream at the pinned commit and copies the overlay files into a fresh workspace.

```bash
chmod +x scripts/rehydrate_workspace.sh
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
```

After that, your runnable workspace will be:

```bash
../g1-teleop-workspace
```

All commands below should be run from that rehydrated workspace, not from this overlay repo.

## A. Run `mac -> sim (GPU box in cloud)`

Recommended architecture:

- **Mac**: Quest 3 browser + Quest 3 manager
- **GPU cloud box**: MuJoCo sim + `gear_sonic_deploy`

Keep MuJoCo and deploy on the same cloud machine.

### A1. On your Mac: install and start Quest 3 manager

```bash
cd ../g1-teleop-workspace
bash install_scripts/install_quest3.sh
source runtime_profiles/LOCAL_MAC.env
bash run_quest3_server.sh
```

This prints your Mac IP and the Quest browser URL, usually:

```bash
https://<MAC_IP>:8443
```

### A2. On the Quest 3 headset

1. Connect Quest 3 to the same Wi-Fi as the Mac.
2. Open Meta Quest Browser.
3. Visit `https://<MAC_IP>:8443`
4. Accept the certificate warning.
5. Visit `https://<MAC_IP>:8765` and accept that certificate too.
6. Go back to `https://<MAC_IP>:8443`
7. Tap `Connect WS`
8. Tap `Start VR`

### A3. On the GPU cloud machine: install and run sim

Clone and rehydrate there too:

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
```

Install whatever NVIDIA upstream requires on that machine, then run:

Terminal 1:
```bash
source .venv_sim/bin/activate
python gear_sonic/scripts/run_sim_loop.py
```

Terminal 2:
```bash
cd gear_sonic_deploy
source ../runtime_profiles/CLOUD_SIM.env
export QUEST3_ZMQ_HOST=<MAC_IP>
bash deploy.sh --runtime-profile CLOUD_SIM --zmq-host "$QUEST3_ZMQ_HOST" sim
```

### A4. Control flow

- Press `Y` on Quest 3 to start/calibrate.
- `Left Stick` moves.
- `Right Stick` yaws.
- `X` toggles VR 3PT arm mode.
- `A` stops the Quest manager.
- `O` in the deploy terminal is the hard stop.

### A5. Optional debug back to Mac

If port `5557` from the cloud box is reachable:

```bash
python gear_sonic_deploy/visualize_motion.py --realtime_debug_url tcp://<CLOUD_HOST>:5557
```

## B. Run `mac -> real Unitree robot`

Recommended architecture:

- **Mac**: Quest 3 browser only
- **Robot workstation / onboard Linux box**: Quest 3 manager + `gear_sonic_deploy`

Reason: the Quest browser must reach the machine hosting the WebXR page and ZMQ Quest manager, and the robot-control side should stay local to the robot network.

### B1. On the robot workstation: clone and rehydrate

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
```

### B2. On the robot workstation: install Quest 3 teleop env

```bash
bash install_scripts/install_quest3.sh
```

### B3. On the robot workstation: run deploy

Terminal 1:
```bash
cd gear_sonic_deploy
bash deploy.sh real --input-type zmq_manager
```

Wait until deploy is initialized.

### B4. On the robot workstation: run Quest 3 manager

Terminal 2:
```bash
cd ../g1-teleop-workspace
source runtime_profiles/LOCAL_MAC.env
bash run_quest3_server.sh
```

Use the workstation Wi-Fi IP shown by the script, not the robot Ethernet IP.

### B5. On the Quest 3 headset

1. Put Quest 3 on the same Wi-Fi as the robot workstation.
2. Open Meta Quest Browser.
3. Visit `https://<WORKSTATION_WIFI_IP>:8443`
4. Accept the certificate warning.
5. Visit `https://<WORKSTATION_WIFI_IP>:8765` and accept that certificate too.
6. Return to `https://<WORKSTATION_WIFI_IP>:8443`
7. Tap `Connect WS`
8. Tap `Start VR`

### B6. Operate the robot

- Stand in calibration pose first.
- Press `Y` to start/calibrate.
- `Left Stick` moves.
- `Right Stick` yaws.
- `X` toggles VR 3PT arm mode.
- `A` exits Quest manager.
- `O` in deploy terminal is the hard stop.

## Notes

- This repo intentionally does **not** contain the full NVIDIA source tree.
- The runnable workspace is created by `scripts/rehydrate_workspace.sh`.
- For `mac -> sim`, the Mac should host Quest/WebXR and the cloud box should host MuJoCo + deploy.
- For `mac -> real robot`, the robot-side Linux machine should host deploy and Quest manager; the Mac is not the robot-control host.
