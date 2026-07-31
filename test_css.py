import urllib.request, re

try:
    req = urllib.request.urlopen('http://localhost:8069/web/login')
    html = req.read().decode('utf-8')
    css_urls = re.findall(r'href="(/web/assets/[^"]+)"', html)
    print('CSS URLs found:', css_urls)
    for url in css_urls:
        full_url = 'http://localhost:8069' + url
        css_req = urllib.request.urlopen(full_url)
        css_content = css_req.read().decode('utf-8')
        print(f'{url} -> length {len(css_content)} bytes')
        if len(css_content) < 500:
            print("CSS PREVIEW:", css_content[:200])
except Exception as e:
    print("Error:", e)
