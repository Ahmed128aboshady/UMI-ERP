import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("""
    SELECT m.id, m.name, m.web_icon
    FROM ir_ui_menu m
    WHERE m.parent_id IS NULL
    LIMIT 20;
""")

for row in cur.fetchall():
    menu_id, name, web_icon = row
    print("----------------------------------------")
    print(f"ID: {menu_id} | NAME: {name} | WEB_ICON: {web_icon}")

cur.close()
conn.close()
