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

    uae_company = env['res.company'].search([('name', 'ilike', 'UMI General Trading')], limit=1)
    egypt_company = env['res.company'].search([('name', 'ilike', 'UMI Egypt')], limit=1)

    # 1. Assign all 20 employees to company 1 (UMI General Trading L.L.C) so they all show up in default view
    employees = env['hr.employee'].search([])
    employees.write({'company_id': uae_company.id})
    print(f"ASSIGNED {len(employees)} EMPLOYEES TO UMI General Trading L.L.C (COMPANY 1)")

    # 2. Update Admin user to have access to BOTH companies (UAE & Egypt)
    admin_user = env['res.users'].browse(1)
    admin_user.write({
        'company_id': uae_company.id,
        'company_ids': [(6, 0, [uae_company.id, egypt_company.id])],
    })
    print("UPDATED ADMIN USER TO HAVE ACCESS TO BOTH COMPANIES (UAE & EGYPT)!")

    cr.commit()
    print("ALL EMPLOYEES ARE NOW VISIBLE TOGETHER!")
