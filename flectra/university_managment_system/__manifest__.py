{
'name': 'CMS ERISP',
'description': 'University Managment System',
'author': 'ERISP.PVT.LTD',
'application': True,
'depends': ['mail'],
'data': [
        'security/cms_access_rule.xml',
         'security/ir.model.access.csv',
         'views/view.xml',
         'views/degree_view.xml',
        'views/degree_report.xml',
         'menus/main_menu.xml',
         'views/cms_transcript.xml'
         ] 
}