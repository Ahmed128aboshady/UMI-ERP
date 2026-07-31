import psycopg2
import os

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

# Get filestore base path
# Default Windows filestore path: C:\Users\Mada\AppData\Local\OpenERP S.A.\Odoo\filestore\umi_erp_db
filestore_base = r"C:\Users\Mada\AppData\Local\OpenERP S.A.\Odoo\filestore\umi_erp_db"

cur.execute("SELECT id, name, url, store_fname FROM ir_attachment WHERE store_fname IS NOT NULL;")
rows = cur.fetchall()

missing_ids = []
for att_id, name, url, store_fname in rows:
    full_path = os.path.join(filestore_base, store_fname)
    if not os.path.exists(full_path):
        missing_ids.append(att_id)

print(f"FOUND {len(missing_ids)} MISSING FILESTORE ATTACHMENTS.")
if missing_ids:
    cur.execute("DELETE FROM ir_attachment WHERE id IN %s;", (tuple(missing_ids),))
    conn.commit()
    print("DELETED MISSING ATTACHMENTS FROM DB!")

cur.close()
conn.close()
