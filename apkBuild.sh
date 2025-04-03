#!/bin/bash

# Find directories matching the pattern, sort them by version, and select the latest one.
NDK_DIR=$(find "$HOME/.pyside6_android_deploy/android-ndk/" -maxdepth 1 -type d -name 'android-ndk-r*' | sort -V | tail -n 1)

pyside6-android-deploy --name "CookAndCart" --keep-deployment-files \
	--wheel-pyside="$HOME/Cook-n-Cart/whl/PySide6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl" \
	--wheel-shiboken="$HOME/Cook-n-Cart/whl/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl" \
	--ndk-path="$NDK_DIR" \
	--sdk-path="$HOME/.pyside6_android_deploy/android-sdk/"
