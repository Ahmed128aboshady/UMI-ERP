import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("UPDATE ir_module_module SET state='uninstalled' WHERE name='web_responsive';")
cur.execute("DELETE FROM ir_asset WHERE path LIKE '%web_responsive%';")
conn.commit()

print("UNINSTALLED web_responsive FROM DB!")
cur.close()
conn.close()
