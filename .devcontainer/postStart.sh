#!/usr/bin/env bash
set -euo pipefail

# Always ensure the venv exists on container boot.
cd "${1:-$PWD}"

find_bootstrap_python() {
  local workspace_venv_bin="$PWD/.venv/bin"
  local candidate=""
  local resolved=""

  for candidate in /usr/local/bin/python3 /usr/local/bin/python /usr/bin/python3 python3 python; do
    if [[ "$candidate" = /* ]]; then
      [[ -x "$candidate" ]] || continue
      resolved="$candidate"
    else
      resolved="$(command -v "$candidate" 2>/dev/null || true)"
      [[ -n "$resolved" ]] || continue
    fi

    if [[ "$resolved" != "$workspace_venv_bin/"* ]]; then
      echo "$resolved"
      return 0
    fi
  done

  echo "Unable to locate a system Python interpreter for bootstrapping .venv." >&2
  return 1
}

ensure_workspace_venv() {
  local bootstrap_python=""
  bootstrap_python="$(find_bootstrap_python)"

  if [[ -x ".venv/bin/python" ]] && ! .venv/bin/python -m pip --version >/dev/null 2>&1; then
    rm -rf .venv
  fi

  if [[ ! -x ".venv/bin/python" ]]; then
    "$bootstrap_python" -m venv .venv
  fi

  .venv/bin/python -m pip --version >/dev/null
}

ensure_workspace_venv

# Light-touch: don't re-install requirements on every start.
# Terminal auto-activation is handled via ~/.bashrc hook (added on create)
# and via remoteEnv PATH/VIRTUAL_ENV in devcontainer.json.
