import psycopg2

try:
    conn = psycopg2.connect(host='127.0.0.1', port=5432, user='odoo', password='odoo', dbname='umi_erp_db')
    cur = conn.cursor()

    # 1. Active Multi-Currency currencies: AED, EGP, USD, EUR
    cur.execute("UPDATE res_currency SET active=TRUE WHERE name IN ('AED', 'EGP', 'USD', 'EUR');")

    # Get currency IDs
    cur.execute("SELECT name, id FROM res_currency WHERE name IN ('AED', 'EGP', 'USD', 'EUR');")
    currencies = dict(cur.fetchall())
    print("ACTIVE CURRENCIES:", currencies)

    # 2. Update Main Company (ID 1) to UMI General Trading L.L.C with AED currency
    cur.execute("""
        UPDATE res_company 
        SET name='UMI General Trading L.L.C', currency_id=%s
        WHERE id=1;
    """, (currencies.get('AED', 1),))

    # Update main partner name
    cur.execute("""
        UPDATE res_partner
        SET name='UMI General Trading L.L.C'
        WHERE id=(SELECT partner_id FROM res_company WHERE id=1);
    """)
    print("UPDATED MAIN COMPANY TO UMI General Trading L.L.C (AED)")

    # 3. Create or Update Secondary Company: UMI Egypt (EGP)
    cur.execute("SELECT id FROM res_company WHERE name LIKE '%UMI Egypt%';")
    egypt_company = cur.fetchone()

    if not egypt_company:
        # Create partner first
        cur.execute("""
            INSERT INTO res_partner (name, is_company, active, autopost_bills, create_date, write_date)
            VALUES ('UMI Egypt', TRUE, TRUE, 'ask', NOW(), NOW())
            RETURNING id;
        """)
        partner_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO res_company (name, partner_id, currency_id, sequence, create_date, write_date)
            VALUES ('UMI Egypt', %s, %s, 10, NOW(), NOW())
            RETURNING id;
        """, (partner_id, currencies.get('EGP', 1)))
        egypt_company_id = cur.fetchone()[0]

        # Link company_id on partner
        cur.execute("UPDATE res_partner SET company_id=%s WHERE id=%s;", (egypt_company_id, partner_id))
        print(f"CREATED SECONDARY COMPANY UMI Egypt (ID: {egypt_company_id}, Partner: {partner_id}) WITH EGP")
    else:
        egypt_company_id = egypt_company[0]
        cur.execute("""
            UPDATE res_company 
            SET currency_id=%s 
            WHERE id=%s;
        """, (currencies.get('EGP', 1), egypt_company_id))
        print(f"UPDATED SECONDARY COMPANY UMI Egypt (ID: {egypt_company_id}) WITH EGP")

    conn.commit()
    cur.close()
    conn.close()
    print("MULTI-COMPANY & MULTI-CURRENCY SETUP COMPLETED SUCCESSFULLY!")

except Exception as e:
    print("ERROR IN SETUP:", e)
