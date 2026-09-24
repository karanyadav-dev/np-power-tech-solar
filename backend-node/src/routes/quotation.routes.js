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
// PUBLIC ROUTES
// ============================================================

router.post('/', optionalAuth, validate({ body: createQuotationRequestSchema }), quotationController.createRequest);

router.get('/:id/view', quotationController.markViewed);

router.post('/:id/respond', validate({ body: customerResponseSchema }), quotationController.customerResponse);

// ============================================================
// PROTECTED ROUTES
// ============================================================

router.get('/', authenticate, requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'), validate({ query: listQuotationsQuerySchema }), quotationController.listQuotations);

router.get('/:id', authenticate, requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'), quotationController.getQuotation);

router.post('/:id/review', authenticate, requireRoles('super_admin', 'admin', 'sales_manager'), quotationController.startReview);

router.post('/:id/request-info', authenticate, requireRoles('super_admin', 'admin', 'sales_manager'), validate({ body: requestInfoSchema }), quotationController.requestInfo);

router.post('/:id/verify', authenticate, requireRoles('super_admin', 'admin', 'sales_manager'), quotationController.verifyInfo);

router.post('/:id/pricing', authenticate, requireRoles('super_admin', 'admin'), validate({ body: configurePricingSchema }), quotationController.configurePricing);

router.post('/:id/approve', authenticate, requireRoles('super_admin', 'admin'), validate({ body: approveQuotationSchema.optional() }), quotationController.approveQuotation);

router.post('/:id/pdf-generated', authenticate, requireRoles('super_admin', 'admin'), quotationController.markPdfGenerated);

router.post('/:id/generate-pdf', authenticate, requireRoles('super_admin', 'admin', 'sales_manager'), quotationController.generatePdf);

router.post('/:id/send', authenticate, requireRoles('super_admin', 'admin', 'sales_manager'), quotationController.sendToCustomer);

module.exports = router;