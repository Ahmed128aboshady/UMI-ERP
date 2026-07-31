from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        browser = p.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
        print("LAUNCHED CHROME HEADFUL SUCCESSFULLY!")
        page = browser.new_page(no_viewport=True)
        page.goto("http://localhost:8069/odoo")
        page.wait_for_timeout(3000)
        browser.close()
    except Exception as e:
        print("CHROME CHANNEL ERROR, TRYING DEFAULT CHROMIUM:", e)
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        print("LAUNCHED CHROMIUM HEADFUL SUCCESSFULLY!")
        page = browser.new_page(no_viewport=True)
        page.goto("http://localhost:8069/odoo")
        page.wait_for_timeout(3000)
        browser.close()
