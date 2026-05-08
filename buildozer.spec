[app]
title = Elda
package.name = elda
package.domain = org.elda
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = bin,.buildozer,.github,__pycache__
source.exclude_patterns = build_apk.sh,Dockerfile,README.md,onboard.py
version = 1.0.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pymongo,dnspython,pillow,certifi,requests,urllib3,charset-normalizer,idna

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.accept_sdk_license = True
android.arch = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
