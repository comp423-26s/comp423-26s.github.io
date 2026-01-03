#!/usr/bin/env bash
set -euo pipefail

# Always ensure the venv exists on container boot.
cd "${1:-$PWD}"

if [[ ! -d ".venv" ]]; then
  python -m venv .venv
fi

# Light-touch: don't re-install requirements on every start.
# Terminal auto-activation is handled via ~/.bashrc hook (added on create)
# and via remoteEnv PATH/VIRTUAL_ENV in devcontainer.json.
