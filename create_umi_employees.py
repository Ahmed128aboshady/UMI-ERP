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

    # Fetch Companies
    uae_company = env['res.company'].search([('name', 'ilike', 'UMI General Trading')], limit=1)
    egypt_company = env['res.company'].search([('name', 'ilike', 'UMI Egypt')], limit=1)

    # 1. Departments Creation
    dept_names = ['Executive Board', 'Human Resources', 'Marketing', '2D Design', '3D Design', 'Operations']
    departments = {}
    for name in dept_names:
        dept = env['hr.department'].search([('name', '=', name)], limit=1)
        if not dept:
            dept = env['hr.department'].create({'name': name})
        departments[name] = dept.id
    print("DEPARTMENTS CREATED/FOUND:", list(departments.keys()))

    # 2. Job Positions Creation
    jobs_data = [
        ('Co-Founder & CEO', departments['Executive Board']),
        ('HR & Egypt Office Manager', departments['Human Resources']),
        ('HR Manager - Dubai', departments['Human Resources']),
        ('Marketing Manager', departments['Marketing']),
        ('SEO & Digital Marketing Specialist', departments['Marketing']),
        ('AI Designer', departments['Marketing']),
        ('2D Graphic Designer', departments['2D Design']),
        ('3D Design Team Leader', departments['3D Design']),
        ('3D Designer', departments['3D Design']),
        ('Operations Specialist', departments['Operations']),
    ]
    jobs = {}
    for title, dept_id in jobs_data:
        job = env['hr.job'].search([('name', '=', title)], limit=1)
        if not job:
            job = env['hr.job'].create({'name': title, 'department_id': dept_id})
        jobs[title] = job.id
    print("JOB POSITIONS CREATED/FOUND:", list(jobs.keys()))

    # 3. Employee List Data
    employee_list = [
        # Executive
        {
            'name': 'Firas',
            'job': 'Co-Founder & CEO',
            'dept': 'Executive Board',
            'company': uae_company.id,
            'email': 'firas@umi.com',
        },
        # HR
        {
            'name': 'Marwa',
            'job': 'HR & Egypt Office Manager',
            'dept': 'Human Resources',
            'company': egypt_company.id,
            'email': 'marwa@umi.com',
        },
        {
            'name': 'Aya Salah',
            'job': 'HR Manager - Dubai',
            'dept': 'Human Resources',
            'company': uae_company.id,
            'email': 'aya.salah@umi.com',
        },
        # Marketing
        {
            'name': 'Hadeer Moustafa',
            'job': 'Marketing Manager',
            'dept': 'Marketing',
            'company': egypt_company.id,
            'email': 'hadeer.moustafa@umi.com',
        },
        {
            'name': 'Ahmed Nasr',
            'job': 'AI Designer',
            'dept': 'Marketing',
            'company': egypt_company.id,
            'email': 'ahmed.nasr@umi.com',
        },
        {
            'name': 'Ahmed Youssef',
            'job': 'SEO & Digital Marketing Specialist',
            'dept': 'Marketing',
            'company': egypt_company.id,
            'email': 'ahmed.youssef@umi.com',
        },
        # 2D Graphic Design
        {
            'name': 'Yara Khamis',
            'job': '2D Graphic Designer',
            'dept': '2D Design',
            'company': egypt_company.id,
            'email': 'yara.khamis@umi.com',
        },
        {
            'name': 'Saeed Ali',
            'job': '2D Graphic Designer',
            'dept': '2D Design',
            'company': egypt_company.id,
            'email': 'saeed.ali@umi.com',
        },
        {
            'name': 'Mohamed Abdelnabi',
            'job': '2D Graphic Designer',
            'dept': '2D Design',
            'company': egypt_company.id,
            'email': 'mohamed.abdelnabi@umi.com',
        },
        # 3D Design Leaders
        {
            'name': 'Mohamed Mahmoud',
            'job': '3D Design Team Leader',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'mohamed.mahmoud@umi.com',
        },
        {
            'name': 'Rawan',
            'job': '3D Design Team Leader',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'rawan@umi.com',
        },
        {
            'name': 'Mai',
            'job': '3D Design Team Leader',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'mai@umi.com',
        },
        # 3D Designers
        {
            'name': 'Dina',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'dina@umi.com',
        },
        {
            'name': 'Sara',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'sara@umi.com',
        },
        {
            'name': 'Hana',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'hana@umi.com',
        },
        {
            'name': 'Logy',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'logy@umi.com',
        },
        {
            'name': 'Marwan',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'marwan@umi.com',
        },
        {
            'name': 'Nouran',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'nouran@umi.com',
        },
        {
            'name': 'Omnia',
            'job': '3D Designer',
            'dept': '3D Design',
            'company': egypt_company.id,
            'email': 'omnia@umi.com',
        },
        # Operations
        {
            'name': 'Geleen',
            'job': 'Operations Specialist',
            'dept': 'Operations',
            'company': uae_company.id,
            'email': 'geleen@umi.com',
        },
    ]

    created_count = 0
    updated_count = 0
    for emp_data in employee_list:
        emp = env['hr.employee'].search([('name', '=', emp_data['name'])], limit=1)
        vals = {
            'name': emp_data['name'],
            'job_id': jobs[emp_data['job']],
            'department_id': departments[emp_data['dept']],
            'company_id': emp_data['company'],
            'work_email': emp_data['email'],
        }
        if not emp:
            env['hr.employee'].create(vals)
            created_count += 1
        else:
            emp.write(vals)
            updated_count += 1

    cr.commit()
    print(f"SUCCESS! CREATED {created_count} NEW EMPLOYEES AND UPDATED {updated_count} EXISTING EMPLOYEES.")
