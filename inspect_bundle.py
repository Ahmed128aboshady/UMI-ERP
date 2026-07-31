import urllib.request

try:
    url = 'http://localhost:8069/web/assets/9e0afda/web.assets_frontend.min.css'
    req = urllib.request.urlopen(url)
    css_content = req.read().decode('utf-8')
    print("--- CSS BUNDLE CONTENT ---")
    print(css_content)
except Exception as e:
    print("Error:", e)
