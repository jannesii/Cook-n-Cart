pyside6-android-deploy --name "CookAndCart" --keep-deployment-files \
	--wheel-pyside=$HOME/Cook-n-Cart/whl/PySide6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl \
	--wheel-shiboken=$HOME/Cook-n-Cart/whl/shiboken6-6.8.0.2-6.8.0-cp311-cp311-android_aarch64.whl \
	--ndk-path=$HOME/.pyside6_android_deploy/android-ndk/android-ndk-r26b/ \
	--sdk-path=$HOME/.pyside6_android_deploy/android-sdk/
