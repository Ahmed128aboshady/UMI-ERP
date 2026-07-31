import os
import sys
import subprocess

print("=====================================================")
print("BUILDING COMPLETE UMI ERP DEMO SYSTEM FROM SCRATCH...")
print("=====================================================")

scripts = [
    r"D:\UMI ERP\create_umi_employees.py",
    r"D:\UMI ERP\set_admin_all_companies.py",
    r"D:\UMI ERP\set_default_income_account.py",
    r"D:\UMI ERP\create_full_demo_cycle.py",
    r"D:\UMI ERP\assign_users_via_orm.py",
    r"D:\UMI ERP\setup_leaves_and_overtime.py",
    r"D:\UMI ERP\create_dubai_police_data.py"
]

for s in scripts:
    if os.path.exists(s):
        print(f"\n---> Running: {os.path.basename(s)}...")
        res = subprocess.run([sys.executable, s], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"SUCCESS: {os.path.basename(s)}")
        else:
            print(f"ERROR in {os.path.basename(s)}: {res.stderr}")

print("\n=====================================================")
print("COMPLETE DEMO SYSTEM REBUILT SUCCESSFULLY!")
print("=====================================================")
