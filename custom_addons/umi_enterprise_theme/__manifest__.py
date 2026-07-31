{
    'name': 'UMI Enterprise Theme',
    'version': '19.0.1.0.0',
    'category': 'Theme/Backend',
    'summary': 'Enterprise App Switcher & Modern Grid Theme for UMI ERP',
    'author': 'UMI ERP',
    'license': 'LGPL-3',
    'depends': ['web'],
    'data': [
        'views/theme_actions.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'umi_enterprise_theme/static/src/scss/enterprise_theme.scss',
            'umi_enterprise_theme/static/src/js/enterprise_home.js',
            'umi_enterprise_theme/static/src/xml/navbar.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
}
