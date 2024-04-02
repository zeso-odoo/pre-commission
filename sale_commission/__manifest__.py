{
    'name': 'Sale Commission',
    'version': '1.0',
    'summary': 'Sales Commissions rule',
    'depends':['sale','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/sales_commission_rule_view.xml',
        'views/sales_commission_view.xml',
        'views/sales_commission_menu.xml',
        
    ],
    'installable': True,
    'application':True,
    'license': 'LGPL-3',
}
