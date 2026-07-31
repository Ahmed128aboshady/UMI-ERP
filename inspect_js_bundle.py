import urllib.request
import re

url = "http://localhost:8069/web/assets/7d97c33/web.assets_web.min.js"
try:
    req = urllib.request.urlopen(url)
    js_content = req.read().decode('utf-8', errors='ignore')
    print("FETCHED JS BUNDLE LENGTH:", len(js_content))
    if "umi_enterprise_theme" in js_content:
        print("FOUND umi_enterprise_theme IN JS BUNDLE!")
    else:
        print("umi_enterprise_theme NOT FOUND IN JS BUNDLE!")
except Exception as e:
    print("ERROR FETCHING JS BUNDLE:", e)
