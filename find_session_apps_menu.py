import os

target_dir = r"D:\UMI ERP\oca_web\web_responsive"
for root, dirs, files in os.walk(target_dir):
    for f in files:
        if f.endswith(('.js', '.py', '.xml', '.scss')):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                if 'session.apps_menu' in content or 'isSmall' in content:
                    print(f"FOUND IN: {filepath}")
