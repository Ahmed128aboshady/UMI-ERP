import psycopg2

try:
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
    cur = conn.cursor()
    cur.execute("DELETE FROM ir_attachment WHERE name LIKE '%%assets%%';")
    conn.commit()
    print("DELETED OLD ASSETS ATTACHMENTS SUCCESSFULLY:", cur.rowcount)
    cur.close()
    conn.close()
except Exception as e:
    print("Error:", e)
