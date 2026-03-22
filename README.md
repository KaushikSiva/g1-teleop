# `g1-teleop`

This repo is a **small overlay repo** for Quest 3 teleoperation on top of NVIDIA `GR00T-WholeBodyControl`.

This repo is **not** a runnable full workspace by itself. First rehydrate a workspace from NVIDIA upstream, then run from that rehydrated workspace.

## What This Repo Contains

- Quest 3 teleop files
- runtime profiles for Mac and cloud
- deploy wrapper changes
- overlay metadata
- a rehydrate script

## 1. Download This Repo

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
```

## 2. Rehydrate a Runnable Workspace

```bash
chmod +x scripts/rehydrate_workspace.sh
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
```

This will:

1. clone NVIDIA upstream at the pinned ref
2. copy the overlay files into that workspace
3. run `git lfs pull` automatically if `git-lfs` is installed

Your runnable workspace will then be:

```bash
../g1-teleop-workspace
```

All run commands below should be executed from that rehydrated workspace, not from this overlay repo.

## 3. Install Rules

`install_scripts/install_quest3.sh` has two modes:

- default: `teleop`
  - safe for Mac
  - installs only what is needed for Quest 3 manager / WebXR
- optional: `full`
  - for Linux workstations that also need the sim stack
  - installs extra sim dependencies

Examples:

```bash
# Mac or teleop-only host
bash install_scripts/install_quest3.sh

# Linux workstation that also needs sim deps
QUEST3_INSTALL_MODE=full bash install_scripts/install_quest3.sh
```

## 4. The 3 Supported Paths

### Path 1: `Quest -> real robot`

Use this when the Quest 3 talks directly to the robot workstation. No Mac is needed in the control path.

Architecture:

- **Quest 3**: browser client
- **Robot workstation / onboard Linux box**:
  - `run_quest3_server.sh`
  - `gear_sonic_deploy`
- **Robot workstation -> robot** over the Unitree robot network

### Path 1 Setup

On the robot workstation:

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
bash install_scripts/install_quest3.sh
```

### Path 1 Run

Terminal 1 on the robot workstation:

```bash
cd gear_sonic_deploy
bash deploy.sh real --input-type zmq_manager
```

Wait until deploy is initialized.

Terminal 2 on the robot workstation:

```bash
cd ../g1-teleop-workspace
source runtime_profiles/LOCAL_MAC.env
bash run_quest3_server.sh
```

Use the workstation **Wi-Fi IP**, not the robot Ethernet `192.168.123.x` IP.

On the Quest 3 headset:

1. Connect the Quest 3 to the same Wi-Fi as the robot workstation.
2. Open Meta Quest Browser.
3. Visit `https://<WORKSTATION_WIFI_IP>:8443`
4. Accept the certificate warning.
5. Visit `https://<WORKSTATION_WIFI_IP>:8765` and accept that certificate too.
6. Return to `https://<WORKSTATION_WIFI_IP>:8443`
7. Tap `Connect WS`
8. Tap `Start VR`

### Path 1 Controls

- `Y`: start / calibrate
- `Left Stick`: move
- `Right Stick`: yaw
- `X`: toggle VR 3PT arms
- `A`: exit Quest manager
- `O` in deploy terminal: hard stop

---

### Path 2: `Mac + Quest -> cloud sim`

Use this when you want Quest/WebXR on your Mac and MuJoCo + GPU inference on a cloud machine.

Architecture:

- **Mac**:
  - Quest browser connection target
  - `run_quest3_server.sh`
- **Cloud GPU box**:
  - MuJoCo sim
  - `gear_sonic_deploy`

Keep MuJoCo and deploy on the same cloud machine.

