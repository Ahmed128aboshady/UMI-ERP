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

    admin_user = env['res.users'].browse(1)
    
    # Search all groups containing Project
    proj_groups = env['res.groups'].search([('name', 'ilike', 'Project')])
    print("PROJECT GROUPS FOUND:", proj_groups.mapped('name'))

    for g in proj_groups:
        if admin_user.id not in g.user_ids.ids:
            g.write({'user_ids': [(4, admin_user.id)]})

    # Also grant Project Administrator & User XML groups
    try:
        group_proj_user = env.ref('project.group_project_user', raise_if_not_found=False)
        group_proj_manager = env.ref('project.group_project_manager', raise_if_not_found=False)
        group_proj_stages = env.ref('project.group_project_stages', raise_if_not_found=False)
        for grp in [group_proj_user, group_proj_manager, group_proj_stages]:
            if grp and admin_user.id not in grp.user_ids.ids:
                grp.write({'user_ids': [(4, admin_user.id)]})
                print(f"ADDED ADMIN TO GROUP: {grp.name}")
    except Exception as e:
        print("REF ERROR:", e)

    cr.commit()
    print("GRANTED ALL PROJECT GROUPS TO ADMIN USER!")
