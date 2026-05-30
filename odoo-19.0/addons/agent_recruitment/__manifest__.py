{
    'name': 'Agent Recruitment',
    'version': '1.0',
    'summary': 'Agentlarni ishga qabul qilish uchun web sahifa va forma',
    'description': 'Agentlarni ishga qabul qilish uchun maxsus modul. Website forma va admin panelni o\'z ichiga oladi.',
    'category': 'Website',
    'author': 'Antigravity',
    'depends': ['website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/agent_application_views.xml',
        'views/website_agent_registration_template.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'agent_recruitment/static/src/css/style.css',
            'agent_recruitment/static/src/js/validation.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
