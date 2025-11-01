# -*- coding: utf-8 -*-
# Part of BSLabs. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    approval_state = fields.Selection([
        ('no_approval', 'No Approval Required'),
        ('pending', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Approval State', default='no_approval', tracking=True)

    approval_required = fields.Boolean(
        string='Approval Required',
        compute='_compute_approval_required',
        store=True
    )

    approver_ids = fields.Many2many(
        'res.users',
        string='Approvers',
        compute='_compute_approver_ids',
        store=True
    )

    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    approved_date = fields.Datetime(string='Approval Date', readonly=True)

    can_approve = fields.Boolean(
        string='Can Approve',
        compute='_compute_can_approve',
        help='Whether current user can approve/reject this transfer'
    )

    @api.depends('location_id', 'location_id.require_approval', 'picking_type_code', 'state')
    def _compute_approval_required(self):
        """
        Compute if approval is required for this transfer.

        Approval is ONLY required when:
        1. Location has require_approval enabled
        2. Transfer type is outgoing or internal
        3. Transfer is in 'waiting' OR 'assigned' state (after clicking "Mark as Todo")
           - 'waiting' = products not reserved yet
           - 'assigned' = products reserved and ready (the "Ready" status)

        Draft transfers are ignored. Completed/cancelled transfers reset to no_approval.
        This prevents retroactive application to old transfers.
        """
        for picking in self:
            # Check approval when in 'waiting' or 'assigned' state (after "Mark as Todo")
            # 'assigned' is the "Ready" state that appears after availability check
            if (picking.location_id.require_approval and
                picking.picking_type_code in ['outgoing', 'internal'] and
                picking.state in ['waiting', 'assigned']):  # Waiting OR Ready state

                picking.approval_required = True

                # Set to pending and notify if transitioning from no_approval
                if picking.approval_state == 'no_approval' and picking.approver_ids:
                    picking.approval_state = 'pending'
                    # Only notify if not in install/upgrade mode
                    if not self.env.context.get('install_mode'):
                        picking._notify_approvers_needed()
            else:
                picking.approval_required = False
                # Reset approval state for draft/done/cancelled transfers
                if picking.state in ['draft', 'done', 'cancel']:
                    picking.approval_state = 'no_approval'

    @api.depends('location_id', 'location_id.responsible_user_ids')
    def _compute_approver_ids(self):
        for picking in self:
            if picking.location_id.require_approval:
                picking.approver_ids = picking.location_id.responsible_user_ids
            else:
                picking.approver_ids = False

    @api.depends('approver_ids')
    def _compute_can_approve(self):
        """Check if current user is in the approver list"""
        for picking in self:
            picking.can_approve = self.env.user in picking.approver_ids

    def button_validate(self):
        # Override validation to check approval
        for picking in self:
            if picking.approval_required and picking.approval_state != 'approved':
                raise UserError(_(
                    'This transfer requires approval from: %s\n'
                    'Current state: %s'
                ) % (
                    ', '.join(picking.approver_ids.mapped('name')) or 'No approver assigned',
                    dict(picking._fields['approval_state'].selection)[picking.approval_state]
                ))
        return super(StockPicking, self).button_validate()

    def action_approve(self):
        """Approve the transfer"""
        for picking in self:
            if self.env.user not in picking.approver_ids:
                raise UserError(_('You are not authorized to approve this transfer.'))

            picking.write({
                'approval_state': 'approved',
                'approved_by': self.env.user.id,
                'approved_date': fields.Datetime.now(),
            })

            # Mark any pending approval activities as done
            picking.activity_feedback(
                ['bslabs_stock_location_approval.mail_activity_data_approval_needed']
            )

            # Send notification
            picking.message_post(
                body=_('✓ Transfer approved by %s') % self.env.user.name,
                subject=_('Transfer Approved'),
                subtype_xmlid='mail.mt_comment',
            )
        return True

    def action_reject(self):
        """Reject the transfer"""
        for picking in self:
            if self.env.user not in picking.approver_ids:
                raise UserError(_('You are not authorized to reject this transfer.'))

            picking.write({
                'approval_state': 'rejected',
            })

            # Mark any pending approval activities as done
            picking.activity_feedback(
                ['bslabs_stock_location_approval.mail_activity_data_approval_needed']
            )

            # Send notification
            picking.message_post(
                body=_('✗ Transfer rejected by %s') % self.env.user.name,
                subject=_('Transfer Rejected'),
                subtype_xmlid='mail.mt_comment',
            )
        return True

    def _notify_approvers_needed(self):
        """Send notification to approvers that a transfer needs approval"""
        for picking in self:
            if not picking.approver_ids:
                continue

            # Create activity for each approver
            picking.activity_schedule(
                'bslabs_stock_location_approval.mail_activity_data_approval_needed',
                user_id=picking.approver_ids[0].id,  # Assign to first approver
                summary=_('Stock Transfer Approval Required'),
                note=_(
                    'Transfer %s from %s to %s requires your approval.<br/>'
                    'Source Location: <strong>%s</strong><br/>'
                    'Destination: <strong>%s</strong><br/>'
                    'Scheduled Date: %s'
                ) % (
                    picking.name,
                    picking.location_id.name,
                    picking.location_dest_id.name,
                    picking.location_id.complete_name,
                    picking.location_dest_id.complete_name,
                    picking.scheduled_date or _('Not set')
                )
            )

            # Also send a message in the chatter mentioning all approvers
            approver_names = ', '.join(['@' + user.name for user in picking.approver_ids])
            picking.message_post(
                body=_(
                    'This transfer requires approval from: %s<br/>'
                    'Please review and approve or reject this transfer.'
                ) % approver_names,
                subject=_('Approval Required'),
                partner_ids=picking.approver_ids.mapped('partner_id').ids,
                subtype_xmlid='mail.mt_comment',
            )
