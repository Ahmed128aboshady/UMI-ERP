import psycopg2

conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
cur = conn.cursor()

cur.execute("""
    SELECT c.id, c.name, curr.name AS currency
    FROM res_company c
    JOIN res_currency curr ON c.currency_id = curr.id
    ORDER BY c.id;
""")
companies = cur.fetchall()
print("=== INSTALLED COMPANIES ===")
for comp in companies:
    print(f"Company ID: {comp[0]} | Name: {comp[1]} | Currency: {comp[2]}")

cur.execute("SELECT name, symbol, active FROM res_currency WHERE active=TRUE;")
currencies = cur.fetchall()
print("\n=== ACTIVE CURRENCIES ===")
for curr in currencies:
    print(f"Currency: {curr[0]} | Symbol: {curr[1]} | Active: {curr[2]}")

cur.close()
conn.close()
