# -*- coding: utf-8 -*-
# Part of BSLabs. See LICENSE file for full copyright and licensing details.

{
    'name': 'BSLabs Stock Location Approval',
    'version': '16.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Require approval for transfers from restricted locations',
    'description': """
BSLabs Stock Location Approval
================================

Universal stock transfer approval system for any restricted location.

Features
--------
* Mark any location as requiring approval for outgoing transfers
* Assign responsible users who can approve transfers
* Block transfer validation until approval is granted
* Track approval history with full audit trail
* Dashboard filters for pending approvals
* Works for pharmacies, warehouses, restricted areas, etc.

Use Cases
---------
* Pharmacy dispensing control
* High-value inventory transfers
* Restricted warehouse section management
* Quality control checkpoints
* Multi-level warehouse authorization
    """,
    'author': 'Bilal Benmerzoug',
    'website': 'https://adoctor.org',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/mail_activity_type_data.xml',
        'views/stock_location_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
