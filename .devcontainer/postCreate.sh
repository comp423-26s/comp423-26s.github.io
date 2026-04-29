#!/usr/bin/env bash
set -euo pipefail

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

# Install a real browser for pa11y/pa11y-ci.
sudo apt-get update
sudo apt-get install -y chromium

ensure_workspace_venv

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

# Ensure Node-based accessibility tooling is available.
# Some images/features require sudo for global installs.
if command -v npm >/dev/null 2>&1; then
  npm install -g pa11y pa11y-ci || sudo npm install -g pa11y pa11y-ci
else
  echo "npm not found; Node feature may not be installed correctly." >&2
  exit 1
fi

# Add an idempotent bashrc hook to auto-activate the workspace venv in interactive shells.
BASHRC="$HOME/.bashrc"
START_MARKER="# >>> comp423 venv >>>"
END_MARKER="# <<< comp423 venv <<<"

if ! grep -Fq "$START_MARKER" "$BASHRC" 2>/dev/null; then
  {
    echo ""
    echo "$START_MARKER"
    echo "# Auto-activate per-repo venv when present"
    echo "if [[ -n \"\$PS1\" ]] && [[ -f \"$PWD/.venv/bin/activate\" ]]; then"
    echo "  # shellcheck disable=SC1091"
    echo "  source \"$PWD/.venv/bin/activate\""
    echo "fi"
    echo "$END_MARKER"
  } >> "$BASHRC"
fi
