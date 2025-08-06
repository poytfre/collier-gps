[app]
android.sdk_path = HOME/.buildozer/android/platform/android-sdk
"'
"'
android.ndk_path = HOME/.buildozer/android/platform/android-ndk-r25b android.accept_sdk_licence = true
title = Collier GPS
package.name = colliergps
package.domain = org.gps.collar
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0
requirements = python3,kivy,kivymd,plyer
orientation = portrait
fullscreen = 1
android.permissions = SEND_SMS,RECEIVE_SMS,READ_SMS,INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
