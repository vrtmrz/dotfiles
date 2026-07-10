#!/usr/bin/env bash

set -euo pipefail

repo_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source_file="$repo_dir/codex/AGENTS.md"
target_dir="${CODEX_HOME:-$HOME/.codex}"
target_file="$target_dir/AGENTS.md"

mkdir -p "$target_dir"

if [[ -e "$target_file" || -L "$target_file" ]]; then
    if [[ "$(readlink -f -- "$target_file")" == "$(readlink -f -- "$source_file")" ]]; then
        printf '%s\n' "Already linked: $target_file"
        exit 0
    fi

    backup_file="$target_file.backup.$(date -u +%Y%m%dT%H%M%SZ)"
    mv -- "$target_file" "$backup_file"
    printf '%s\n' "Preserved existing file: $backup_file"
fi

ln -s -- "$source_file" "$target_file"
printf '%s\n' "Linked: $target_file -> $source_file"
