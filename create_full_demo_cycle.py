import os
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

    # 1. Create/Find Customer Partner: Emaar Properties PJSC
    emaar = env['res.partner'].search([('name', 'ilike', 'Emaar Properties')], limit=1)
    if not emaar:
        emaar = env['res.partner'].create({
            'name': 'Emaar Properties PJSC',
            'is_company': True,
            'street': 'Downtown Dubai, Emaar Square',
            'city': 'Dubai',
            'country_id': env.ref('base.ae').id,
            'email': 'projects@emaar.ae',
            'phone': '+971 4 367 3333',
            'company_id': uae_company.id,
        })
    print(f"1. CLIENT PARTNER CREATED: {emaar.name} (ID: {emaar.id})")

    # 2. Create Service Products for Sales Order
    products_data = [
        ('3D Architectural Exterior & Interior Rendering', 80000.0),
        ('2D Brand Identity & VR Presentation Pack', 40000.0),
        ('Digital Marketing & AI Concept Campaign', 30000.0),
    ]
    products = {}
    for p_name, price in products_data:
        prod = env['product.product'].search([('name', '=', p_name)], limit=1)
        if not prod:
            prod = env['product.product'].create({
                'name': p_name,
                'type': 'service',
                'list_price': price,
                'standard_price': price * 0.4,
                'property_account_income_id': income_acc.id if income_acc else False,
            })
        elif income_acc:
            prod.write({'property_account_income_id': income_acc.id})
        products[p_name] = prod
    print("2. PRODUCTS CREATED/FOUND:", list(products.keys()))

    # 3. Create Sales Order (SO)
    so = env['sale.order'].search([('partner_id', '=', emaar.id)], limit=1)
    if not so:
        so = env['sale.order'].create({
            'partner_id': emaar.id,
            'company_id': uae_company.id,
            'currency_id': aed.id,
            'order_line': [
                (0, 0, {'product_id': products['3D Architectural Exterior & Interior Rendering'].id, 'product_uom_qty': 1, 'price_unit': 80000.0}),
                (0, 0, {'product_id': products['2D Brand Identity & VR Presentation Pack'].id, 'product_uom_qty': 1, 'price_unit': 40000.0}),
                (0, 0, {'product_id': products['Digital Marketing & AI Concept Campaign'].id, 'product_uom_qty': 1, 'price_unit': 30000.0}),
            ],
        })
        # Confirm Sale Order
        so.action_confirm()
    print(f"3. SALES ORDER CONFIRMED: {so.name} (Total: {so.amount_total} AED)")

    # 4. Create Project & Stages
    project = env['project.project'].search([('name', 'ilike', 'Emaar - Dubai Hills')], limit=1)
    if not project:
        project = env['project.project'].create({
            'name': 'Emaar - Dubai Hills Luxury Villa 3D & Branding',
            'partner_id': emaar.id,
            'company_id': uae_company.id,
            'allow_timesheets': True,
        })
    print(f"4. PROJECT CREATED: {project.name} (ID: {project.id})")

    # Project Task Stages
    stage_names = [
        '1. Brief & Discovery',
        '2. 2D & Moodboard Design',
        '3. 3D Modeling & Rendering',
        '4. Digital Campaign & AI Assets',
        '5. Client Review & Revisions',
        '6. Final Delivery & Sign-off'
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

    # Helper to get Employee Record
    def get_emp(emp_name):
        return env['hr.employee'].search([('name', 'ilike', emp_name)], limit=1)

    # 5. Create Tasks and Log Real Timesheets
    tasks_data = [
        {
            'title': 'Task 1: Client Requirements & Project Brief',
            'stage': '1. Brief & Discovery',
            'emps': ['Firas', 'Aya Salah'],
            'timesheets': [
                ('Firas', 5.0, 'Initial Client Briefing & Scope Definition with Emaar Executives'),
                ('Aya Salah', 3.0, 'Project Resource Planning & Team Allocation Setup'),
            ]
        },
        {
            'title': 'Task 2: 2D Brand Identity & Visual Style Guide',
            'stage': '2. 2D & Moodboard Design',
            'emps': ['Yara Khamis', 'Saeed Ali', 'Mohamed Abdelnabi'],
            'timesheets': [
                ('Yara Khamis', 16.0, '2D Branding Concepts & Logo Options Creation'),
                ('Saeed Ali', 12.0, 'Color Palette & Typography Selection'),
                ('Mohamed Abdelnabi', 10.0, 'Visual Guidelines & Asset Exports for Client'),
            ]
        },
        {
            'title': 'Task 3: 3D Exterior Villa Modeling & Texturing',
            'stage': '3. 3D Modeling & Rendering',
            'emps': ['Mohamed Mahmoud', 'Dina', 'Sara', 'Hana'],
            'timesheets': [
                ('Mohamed Mahmoud', 20.0, '3D Architecture Setup & Team Supervision'),
                ('Dina', 25.0, 'Exterior Villa Geometry & Landscape Modeling'),
                ('Sara', 18.0, 'Lighting Setup & High-Res Texturing'),
                ('Hana', 15.0, 'Camera Angles & V-Ray Rendering Pass'),
            ]
        },
        {
            'title': 'Task 4: 3D Interior Living & Master Suite Rendering',
            'stage': '3. 3D Modeling & Rendering',
            'emps': ['Rawan', 'Mai', 'Logy', 'Marwan', 'Nouran', 'Omnia'],
            'timesheets': [
                ('Rawan', 18.0, 'Interior Furniture & Lighting Layout Review'),
                ('Mai', 15.0, 'Material Selection & Quality Control Inspection'),
                ('Logy', 22.0, 'Living Room 3D Assets & Soft Furnishings'),
                ('Marwan', 20.0, 'Master Suite Lighting & Camera Motion Design'),
                ('Nouran', 14.0, 'Bathroom & Kitchen 3D Detailed Modeling'),
                ('Omnia', 16.0, 'Post-Processing & Photoshop Color Grading'),
            ]
        },
        {
            'title': 'Task 5: AI Concept Generation & Social Media Campaign',
            'stage': '4. Digital Campaign & AI Assets',
            'emps': ['Hadeer Moustafa', 'Ahmed Nasr', 'Ahmed Youssef'],
            'timesheets': [
                ('Hadeer Moustafa', 10.0, 'Marketing Strategy & Campaign Brief Planning'),
                ('Ahmed Nasr', 15.0, 'Midjourney & AI Visual Prompts Generation'),
                ('Ahmed Youssef', 12.0, 'SEO Keyword Research & Ad Copywriting'),
            ]
        },
        {
            'title': 'Task 6: Final Review & Client Sign-Off',
            'stage': '6. Final Delivery & Sign-off',
            'emps': ['Firas', 'Marwa'],
            'timesheets': [
                ('Firas', 4.0, 'Final Presentation to Emaar Executive Board'),
                ('Marwa', 3.0, 'Delivery Documentation & Client Approval Sign-Off'),
            ]
        },
    ]

    total_hours_logged = 0.0
    for t_data in tasks_data:
        task = env['project.task'].search([('name', '=', t_data['title']), ('project_id', '=', project.id)], limit=1)
        emp_recs = [get_emp(name) for name in t_data['emps'] if get_emp(name)]
        
        if not task:
            task = env['project.task'].create({
                'name': t_data['title'],
                'project_id': project.id,
                'stage_id': stages[t_data['stage']].id,
                'user_ids': [(6, 0, [emp.user_id.id for emp in emp_recs if emp.user_id])],
            })

        # Create Timesheets
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
                total_hours_logged += hours

    print(f"5. CREATED 6 TASKS AND LOGGED {total_hours_logged} HOURS OF TIMESHEETS ACROSS ALL EMPLOYEES!")

    cr.commit()
    print("\n=======================================================")
    print("SUCCESS! COMPLETE END-TO-END DEMO CYCLE GENERATED CLEANLY!")
    print("=======================================================")
