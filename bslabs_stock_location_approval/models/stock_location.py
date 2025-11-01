# -*- coding: utf-8 -*-
# Part of BSLabs. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class StockLocation(models.Model):
    _inherit = 'stock.location'

    require_approval = fields.Boolean(
        string='Require Approval for Outgoing',
        help='If checked, transfers from this location need approval before validation'
    )

    responsible_user_ids = fields.Many2many(
        'res.users',
        'location_responsible_user_rel',
        'location_id', 'user_id',
        string='Responsible Users',
        help='Users who can approve transfers from this location'
    )
