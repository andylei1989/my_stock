[app]
title = 私募持仓分析
package.name = stockpro
package.domain = org.analysis
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,xlsx

# 核心依赖库：务必包含 openpyxl 和 numpy
requirements = python3, kivy, pandas, akshare, numpy, openpyxl, requests, certifi, urllib3, chardet, idna

version = 1.0
orientation = portrait

# 安卓权限：网络和读写
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 33
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
