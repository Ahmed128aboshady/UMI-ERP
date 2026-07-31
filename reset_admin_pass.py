import psycopg2
from passlib.context import CryptContext

try:
    # Hash password 'admin' using passlib pbkdf2_sha512
    ctx = CryptContext(schemes=['pbkdf2_sha512', 'plaintext'])
    hashed_password = ctx.hash('admin')

    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
    cur = conn.cursor()

    cur.execute("SELECT id, login, active, password FROM res_users WHERE login = 'admin';")
    users = cur.fetchall()
    print("USERS BEFORE RESET:", users)

    if users:
        cur.execute("UPDATE res_users SET password = %s, active = true WHERE login = 'admin';", (hashed_password,))
        conn.commit()
        print("UPDATED ADMIN PASSWORD TO 'admin' SUCCESSFULLY!")
    else:
        print("ADMIN USER NOT FOUND IN DB!")

    cur.close()
    conn.close()

except Exception as e:
    print("Error resetting password:", e)
