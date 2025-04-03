#!/bin/bash

# Automatically select the latest Android NDK directory based on version name
NDK_DIR=$(ls -d $HOME/.pyside6_android_deploy/android-ndk/android-ndk-r* | sort -V | tail -n 1)

pyside6-android-deploy --name "CookAndCart" --keep-deployment-files \
	--wheel-pyside="$HOME/Cook-n-Cart/whl/PySide6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl" \
	--wheel-shiboken="$HOME/Cook-n-Cart/whl/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl" \
	--ndk-path="$NDK_DIR" \
	--sdk-path="$HOME/.pyside6_android_deploy/android-sdk/"

