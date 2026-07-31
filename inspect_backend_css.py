import requests
import re

session = requests.Session()
login_url = "http://localhost:8069/web/login"

res_get = session.get(login_url)
match = re.search(r'name="csrf_token"\s+value="([^"]+)"', res_get.text)
csrf_token = match.group(1) if match else ''

payload = {
    'login': 'admin',
    'password': 'admin',
    'csrf_token': csrf_token
}

res_post = session.post(login_url, data=payload, allow_redirects=True)

res_web = session.get("http://localhost:8069/web")
all_css = re.findall(r'href="([^"]+\.css[^"]*)"', res_web.text)

for css_url in all_css:
    full_url = "http://localhost:8069" + css_url
    res_css = session.get(full_url)
    print(f"\n=== CSS URL: {css_url} | Size: {len(res_css.text)} bytes ===")
    if "css error" in res_css.text.lower() or "error:" in res_css.text.lower():
        safe_text = res_css.text[:3000].encode('ascii', errors='backslashreplace').decode('ascii')
        print(safe_text)
    else:
        print("CSS OK!")
