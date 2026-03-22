# `g1-teleop`

This repository is now a **team overlay repo**, not a self-contained copy of NVIDIA GR00T / GEAR-SONIC.

It keeps only the team-owned files needed for:

- Quest 3 teleoperation
- Mac -> cloud runtime setup
- deployment/runtime wrappers
- overlay metadata and rehydrate tooling

## Repo model

- `upstream`: NVIDIA `GR00T-WholeBodyControl`
- `this repo`: your team's overlay only

You do **not** run this repo directly. You first rehydrate a working workspace from upstream, then apply the overlay files from this repo.

## Main files

- `overlay/manifest.yaml`: pinned upstream ref and overlay contract
- `overlay_files/`: team-owned files copied into upstream during rehydrate
- `runtime_profiles/`: env presets for Mac and cloud hosts
- `scripts/rehydrate_workspace.sh`: builds a runnable workspace from upstream + overlay

## Rehydrate a runnable workspace

```bash
git clone https://github.com/KaushikSiva/g1-teleop.git
cd g1-teleop

scripts/rehydrate_workspace.sh ../g1-teleop-workspace
```

That will:

1. clone NVIDIA upstream at the pinned ref
2. copy all files from `overlay_files/` into the new workspace
3. print the next steps for running the Mac/cloud setup

## Mac + Cloud runtime

- **Mac**: Quest 3 browser + `run_quest3_server.sh`
- **Cloud GPU machine**: MuJoCo + `gear_sonic_deploy`

Keep MuJoCo and deploy on the same machine for v1. Quest input already crosses machines cleanly over WebXR/WebSocket -> ZMQ; the current MuJoCo sim path still uses local DDS topics.
