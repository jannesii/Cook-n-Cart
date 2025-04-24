#!/bin/bash

# This script installs the required packages for building PySide6 on Android.
# It is intended to be run on a Debian-based system (like Ubuntu).

# Update package list and install necessary system packages.
echo "Updating package list and installing required system packages..."
sudo apt update && sudo apt install -y python3 default-jdk zip autoconf automake libtool pkg-config python3-venv build-essential zlib1g-dev lld

# Create a Python virtual environment.
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate the virtual environment.
echo "Activating the virtual environment..."
source .venv/bin/activate

# Install Python dependencies from the requirements file.
echo "Installing Python dependencies..."
pip install -r ./build/requirements.txt

# Clone the pyside-setup repository.
echo "Cloning the pyside-setup repository..."
git clone https://code.qt.io/pyside/pyside-setup

# Enter the repository directory.
cd pyside-setup

# Download the Android NDK and SDK packages required for PySide6 Android deployment.
echo "Downloading Android NDK and SDK packages (this may take a while)..."
python3 tools/cross_compile_android/main.py --download-only --skip-update --auto-accept-license

# Return to the parent directory.
cd ..

# Clean up by removing the pyside-setup repository.
echo "Cleaning up: Removing the pyside-setup directory..."
rm -rf pyside-setup/

# Initialize PySide6 Android deployment with the specified wheel files.
echo "Initializing PySide6 Android deployment..."
pyside6-android-deploy --init \
	--wheel-pyside="$HOME/Cook-n-Cart/whl/PySide6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl" \
	--wheel-shiboken="$HOME/Cook-n-Cart/whl/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl"

echo "Deployment initialization complete."
