import sys

sys.path.insert(0, r"D:\UMI ERP\odoo-19.0.post20260506")

import odoo
from odoo import api, fields, SUPERUSER_ID
from odoo.modules.registry import Registry

config_path = r"D:\UMI ERP\odoo.conf"
odoo.tools.config.parse_config(['-c', config_path, '-d', 'umi_erp_db'])

registry = Registry('umi_erp_db')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})

    uae_company = env['res.company'].search([('name', 'ilike', 'UMI General Trading')], limit=1)
    aed = env['res.currency'].with_context(active_test=False).search([('name', '=', 'AED')], limit=1)
    income_acc = env['account.account'].search([('account_type', '=', 'income')], limit=1)

    # 1. Create Partner: Dubai Police General HQ
    police = env['res.partner'].search([('name', 'ilike', 'Dubai Police')], limit=1)
    if not police:
        police = env['res.partner'].create({
            'name': 'Dubai Police General HQ',
            'is_company': True,
            'street': 'Al Twar 1, Dubai Police Headquarters',
            'city': 'Dubai',
            'country_id': env.ref('base.ae').id,
            'email': 'projects@dubaipolice.gov.ae',
            'phone': '+971 4 609 9999',
            'company_id': uae_company.id,
        })

    # 2. Service Products
    p1_name = '3D Command Center & Smart Police Station Visualization'
    p2_name = 'AI Smart Traffic Awareness Campaign & Animation'
    p3_name = 'VR Interactive Training Platform Concept'

    prod1 = env['product.product'].search([('name', '=', p1_name)], limit=1)
    if not prod1:
        prod1 = env['product.product'].create({
            'name': p1_name, 'type': 'service', 'list_price': 120000.0,
            'property_account_income_id': income_acc.id if income_acc else False
        })
    prod2 = env['product.product'].search([('name', '=', p2_name)], limit=1)
    if not prod2:
        prod2 = env['product.product'].create({
            'name': p2_name, 'type': 'service', 'list_price': 80000.0,
            'property_account_income_id': income_acc.id if income_acc else False
        })
    prod3 = env['product.product'].search([('name', '=', p3_name)], limit=1)
    if not prod3:
        prod3 = env['product.product'].create({
            'name': p3_name, 'type': 'service', 'list_price': 50000.0,
            'property_account_income_id': income_acc.id if income_acc else False
        })

    # 3. Create Sales Order (SO) - 250,000 AED
    so = env['sale.order'].search([('partner_id', '=', police.id)], limit=1)
    if not so:
        so = env['sale.order'].create({
            'partner_id': police.id,
            'company_id': uae_company.id,
            'currency_id': aed.id,
            'order_line': [
                (0, 0, {'product_id': prod1.id, 'product_uom_qty': 1, 'price_unit': 120000.0}),
                (0, 0, {'product_id': prod2.id, 'product_uom_qty': 1, 'price_unit': 80000.0}),
                (0, 0, {'product_id': prod3.id, 'product_uom_qty': 1, 'price_unit': 50000.0}),
            ],
        })
        so.action_confirm()

    # 4. Project & Stages
    project = env['project.project'].search([('name', 'ilike', 'Dubai Police')], limit=1)
    if not project:
        project = env['project.project'].create({
            'name': 'Dubai Police - Smart Command Center & AI Campaign',
            'partner_id': police.id,
            'company_id': uae_company.id,
            'allow_timesheets': True,
        })

    stage_names = [
        '1. Requirements & Security Clearance',
        '2. 3D Architectural & VR Prototyping',
        '3. AI Media & Video Production',
        '4. High-Level Review & Simulation',
        '5. Security System Integration',
        '6. Final Handover & Official Sign-off'
    ]
    stages = {}
    for idx, s_name in enumerate(stage_names):
        stage = env['project.task.type'].search([('name', '=', s_name)], limit=1)
        if not stage:
            stage = env['project.task.type'].create({
                'name': s_name,
                'sequence': idx + 1,
            })
        stages[s_name] = stage
        if stage.id not in project.type_ids.ids:
            project.write({'type_ids': [(4, stage.id)]})

    # Helper function to get User IDs and Employee IDs
    def get_emp(name):
        return env['hr.employee'].search([('name', 'ilike', name)], limit=1)

    def get_user_ids(emp_names):
        uids = []
        for name in emp_names:
            emp = get_emp(name)
            if emp and emp.user_id:
                uids.append(emp.user_id.id)
        return uids

    # 5. Create Tasks and Log Timesheets
    tasks_data = [
        {
            'title': 'Task 1: Security Briefing & Asset Clearance',
            'stage': '1. Requirements & Security Clearance',
            'emps': ['Firas', 'Aya Salah', 'Marwa'],
            'timesheets': [
                ('Firas', 5.0, 'Executive Security Briefing with Dubai Police Leadership'),
                ('Aya Salah', 3.0, 'Team Clearance Documentation & Access Authorization'),
                ('Marwa', 2.0, 'HR Security Protocol Sign-off'),
            ]
        },
        {
            'title': 'Task 2: 3D Command Center & VR Layout Design',
            'stage': '2. 3D Architectural & VR Prototyping',
            'emps': ['Mohamed Mahmoud', 'Dina', 'Sara', 'Marwan'],
            'timesheets': [
                ('Mohamed Mahmoud', 15.0, '3D Command Center Main Control Hall Modeling'),
                ('Dina', 12.0, 'Hologram Display & Wall Screen Geometry'),
                ('Sara', 10.0, 'Realistic Lighting & Cyber Security Color Palette'),
                ('Marwan', 8.0, 'VR Camera Pathing & Real-time Unreal Engine Export'),
            ]
        },
        {
            'title': 'Task 3: Smart Police Station Exterior & Aerial Lighting',
            'stage': '2. 3D Architectural & VR Prototyping',
            'emps': ['Rawan', 'Mai', 'Hana', 'Logy', 'Nouran'],
            'timesheets': [
                ('Rawan', 12.0, 'Smart Police Station Exterior Facade Architectural Review'),
                ('Mai', 10.0, 'Glass & Metallic Material Shader Setup'),
                ('Hana', 10.0, 'Night Lighting & Drone Perspective Camera Pass'),
                ('Logy', 10.0, 'Police Vehicle 3D Models & Patrol Fleet Placement'),
                ('Nouran', 8.0, 'Post-Production Color Grading & Lens Flare FX'),
            ]
        },
        {
            'title': 'Task 4: AI Traffic Awareness Animation & Video Production',
            'stage': '3. AI Media & Video Production',
            'emps': ['Hadeer Moustafa', 'Ahmed Nasr', 'Ahmed Youssef', 'Yara Khamis', 'Saeed Ali', 'Mohamed Abdelnabi'],
            'timesheets': [
                ('Hadeer Moustafa', 10.0, 'Campaign Scriptwriting & Awareness Objectives'),
                ('Ahmed Nasr', 15.0, 'Midjourney & AI Prompt Generation for Patrol Concepts'),
                ('Ahmed Youssef', 10.0, 'Digital Marketing Strategy & Social Channels Prep'),
                ('Yara Khamis', 10.0, '2D Infographics & Motion Graphics Elements'),
                ('Saeed Ali', 8.0, 'Typography & Arabic Dubbing Audio Sync'),
                ('Mohamed Abdelnabi', 7.0, 'Video Assembly & Final Cut Export'),
            ]
        },
        {
            'title': 'Task 5: High-Level Review & Official Sign-Off',
            'stage': '6. Final Handover & Official Sign-off',
            'emps': ['Firas', 'Omnia', 'Geleen'],
            'timesheets': [
                ('Firas', 5.0, 'Official Presentation to Dubai Police High Command'),
                ('Omnia', 6.0, 'Interactive Presentation Pack Final Touches'),
                ('Geleen', 4.0, 'Operations Handover & Client Approval Signing'),
            ]
        },
    ]

    for t_data in tasks_data:
        task = env['project.task'].search([('name', '=', t_data['title']), ('project_id', '=', project.id)], limit=1)
        uids = get_user_ids(t_data['emps'])
        if not task:
            task = env['project.task'].create({
                'name': t_data['title'],
                'project_id': project.id,
                'stage_id': stages[t_data['stage']].id,
                'user_ids': [(6, 0, uids)],
            })
        else:
            task.write({'user_ids': [(6, 0, uids)]})

        for emp_name, hours, desc in t_data['timesheets']:
            emp = get_emp(emp_name)
            if emp:
                ts = env['account.analytic.line'].search([('task_id', '=', task.id), ('employee_id', '=', emp.id), ('name', '=', desc)], limit=1)
                if not ts:
                    env['account.analytic.line'].create({
                        'name': desc,
                        'project_id': project.id,
                        'task_id': task.id,
                        'employee_id': emp.id,
                        'unit_amount': hours,
                        'date': fields.Date.today(),
                    })

    cr.commit()
    print("DUBAI POLICE PROJECT DATA GENERATED CLEANLY IN ODOO!")
