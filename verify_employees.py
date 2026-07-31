import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("SELECT name FROM hr_employee ORDER BY id;")
employees = cur.fetchall()

print(f"=== UMI ERP EMPLOYEES DIRECTORY ({len(employees)} TOTAL) ===")
for emp in employees:
    print(f"Employee Name: {emp[0]}")

cur.close()
conn.close()
