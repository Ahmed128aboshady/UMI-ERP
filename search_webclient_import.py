import os

web_src = r"D:\UMI ERP\odoo-19.0.post20260506\odoo\addons\web\static\src"
for root, dirs, files in os.walk(web_src):
    for f in files:
        if f.endswith('.js'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                if 'WebClient.prototype' in content or 'patch(NavBar' in content or 'patch(WebClient' in content:
                    print(f"FOUND IN: {filepath}")
