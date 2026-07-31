import time
from playwright.sync_api import sync_playwright

print("=====================================================")
print("STARTING LIVE AUTOMATED DEMO FOR DUBAI POLICE PROJECT...")
print("=====================================================")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        channel="chrome",
        args=["--start-maximized", "--force-device-scale-factor=1.0"]
    )
    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    # 1. Login to Odoo
    print("1. Opening Odoo Login Page...")
    page.goto("http://localhost:8069/web/login")
    page.wait_for_timeout(2000)

    if page.locator("input[name='login']").is_visible():
        page.fill("input[name='login']", "admin")
        page.fill("input[name='password']", "admin")
        page.click("button[type='submit']")
        page.wait_for_timeout(3000)

    # 2. Sales Orders - Open Dubai Police Contract (250,000 AED)
    print("2. Opening Sales Orders for Dubai Police HQ (250,000 AED)...")
    page.goto("http://localhost:8069/odoo/sales")
    page.wait_for_timeout(3000)

    police_so = page.locator("td:has-text('Dubai Police'), tr:has-text('Dubai Police')").first
    if police_so.is_visible():
        police_so.click()
        page.wait_for_timeout(4000)

    # 3. Open Dubai Police Project Kanban & Stages
    print("3. Navigating to Dubai Police Project Kanban Board...")
    page.goto("http://localhost:8069/odoo/action-project.open_view_project_all")
    page.wait_for_timeout(3000)

    police_proj = page.locator(".o_kanban_record:has-text('Dubai Police')").first
    if police_proj.is_visible():
        police_proj.click()
        page.wait_for_timeout(4000)

    # Scroll Kanban Board
    page.evaluate("window.scrollBy({left: 500, behavior: 'smooth'})")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy({left: 500, behavior: 'smooth'})")
    page.wait_for_timeout(3000)

    # 4. Timesheets View
    print("4. Navigating to Dubai Police Timesheets...")
    page.goto("http://localhost:8069/odoo/action-hr_timesheet.act_hr_timesheet_line_ev_all")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
    page.wait_for_timeout(3000)

    # 5. Dashboards Summary (Both Projects: Emaar & Dubai Police)
    print("5. Returning to Executive Dashboard Summary...")
    page.goto("http://localhost:8069/odoo")
    page.wait_for_timeout(5000)

    print("=====================================================")
    print("DUBAI POLICE LIVE AUTOMATED DEMO COMPLETED!")
    print("=====================================================")
    browser.close()
