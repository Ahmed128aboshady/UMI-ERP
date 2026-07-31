import psycopg2, shutil, os

try:
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
    cur = conn.cursor()
    cur.execute("DELETE FROM ir_attachment WHERE url LIKE '%%assets%%' OR name LIKE '%%assets%%' OR name LIKE '%%web.assets%%';")
    print("DELETED ATTACHMENT ROWS:", cur.rowcount)
    conn.commit()
    cur.close()
    conn.close()

    filestore_dir = os.path.expanduser(r'~\AppData\Local\OpenERP S.A.\Odoo\filestore\umi_erp_db')
    if os.path.exists(filestore_dir):
        shutil.rmtree(filestore_dir)
        print("REMOVED FILESTORE DIR:", filestore_dir)

except Exception as e:
    print("Error:", e)
