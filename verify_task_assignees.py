import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("""
    SELECT t.id, t.name, string_agg(p.name, ', ') AS assignees
    FROM project_task t
    LEFT JOIN project_task_user_rel rel ON t.id = rel.task_id
    LEFT JOIN res_users u ON rel.user_id = u.id
    LEFT JOIN res_partner p ON u.partner_id = p.id
    GROUP BY t.id, t.name
    ORDER BY t.id;
""")
rows = cur.fetchall()

print("=== PROJECT TASKS & ASSIGNEES ===")
for r in rows:
    print(f"Task ID: {r[0]} | Title: {r[1]} | Assignees: {r[2]}")

cur.close()
conn.close()
