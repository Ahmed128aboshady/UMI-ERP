import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("SELECT name, state FROM ir_module_module WHERE name IN ('project', 'hr_timesheet', 'sale_project');")
rows = cur.fetchall()
print("PROJECT MODULE STATES:", rows)

cur.close()
conn.close()
