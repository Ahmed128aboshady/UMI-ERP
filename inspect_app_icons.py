import urllib.request
import urllib.parse
import json

# Login first
login_url = 'http://localhost:8069/web/login'
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())

login_data = urllib.parse.urlencode({
    'login': 'admin',
    'password': 'admin',
    'db': 'umi_erp_db'
}).encode('utf-8')

opener.open(login_url, login_data)

res = opener.open('http://localhost:8069/web/webclient/load_menus')
data = json.loads(res.read().decode('utf-8'))

root_children = data['root']['children']
print(f"TOTAL ROOT APPS: {len(root_children)}")

for child_id in root_children[:15]:
    app = data[str(child_id)]
    print("----------------------------------------")
    print(f"NAME: {app.get('name')}")
    print(f"XMLID: {app.get('xmlid')}")
    print(f"WEB_ICON: {app.get('webIcon')}")
    print(f"WEB_ICON_DATA: {bool(app.get('webIconData'))}")
    if app.get('webIconData'):
        print(f"WEB_ICON_DATA SAMPLE: {app.get('webIconData')[:40]}...")
