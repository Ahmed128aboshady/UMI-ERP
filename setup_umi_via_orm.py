import os
import sys

sys.path.insert(0, r"D:\UMI ERP\odoo-19.0.post20260506")

import odoo
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry

config_path = r"D:\UMI ERP\odoo.conf"
odoo.tools.config.parse_config(['-c', config_path, '-d', 'umi_erp_db'])

registry = Registry('umi_erp_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    # 1. Activate Currencies: AED, EGP, USD, EUR using active_test=False
    Currency = env['res.currency'].with_context(active_test=False)
    currencies = Currency.search([('name', 'in', ['AED', 'EGP', 'USD', 'EUR'])])
    currencies.write({'active': True})
    print("ACTIVATED CURRENCIES:", currencies.mapped('name'))

    aed = Currency.search([('name', '=', 'AED')], limit=1)
    egp = Currency.search([('name', '=', 'EGP')], limit=1)

    # 2. Update Main Company
    main_company = env['res.company'].browse(1)
    main_company.write({
        'name': 'UMI General Trading L.L.C',
        'currency_id': aed.id,
    })
    main_company.partner_id.name = 'UMI General Trading L.L.C'
    print("UPDATED MAIN COMPANY TO UMI General Trading L.L.C (AED)")

    # 3. Create or Update Secondary Company: UMI Egypt
    Company = env['res.company'].with_context(active_test=False)
    egypt_company = Company.search([('name', 'ilike', 'UMI Egypt')], limit=1)
    if not egypt_company:
        egypt_company = Company.create({
            'name': 'UMI Egypt',
            'currency_id': egp.id,
        })
        print(f"CREATED SECONDARY COMPANY UMI Egypt (ID: {egypt_company.id}) WITH EGP")
    else:
        egypt_company.write({'currency_id': egp.id})
        print(f"UPDATED SECONDARY COMPANY UMI Egypt (ID: {egypt_company.id}) WITH EGP")

    cr.commit()
    print("ALL COMPANIES & CURRENCIES SET UP CLEANLY VIA ODOO ORM!")
