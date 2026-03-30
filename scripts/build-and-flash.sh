#!/bin/bash
# Compile and flash both halves in one go.
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
"$DIR/compile.sh"
"$DIR/flash.sh"
