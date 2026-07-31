import time
from playwright.sync_api import sync_playwright

print("=====================================================")
print("STARTING LIVE VISUAL DEMO AUTOMATION FOR OBS RECORDING...")
print("=====================================================")

with sync_playwright() as p:
    # Launch Chrome Headful with maximized window
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
        print("Logging in as Admin...")
        page.fill("input[name='login']", "admin")
        page.fill("input[name='password']", "admin")
        page.click("button[type='submit']")
        page.wait_for_timeout(3000)

    # 2. Employees Directory
    print("2. Navigating to Employees Directory...")
    page.goto("http://localhost:8069/odoo/employees")
    page.wait_for_timeout(3000)
    # Smooth scroll down to show all 20 employees
    page.evaluate("window.scrollBy({top: 400, behavior: 'smooth'})")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollBy({top: 400, behavior: 'smooth'})")
    page.wait_for_timeout(3000)

    # 3. Sales Order (150,000 AED Emaar Contract)
    print("3. Navigating to Sales Orders...")
    page.goto("http://localhost:8069/odoo/sales")
    page.wait_for_timeout(3000)

    # Click on Sale Order S00006 or Emaar
    emaar_so = page.locator("td:has-text('Emaar Properties'), tr:has-text('S00006')").first
    if emaar_so.is_visible():
        print("Opening Sales Order S00006 (Emaar Properties)...")
        emaar_so.click()
        page.wait_for_timeout(4000)

    # 4. Project & Kanban Stages
    print("4. Navigating to Project & Kanban Board...")
    page.goto("http://localhost:8069/odoo/action-project.open_view_project_all")
    page.wait_for_timeout(3000)

    emaar_proj = page.locator(".o_kanban_record:has-text('Emaar')").first
    if emaar_proj.is_visible():
        print("Opening Emaar Project Kanban Board...")
        emaar_proj.click()
        page.wait_for_timeout(4000)

    # Smooth scroll across Kanban stages
    page.evaluate("window.scrollBy({left: 500, behavior: 'smooth'})")
    page.wait_for_timeout(3000)

    # 5. Timesheets & Logged Hours (273 Hours)
    print("5. Navigating to Timesheets (273.0 Hours Logged)...")
    page.goto("http://localhost:8069/odoo/action-hr_timesheet.act_hr_timesheet_line_ev_all")
    page.wait_for_timeout(3000)
    page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
    page.wait_for_timeout(2000)
    page.evaluate("window.scrollBy({top: 300, behavior: 'smooth'})")
    page.wait_for_timeout(3000)

    # 6. Time Off & Leave Allocations (21 Days Annual Paid Leave)
    print("6. Navigating to Time Off (Leaves & Allocations)...")
    page.goto("http://localhost:8069/odoo/action-hr_holidays.hr_leave_action_action_approve_department")
    page.wait_for_timeout(4000)

    # 7. Dashboards Summary
    print("7. Returning to Main Executive Dashboard...")
    page.goto("http://localhost:8069/odoo")
    page.wait_for_timeout(5000)

    print("=====================================================")
    print("LIVE DEMO RECORDING COMPLETED SUCCESSFULLY!")
    print("=====================================================")
    browser.close()
