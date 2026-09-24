'use strict';

const express = require('express');
const quotationController = require('../controllers/quotation.controller');
const { validate } = require('../middleware/validate');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createQuotationRequestSchema,
  requestInfoSchema,
  configurePricingSchema,
  approveQuotationSchema,
  customerResponseSchema,
  listQuotationsQuerySchema,
} = require('../validators/quotation.validator');

const router = express.Router();

// ============================================================
// PUBLIC ROUTES (customer-facing)
// ============================================================

// Submit quotation request (public — no auth needed)
router.post(
  '/',
  optionalAuth,
  validate({ body: createQuotationRequestSchema }),
  quotationController.createRequest,
);

// Customer: view their quotation (via public link with ID)
router.get(
  '/:id/view',
  quotationController.markViewed,
);

// Customer: accept/reject quotation (via public link)
router.post(
  '/:id/respond',
  validate({ body: customerResponseSchema }),
  quotationController.customerResponse,
);

// ============================================================
// PROTECTED ROUTES (admin/staff)
// ============================================================

// List quotations (admin/sales only)
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ query: listQuotationsQuerySchema }),
  quotationController.listQuotations,
);

// Get single quotation
router.get(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  quotationController.getQuotation,
);

// Admin workflow: Start review
router.post(
  '/:id/review',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.startReview,
);

// Admin workflow: Request additional info
router.post(
  '/:id/request-info',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  validate({ body: requestInfoSchema }),
  quotationController.requestInfo,
);

// Admin workflow: Verify information
router.post(
  '/:id/verify',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.verifyInfo,
);

// Admin workflow: Configure pricing
router.post(
  '/:id/pricing',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: configurePricingSchema }),
  quotationController.configurePricing,
);

// Admin workflow: Approve quotation
router.post(
  '/:id/approve',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: approveQuotationSchema.optional() }),
  quotationController.approveQuotation,
);

// Admin workflow: Mark PDF generated
router.post(
  '/:id/pdf-generated',
  authenticate,
  requireRoles('super_admin', 'admin'),
  quotationController.markPdfGenerated,
);

// Admin workflow: Send to customer
router.post(
  '/:id/send',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.sendToCustomer,
);

module.exports = router;