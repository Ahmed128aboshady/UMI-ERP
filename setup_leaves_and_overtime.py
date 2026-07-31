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

    # 1. Leave Types Setup
    paid_leave = env['hr.leave.type'].search([('name', 'ilike', 'Paid Time Off')], limit=1)
    if not paid_leave:
        paid_leave = env['hr.leave.type'].search([('name', 'ilike', 'Paid')], limit=1)
    if not paid_leave:
        paid_leave = env['hr.leave.type'].create({
            'name': 'Paid Time Off (إجازة سنوية مدفوعة)',
            'requires_allocation': 'yes',
            'employee_requests': 'yes',
        })
    print(f"PAID LEAVE TYPE: {paid_leave.name} (ID: {paid_leave.id})")

    sick_leave = env['hr.leave.type'].search([('name', 'ilike', 'Sick')], limit=1)
    if not sick_leave:
        sick_leave = env['hr.leave.type'].create({
            'name': 'Sick Time Off (إجازة مرضية)',
            'requires_allocation': 'no',
            'employee_requests': 'yes',
        })
    print(f"SICK LEAVE TYPE: {sick_leave.name} (ID: {sick_leave.id})")

    overtime_leave = env['hr.leave.type'].search([('name', 'ilike', 'Compensatory')], limit=1)
    if not overtime_leave:
        overtime_leave = env['hr.leave.type'].create({
            'name': 'Overtime & Compensatory Days (أوفرتايم وأيام تعويضية)',
            'requires_allocation': 'yes',
            'employee_requests': 'yes',
        })
    print(f"OVERTIME LEAVE TYPE: {overtime_leave.name} (ID: {overtime_leave.id})")

    # 2. Allocate 21 Days Annual Paid Leave for All 20 Employees and Approve
    employees = env['hr.employee'].search([('name', '!=', 'Administrator')])
    for emp in employees:
        alloc = env['hr.leave.allocation'].search([('employee_id', '=', emp.id), ('holiday_status_id', '=', paid_leave.id)], limit=1)
        if not alloc:
            alloc = env['hr.leave.allocation'].create({
                'name': f'Annual Paid Leave 2026 - {emp.name}',
                'employee_id': emp.id,
                'holiday_status_id': paid_leave.id,
                'number_of_days': 21.0,
            })
        
        # Approve allocation
        if alloc.state != 'validate':
            try:
                alloc.action_validate()
            except Exception as e:
                try:
                    alloc.action_approve()
                except:
                    pass
        print(f"ALLOCATED & APPROVED 21 PAID LEAVE DAYS FOR {emp.name}")

    cr.commit()
    print("SUCCESSFULLY APPROVED 21 DAYS ANNUAL LEAVE ALLOCATION FOR ALL 20 EMPLOYEES!")
