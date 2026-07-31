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

    # Search all 20 Employees
    employees = env['hr.employee'].search([('name', '!=', 'Administrator')])

    # Default internal user group
    group_internal = env.ref('base.group_user')
    group_proj_user = env.ref('project.group_project_user', raise_if_not_found=False)

    users_by_emp = {}
    for emp in employees:
        if not emp.user_id:
            # Create user for employee
            login = emp.work_email or f"{emp.name.lower().replace(' ', '.')}@umi.com"
            user = env['res.users'].search([('login', '=', login)], limit=1)
            if not user:
                user = env['res.users'].create({
                    'name': emp.name,
                    'login': login,
                    'email': login,
                    'company_id': emp.company_id.id if emp.company_id else uae_company.id,
                    'company_ids': [(6, 0, [uae_company.id, egypt_company.id])],
                    'group_ids': [(6, 0, [group_internal.id, group_proj_user.id] if group_proj_user else [group_internal.id])],
                })
            emp.write({'user_id': user.id})
            users_by_emp[emp.name] = user
            print(f"CREATED USER FOR {emp.name}: {user.login}")
        else:
            users_by_emp[emp.name] = emp.user_id

    # Helper function to get User IDs for employee names
    def get_user_ids(emp_names):
        uids = []
        for name in emp_names:
            emp = env['hr.employee'].search([('name', 'ilike', name)], limit=1)
            if emp and emp.user_id:
                uids.append(emp.user_id.id)
        return uids

    # 2. Update Tasks Assignees
    tasks_assignees = {
        'Task 1: Client Requirements & Project Brief': ['Firas', 'Aya Salah'],
        'Task 2: 2D Brand Identity & Visual Style Guide': ['Yara Khamis', 'Saeed Ali', 'Mohamed Abdelnabi'],
        'Task 3: 3D Exterior Villa Modeling & Texturing': ['Mohamed Mahmoud', 'Dina', 'Sara', 'Hana'],
        'Task 4: 3D Interior Living & Master Suite Rendering': ['Rawan', 'Mai', 'Logy', 'Marwan', 'Nouran', 'Omnia'],
        'Task 5: AI Concept Generation & Social Media Campaign': ['Hadeer Moustafa', 'Ahmed Nasr', 'Ahmed Youssef'],
        'Task 6: Final Review & Client Sign-Off': ['Firas', 'Marwa'],
    }

    for task_name, emp_names in tasks_assignees.items():
        uids = get_user_ids(emp_names)
        tasks = env['project.task'].search([('name', 'ilike', task_name)])
        for t in tasks:
            t.write({'user_ids': [(6, 0, uids)]})
            print(f"ASSIGNED ASSIGNEES TO {t.name}: {emp_names}")

    cr.commit()
    print("SUCCESSFULLY CREATED USERS FOR ALL 20 EMPLOYEES & ASSIGNED ASSIGNEES TO ALL TASKS!")
