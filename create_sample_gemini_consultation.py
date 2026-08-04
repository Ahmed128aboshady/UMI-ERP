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

    copilot = env['umi.gemini.ai.copilot'].create({
        'name': 'التحليل الشامل والاستشارة الذكية لنظام UMI ERP',
        'prompt': 'حلل لي أداء الشركة بالكامل في المبيعات والمشاريع وكفاءة الموظفين واعطني توصيات تسويقية',
    })
    copilot.action_ask_gemini()

    cr.commit()
    print("CREATED & EXECUTED INITIAL GEMINI AI CONSULTATION!")
