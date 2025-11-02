# Stock Location Approval

[![License: LGPL-3](https://img.shields.io/badge/license-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo Version](https://img.shields.io/badge/Odoo-16.0-purple.svg)](https://www.odoo.com/)

## Universal Stock Transfer Approval System

A flexible and powerful approval workflow for stock transfers from restricted locations. Perfect for pharmacies, controlled warehouses, high-value inventory, and any scenario requiring authorization before stock movement.

---

## 🎯 Key Features

### ✅ Location-Based Approval Control
- Mark any stock location as requiring approval for outgoing transfers
- Works with internal transfers and outgoing shipments
- No modification to standard Odoo workflows

### 👥 Multi-User Assignment
- Assign multiple responsible users per location
- Any assigned user can approve transfers
- Flexible authorization management

### 🔔 Automatic Notifications
- **Activity notifications** in user dashboard
- **Email alerts** to all responsible users
- **Chatter messages** with @mentions
- Real-time approval requests

### 🚫 Validation Blocking
- Prevents transfer validation until approval is granted
- Clear error messages indicating who needs to approve
- Current approval status always visible

### 📊 Smart UI
- **Smart button status** indicators (no statusbar clutter)
- **Badge indicators** in list view (color-coded, hidden when not needed)
- **Approve/Reject buttons** only visible to authorized users
- **Dedicated Approval tab** with full details
- **Dashboard filters** for quick access
- Clean, uncluttered interface following Odoo standards

### 🌍 Multi-Language Support
- **English** - Full support
- **French** - Complete translation
- Easy to add more languages

### 📈 Full Audit Trail
- Track who approved/rejected each transfer
- Timestamp for all approval actions
- Complete history in chatter
- Activity completion records

---

---

## 🚀 Installation

1. **Download the module:**
   ```bash
   cd /path/to/odoo/addons
   git clone [repository-url] bslabs_stock_location_approval
   ```

2. **Restart Odoo:**
   ```bash
   sudo service odoo restart
   ```

3. **Update Apps List:**
   - Go to Apps menu
   - Click "Update Apps List"
   - Search for "Stock Location Approval"

4. **Install:**
   - Click "Install" button

---

## ⚙️ Configuration

### Step 1: Configure Locations

1. Navigate to: **Inventory > Configuration > Locations**
2. Open the location you want to restrict (e.g., Pharmacy, Warehouse)
3. In the **"Additional Information"** section:
   - ☑️ Check **"Require Approval for Outgoing"**
   - Select **"Responsible Users"** (one or more users)
4. Click **Save**

![Configuration Steps](static/description/config_steps.png)

### Step 2: That's It!

The approval workflow is now active for that location. Any transfer FROM this location will automatically:
- Enter "Pending Approval" state
- Notify responsible users
- Block validation until approved

---

## 👤 Usage Guide

### For Transfer Creators

1. **Create a transfer** from a restricted location (normal process)
2. System automatically detects approval requirement
3. Transfer shows **"Waiting Approval"** status in smart button
4. Cannot validate until approved
5. Monitor status in the **"Approval"** tab

### For Approvers

#### You Will Receive:
- ✉️ **Activity** in your dashboard
- 📧 **Email notification** (if configured)
- 💬 **Chatter message** with @mention

#### To Approve:
1. Go to: **Inventory > Operations > Transfers**
2. Use filter: **"My Approvals"**
3. Open the transfer
4. Review details in **"Approval"** tab
5. Click **"Approve"** or **"Reject"** button in the header

### After Approval

- ✅ Smart button changes to green **"Approved"** status
- ✅ Activity automatically closed
- ✅ Validation button becomes available
- ✅ Approval logged in chatter with timestamp
- ✅ Records who approved and when

### If Rejected

- ❌ Smart button changes to red **"Rejected"** status
- ❌ Validation remains blocked
- ❌ Rejection logged in chatter
- ❌ Creator notified of rejection

---

## 🎨 UI Elements

### Location Form
- **Checkbox:** "Require Approval for Outgoing"
- **Tags Field:** "Responsible Users" (appears when enabled)
- **Location:** In "Additional Information" group (properly aligned)

### Transfer Form - Header
- **Approve Button:** Green (visible to approvers when pending)
- **Reject Button:** Gray (visible to approvers when pending)
- **Standard Status Bar:** Draft → Waiting → Ready → Done (unchanged)

### Transfer Form - Button Box (Smart Buttons)
Clean status indicators (one visible at a time):
- **🕐 Waiting Approval:** Yellow, shown when pending
- **✓ Approved:** Green, shown when approved
- **✗ Rejected:** Red, shown when rejected
- **Note:** No clutter in status bar - status shows as smart button instead

### Transfer Form - Approval Tab
- **Approval Required:** Yes/No indicator
- **Approvers:** List of authorized users
- **Approved By:** Who approved (after approval)
- **Approval Date:** When approved (after approval)

### Transfer List View
- **Approval Column:** Badge with color coding (hidden when not applicable):
  - 🟡 **Yellow:** Pending
  - 🟢 **Green:** Approved
  - 🔴 **Red:** Rejected
  - **(empty):** No approval needed (column hidden)

### Search Filters
- **"Pending Approval":** All transfers waiting for approval
- **"My Approvals":** Transfers you can approve

---

## 🔒 Security & Permissions

### Access Rights
- Uses standard Odoo stock groups:
  - `stock.group_stock_user` - Can create transfers, view approval status
  - `stock.group_stock_manager` - Full access

### Approval Authorization
- Even with user group access, only users in the "Responsible Users" list can approve/reject
- System validates authorization in code (not just UI)
- Prevents unauthorized approvals via API calls

### Audit Security
- All approvals/rejections logged with user and timestamp
- Cannot modify approval history
- Complete trail for compliance

---

## 📋 Use Cases

### 🏥 Healthcare - Pharmacy Control
**Scenario:** Prevent medication dispensing without pharmacist approval
```
Location: Pharmacy Stock
Responsible Users: Head Pharmacist, Duty Pharmacist
Result: All medication transfers require pharmacist authorization
```

### 💎 High-Value Inventory
**Scenario:** Authorize expensive item transfers
```
Location: Precious Metals Vault
Responsible Users: Warehouse Manager, Security Officer
Result: No expensive items leave without management approval
```

### 🏭 Manufacturing - Quality Control
**Scenario:** Quality checkpoint before shipment
```
Location: Quality Control Zone
Responsible Users: QC Inspector, QC Manager
Result: Products only ship after QC approval
```

### 🏢 Multi-Warehouse - Internal Transfers
**Scenario:** Control transfers between warehouse sections
```
Location: Restricted Area A
Responsible Users: Section Supervisor, Warehouse Manager
Result: Internal movements require supervisor approval
```

### 🔬 Laboratory - Controlled Substances
**Scenario:** Track and authorize controlled substance usage
```
Location: Controlled Substances Cabinet
Responsible Users: Lab Manager, Safety Officer
Result: All removals require authorized approval
```

---

## 🔧 Technical Details

### Module Information
- **Name:** `bslabs_stock_location_approval`
- **Version:** 16.0.1.0.0
- **Category:** Inventory/Inventory
- **Dependencies:** `stock`, `mail`
- **License:** LGPL-3

### Architecture
- **Non-intrusive:** Doesn't modify core Odoo workflows
- **Parallel states:** Approval states run alongside standard picking states (see DESIGN_DECISIONS.md)
- **Event-driven:** Notifications triggered automatically on state changes
- **Clean UI:** Smart buttons instead of statusbar clutter
- **Extensible:** Easy to customize or extend

### Data Models Extended
- `stock.location` - Added approval configuration
- `stock.picking` - Added approval workflow

### New Fields

#### On `stock.location`:
- `require_approval` (Boolean)
- `responsible_user_ids` (Many2many to res.users)

#### On `stock.picking`:
- `approval_state` (Selection: no_approval/pending/approved/rejected)
- `approval_required` (Boolean, computed)
- `approver_ids` (Many2many, computed from location)
- `approved_by` (Many2one to res.users)
- `approved_date` (Datetime)
- `can_approve` (Boolean, computed for current user)

---

## 🌐 Translations

Current translations:
- 🇬🇧 **English** - Default
- 🇫🇷 **French** - Complete

To add more languages:
1. Go to: Settings > Translations > Export Translation
2. Select module: `bslabs_stock_location_approval`
3. Select language and export
4. Translate the PO file
5. Import back into Odoo

---

## 📚 Documentation

- **Installation Guide:** See Installation section above
- **User Manual:** See Usage Guide section above
- **Configuration:** See Configuration section above
Why separate approval_state vs modifying standard state

---

## 🆘 Support

### Getting Help
- 📧 Email: support@adoctor.org
- 🌐 Website: https://adoctor.org
- 📖 Documentation: [Module Wiki](https://github.com/[repo]/wiki)

### Reporting Issues
1. Check existing issues on GitHub
2. Provide clear steps to reproduce
3. Include Odoo version and module version
4. Attach relevant logs if applicable

### Feature Requests
We welcome suggestions! Please open an issue with:
- Clear description of the feature
- Use case / business need
- Expected behavior

---

## 🔮 Roadmap

Planned future enhancements:
- [ ] Fixing Bugs if they rais
- [ ] Make it compatible with odoo 17, 18, 19

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines
- Follow Odoo coding standards
- Add translations for new strings
- Update documentation
- Test with multiple Odoo versions if possible

---

## 📄 License

This module is licensed under LGPL-3.

Copyright (C) 2024 Bilal Benmerzoug

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

---

## 👨‍💻 Author

**Serenvale**
- Website: https://adoctor.org
- GitHub: [\[Your GitHub Profile\]](https://github.com/xmoroix)

---

## 🙏 Acknowledgments

- Odoo Community Association (OCA) for best practices
- Contributors and testers
- Users providing feedback and feature requests

---

## 📊 Statistics

- **Lines of Code:** ~300
- **Files:** 12
- **Translations:** 2 languages (50+ strings)
- **Models Extended:** 2
- **Views Created:** 5
- **Security Groups:** 2

---

## ⚡ Quick Start Checklist

- [ ] Install the module
- [ ] Configure at least one restricted location
- [ ] Assign responsible users
- [ ] Create a test transfer
- [ ] Verify notifications work
- [ ] Test approval workflow
- [ ] Check activity dashboard
- [ ] Review chatter messages
- [ ] Test rejection workflow
- [ ] Verify validation blocking

---

**Ready to improve your inventory control?** Install now and start managing approvals efficiently! 🚀

