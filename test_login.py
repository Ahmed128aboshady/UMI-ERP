import requests
import re

session = requests.Session()
login_url = "http://localhost:8069/web/login"

# GET login page
res_get = session.get(login_url)
match = re.search(r'name="csrf_token"\s+value="([^"]+)"', res_get.text)
csrf_token = match.group(1) if match else ''

payload = {
    'login': 'admin',
    'password': 'admin',
    'csrf_token': csrf_token
}

res_post = session.post(login_url, data=payload, allow_redirects=True)
print("STATUS CODE:", res_post.status_code)
print("FINAL URL:", res_post.url)
print("IS ACCESS DENIED IN CONTENT:", "Access Denied" in res_post.text or "Forbidden" in res_post.text)
print("IS LOGGED IN (contains odoo or webclient):", "webclient" in res_post.text or "odoo" in res_post.url)
