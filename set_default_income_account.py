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
        # Check if Income Account exists
        income_acc = env['account.account'].search([('company_ids', 'in', comp.id), ('account_type', '=', 'income')], limit=1)
        if not income_acc:
            income_acc = env['account.account'].search([('account_type', '=', 'income')], limit=1)
        if not income_acc:
            income_acc = env['account.account'].create({
                'name': 'Sales / Service Revenue',
                'code': f'4000{comp.id}',
                'account_type': 'income',
                'company_ids': [(4, comp.id)],
            })
            print(f"CREATED INCOME ACCOUNT FOR {comp.name}")

        # Set default income account on Product Category All
        cat = env['product.category'].search([], limit=1)
        if cat:
            cat.write({'property_account_income_categ_id': income_acc.id})
            print(f"SET INCOME ACCOUNT {income_acc.name} ON PRODUCT CATEGORY {cat.name}")

    cr.commit()
    print("INCOME ACCOUNT SETUP COMPLETED SUCCESSFULLY!")
