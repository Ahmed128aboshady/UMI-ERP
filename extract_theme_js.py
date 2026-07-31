import urllib.request
import re

url = "http://localhost:8069/web/assets/7d97c33/web.assets_web.min.js"
req = urllib.request.urlopen(url)
js = req.read().decode('utf-8', errors='ignore')

matches = [m.start() for m in re.finditer("EnterpriseHomeDashboard", js)]
for m in matches:
    print("--- MATCH AT ---", m)
    print(js[max(0, m-100):min(len(js), m+400)])
