#!/bin/zsh
#
# cursorkit: install Cursor Starter Kit into a repo
# Version: 1.0.0
#
# Source this file in your shell (e.g., add to ~/.zshrc):
#   source "/path/to/cursor-starter-kit/cursorkit.zsh"
#
# Then run:
#   cursorkit --target /path/to/repo --skip-existing
#
# The installer path is auto-detected relative to this script.
# Override with: export CURSORKIT_INSTALLER="/custom/path/install.sh"
#

cursorkit() {
  emulate -L zsh
  # Important: don't enable `errexit`/`nounset` in an interactive helper,
  # because a non-zero installer exit can close the whole terminal session.
  setopt pipefail

  # Self-locate: find install.sh relative to this script
  local script_dir="${${(%):-%x}:A:h}"
  local installer="${CURSORKIT_INSTALLER:-${script_dir}/install.sh}"
  local target=""
  local mode_skip=0 mode_backup=0 mode_force=0

  while (( $# )); do
    case "$1" in
      -h|--help)
        cat <<'EOF'
cursorkit: install Cursor Starter Kit into a repo

Usage:
  cursorkit [--target PATH] [--skip-existing|--backup] [--force] [--installer PATH]
  cursorkit --target /path/to/repo --backup --force

Options:
  --target PATH        Install into PATH (default: git root if in a repo, else $PWD)
  --skip-existing      INSTALL_SKIP_EXISTING=1 (least intrusive)
  --backup             INSTALL_BACKUP=1 (backs up then overwrites)
  --force              INSTALL_FORCE=1 (reinstall even if detected)
  --installer PATH     Override installer path (or set CURSORKIT_INSTALLER)
EOF
        return 0
        ;;
      --installer)
        if (( $# < 2 )); then
          echo "cursorkit: --installer requires a PATH" >&2
          return 2
        fi
        installer="$2"
        shift 2
        ;;
      --target)
        if (( $# < 2 )); then
          echo "cursorkit: --target requires a PATH" >&2
          return 2
        fi
        target="$2"
        shift 2
        ;;
      --skip-existing)
        mode_skip=1
        shift
        ;;
      --backup)
        mode_backup=1
        shift
        ;;
      --force)
        mode_force=1
        shift
        ;;
      *)
        echo "cursorkit: unknown option: $1 (try --help)" >&2
        return 2
        ;;
    esac
  done

  if (( mode_skip && mode_backup )); then
    echo "cursorkit: choose only one: --skip-existing OR --backup" >&2
    return 2
  fi

  if [[ -z "$target" ]]; then
    if git rev-parse --show-toplevel > /dev/null 2>&1; then
      target="$(git rev-parse --show-toplevel)"
    else
      target="$PWD"
    fi
  fi

  if [[ ! -e "$installer" ]]; then
    echo "cursorkit: installer not found: $installer" >&2
    return 1
  fi

  local -a env_args=()
  (( mode_skip )) && env_args+=(INSTALL_SKIP_EXISTING=1)
  (( mode_backup )) && env_args+=(INSTALL_BACKUP=1)
  (( mode_force )) && env_args+=(INSTALL_FORCE=1)

  env "${env_args[@]}" zsh "$installer" "$target"
  return $?
}

