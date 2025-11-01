#!/usr/bin/env python3
"""
Script to fix existing stock transfers that were incorrectly set to pending approval.
This should be run ONCE after upgrading the module to clean up the data.

Usage:
    docker compose exec odoo python3 /mnt/extra-addons/bslabs_stock_location_approval/fix_existing_transfers.py
"""

import sys
import os

# Add Odoo to path
sys.path.insert(0, '/usr/lib/python3/dist-packages')

import odoo
from odoo import api, SUPERUSER_ID

def fix_transfers():
    """Fix all transfers that were incorrectly marked as pending approval"""

    db_name = os.environ.get('ODOO_DB_NAME', 'odoo')

    # Connect to database
    registry = odoo.registry(db_name)

    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Find all pickings with approval_state = 'pending' that are done or cancelled
        bad_pickings = env['stock.picking'].search([
            ('approval_state', '=', 'pending'),
            ('state', 'in', ['done', 'cancel'])
        ])

        print(f"Found {len(bad_pickings)} completed transfers incorrectly marked as pending")

        if bad_pickings:
            # Reset their approval state
            bad_pickings.write({
                'approval_state': 'no_approval',
                'approval_required': False
            })
            print(f"✓ Fixed {len(bad_pickings)} transfers")

            # Delete any activities created for these transfers
            activities = env['mail.activity'].search([
                ('res_model', '=', 'stock.picking'),
                ('res_id', 'in', bad_pickings.ids),
                ('activity_type_id', '=', env.ref('bslabs_stock_location_approval.mail_activity_data_approval_needed').id)
            ])

            if activities:
                activities.unlink()
                print(f"✓ Deleted {len(activities)} incorrect activities")

        # Commit changes
        cr.commit()
        print("\n✓ All existing transfers have been fixed!")
        print("The module will now only require approval for NEW transfers from restricted locations.")

if __name__ == '__main__':
    fix_transfers()
