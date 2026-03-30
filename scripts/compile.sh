#!/bin/bash
export PATH="$HOME/.local/toolchains/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi/bin:$PATH"
cd ~/code/qmk_firmware
QMK_HOME=~/code/qmk_firmware qmk compile -kb lucky_studio/sofle_4x6 -km default
