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

    group_internal = env.ref('base.group_user')
    group_proj_user = env.ref('project.group_project_user', raise_if_not_found=False)

    # 1. Ensure User Account Exists For Every Single Employee
    employees = env['hr.employee'].search([('name', '!=', 'Administrator')])
    for emp in employees:
        if not emp.user_id:
            login = emp.work_email or f"{emp.name.lower().replace(' ', '.')}@umi.com"
            user = env['res.users'].search([('login', '=', login)], limit=1)
            if not user:
                user = env['res.users'].create({
                    'name': emp.name,
                    'login': login,
                    'email': login,
                    'company_id': uae_company.id,
                    'company_ids': [(6, 0, [uae_company.id, egypt_company.id])],
                    'group_ids': [(6, 0, [group_internal.id, group_proj_user.id] if group_proj_user else [group_internal.id])],
                })
            emp.write({'user_id': user.id})
            print(f"USER CREATED & LINKED FOR {emp.name}: User ID {user.id}")

    # Helper function to get User IDs for employee names
    def get_users_for_names(emp_names):
        u_list = []
        for n in emp_names:
            emp = env['hr.employee'].search([('name', 'ilike', n)], limit=1)
            if emp and emp.user_id:
                u_list.append(emp.user_id.id)
        return u_list

    # Map Tasks to Employee Names
    assignments = [
        (25, ['Firas', 'Aya Salah']),
        (26, ['Yara Khamis', 'Saeed Ali', 'Mohamed Abdelnabi']),
        (27, ['Mohamed Mahmoud', 'Dina', 'Sara', 'Hana']),
        (28, ['Rawan', 'Mai', 'Logy', 'Marwan', 'Nouran', 'Omnia']),
        (29, ['Hadeer Moustafa', 'Ahmed Nasr', 'Ahmed Youssef']),
        (30, ['Firas', 'Marwa']),
    ]

    for task_id, names in assignments:
        task = env['project.task'].browse(task_id)
        if task.exists():
            uids = get_users_for_names(names)
            task.write({'user_ids': [(6, 0, uids)]})
            print(f"ASSIGNED ASSIGNEES TO TASK {task.id} ({task.name}): {uids} -> {names}")

    cr.commit()
    print("FINISHED ALL TASK ASSIGNEE ASSIGNMENTS!")
