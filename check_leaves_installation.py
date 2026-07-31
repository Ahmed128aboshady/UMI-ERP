import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("SELECT name, state FROM ir_module_module WHERE name IN ('hr_holidays', 'hr_attendance');")
rows = cur.fetchall()
print("LEAVE MODULE STATES:", rows)

cur.close()
conn.close()
