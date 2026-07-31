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

    # Set company_id = False for all employees so they appear globally across all companies (UAE & Egypt)
    employees = env['hr.employee'].search([])
    employees.write({'company_id': False})
    
    # Also set company_id = False on departments and jobs so all departments appear globally
    env['hr.department'].search([]).write({'company_id': False})
    env['hr.job'].search([]).write({'company_id': False})

    cr.commit()
    print(f"SUCCESSFULLY UPDATED {len(employees)} EMPLOYEES TO BE GLOBAL ACROSS ALL COMPANIES!")
