'use strict';

const express = require('express');
const leadController = require('../controllers/lead.controller');
const { validate } = require('../middleware/validate');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createLeadSchema,
  updateLeadSchema,
  updateStatusSchema,
  assignLeadSchema,
  followupSchema,
  listLeadsQuerySchema,
} = require('../validators/lead.validator');

const router = express.Router();

// Public: create lead (from website form)
router.post(
  '/',
  optionalAuth,
  validate({ body: createLeadSchema }),
  leadController.createLead,
);

// Admin/Staff only
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ query: listLeadsQuerySchema }),
  leadController.listLeads,
);

router.get(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  leadController.getLead,
);

router.patch(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ body: updateLeadSchema }),
  leadController.updateLead,
);

router.patch(
  '/:id/status',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ body: updateStatusSchema }),
  leadController.updateStatus,
);

router.post(
  '/:id/assign',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  validate({ body: assignLeadSchema }),
  leadController.assignLead,
);

router.post(
  '/:id/followups',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ body: followupSchema }),
  leadController.addFollowup,
);

router.get(
  '/:id/followups',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  leadController.listFollowups,
);

module.exports = router;