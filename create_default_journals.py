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

    companies = env['res.company'].search([])
    for comp in companies:
        # Check Sales Journal
        sale_journal = env['account.journal'].search([('company_id', '=', comp.id), ('type', '=', 'sale')], limit=1)
        if not sale_journal:
            env['account.journal'].create({
                'name': 'Customer Invoices',
                'code': 'INV',
                'type': 'sale',
                'company_id': comp.id,
                'currency_id': comp.currency_id.id,
            })
            print(f"CREATED SALES JOURNAL FOR {comp.name}")

        # Check Purchase Journal
        purchase_journal = env['account.journal'].search([('company_id', '=', comp.id), ('type', '=', 'purchase')], limit=1)
        if not purchase_journal:
            env['account.journal'].create({
                'name': 'Vendor Bills',
                'code': 'BILL',
                'type': 'purchase',
                'company_id': comp.id,
                'currency_id': comp.currency_id.id,
            })
            print(f"CREATED PURCHASE JOURNAL FOR {comp.name}")

    cr.commit()
    print("DEFAULT JOURNALS CREATED CLEANLY FOR ALL COMPANIES!")
