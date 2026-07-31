import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("""
    SELECT t.id, t.name, t.project_id, p.name AS proj_name
    FROM project_task t
    JOIN project_project p ON t.project_id = p.id;
""")
rows = cur.fetchall()

print("=== ALL TASKS IN DB ===")
for r in rows:
    print(f"Task ID: {r[0]} | Name: {r[1]} | Project ID: {r[2]} | Proj: {r[3]}")

cur.close()
conn.close()
