#!/bin/bash

# This script installs the required packages for building PySide6 on Android.
# It is intended to be run on a Debian-based system (like Ubuntu).

# Install necessary packages (adding -y for non-interactive mode)
sudo apt update && sudo apt install -y python3 default-jdk zip autoconf automake libtool pkg-config python3-venv build-essential

# Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r ./build/requirements.txt

# Clone the pyside-setup repository
git clone https://code.qt.io/pyside/pyside-setup

cd pyside-setup

# This script will download the Android NDK and SDK packages required into your home directory as a directory called .pyside6-android-deploy.
python3 tools/cross_compile_android/main.py --download-only --skip-update --auto-accept-license

cd ..

# Clean up
rm -rf pyside-setup/

pyside6-android-deploy --init \
	--wheel-pyside=$HOME/Cook-n-Cart/whl/PySide6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl \
	--wheel-shiboken=$HOME/Cook-n-Cart/whl/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl