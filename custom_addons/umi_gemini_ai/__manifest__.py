{
    'name': 'UMI Gemini AI Copilot',
    'version': '19.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'Smart Gemini AI Copilot connected directly to UMI ERP Database',
    'description': """
        UMI Gemini AI Copilot Integration
        ==================================
        Connects Google Gemini AI directly to Odoo 19 Database to provide intelligent
        insights on Sales, Projects, Tasks, Employee Performance, Timesheets, and Product Strategy.
    """,
    'author': 'UMI ERP Team',
    'depends': ['base', 'web', 'sale', 'project', 'hr', 'hr_timesheet', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/gemini_ai_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