### Path 2 Setup On Mac

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
bash install_scripts/install_quest3.sh
```

This is a teleop-only install on the Mac.

### Path 2 Run On Mac

```bash
cd ../g1-teleop-workspace
source runtime_profiles/LOCAL_MAC.env
bash run_quest3_server.sh
```

This prints the Mac IP. Use that IP on the Quest and on the cloud deploy side.

On the Quest 3 headset:

1. Connect Quest 3 to the same Wi-Fi as the Mac.
2. Open Meta Quest Browser.
3. Visit `https://<MAC_IP>:8443`
4. Accept the certificate warning.
5. Visit `https://<MAC_IP>:8765` and accept that certificate too.
6. Return to `https://<MAC_IP>:8443`
7. Tap `Connect WS`
8. Tap `Start VR`

### Path 2 Setup On Cloud GPU Machine

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
```

If this machine also needs the Quest teleop install pieces:

```bash
QUEST3_INSTALL_MODE=full bash install_scripts/install_quest3.sh
```

### Path 2 Run On Cloud GPU Machine

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

### Path 2 Controls

- `Y`: start / calibrate
- `Left Stick`: move
- `Right Stick`: yaw
- `X`: toggle VR 3PT arms
- `A`: exit Quest manager
- `O` in deploy terminal: hard stop

Optional remote debug:

```bash
python gear_sonic_deploy/visualize_motion.py --realtime_debug_url tcp://<CLOUD_HOST>:5557
```

---

### Path 3: `Mac + Quest -> real robot`

Use this when you want the Quest manager on your Mac, but the real robot is controlled by a separate Linux workstation.

Architecture:

- **Mac**:
  - Quest browser connection target
  - `run_quest3_server.sh`
- **Robot workstation / onboard Linux box**:
  - `gear_sonic_deploy`
  - ZMQ subscriber to the Mac-hosted Quest manager
- **Robot workstation -> robot** over the Unitree robot network

### Path 3 Setup On Mac

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
bash install_scripts/install_quest3.sh
source runtime_profiles/LOCAL_MAC.env
```

### Path 3 Run On Mac

```bash
bash run_quest3_server.sh
```

This prints the Mac IP. Use that IP on the Quest and on the robot workstation deploy side.

On the Quest 3 headset:

1. Connect Quest 3 to the same Wi-Fi as the Mac.
2. Open Meta Quest Browser.
3. Visit `https://<MAC_IP>:8443`
4. Accept the certificate warning.
5. Visit `https://<MAC_IP>:8765` and accept that certificate too.
6. Return to `https://<MAC_IP>:8443`
7. Tap `Connect WS`
8. Tap `Start VR`

### Path 3 Setup On Robot Workstation

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop
scripts/rehydrate_workspace.sh ../g1-teleop-workspace
cd ../g1-teleop-workspace
```

### Path 3 Run On Robot Workstation

Terminal 1:

```bash
cd gear_sonic_deploy
export QUEST3_ZMQ_HOST=<MAC_IP>
bash deploy.sh --zmq-host "$QUEST3_ZMQ_HOST" real --input-type zmq_manager
```

If you want the runtime profile defaults too:

```bash
cd gear_sonic_deploy
export QUEST3_ZMQ_HOST=<MAC_IP>
bash deploy.sh --runtime-profile REMOTE_SIM_BRIDGE --zmq-host "$QUEST3_ZMQ_HOST" real --input-type zmq_manager
```

Use the robot workstation interface for the robot side and the Mac IP only for `--zmq-host`.

### Path 3 Controls

- `Y`: start / calibrate
- `Left Stick`: move
- `Right Stick`: yaw
- `X`: toggle VR 3PT arms
- `A`: exit Quest manager
- `O` in deploy terminal: hard stop

## 5. Common Notes

- This repo intentionally does **not** contain the full NVIDIA source tree.
- The runnable workspace is created by `scripts/rehydrate_workspace.sh`.
- `run_quest3_server.sh` should run on whichever machine is hosting the Quest browser session.
- `gear_sonic_deploy` should run on whichever machine owns the sim or the real robot link.
- For real robot setups, never use the robot Ethernet `192.168.123.x` address in the Quest browser.
- For real robot setups, the Quest/browser side and the robot workstation can be on different machines, but deploy must have ZMQ reachability to the Quest manager host.
