'use strict';

const express = require('express');
const path = require('path');
const fs = require('fs');
const quotationController = require('../controllers/quotation.controller');
const { validate } = require('../middleware/validate');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createQuotationRequestSchema,
  requestInfoSchema,
  configurePricingSchema,
  approveQuotationSchema,
  updateBankDetailsSchema,
  customerResponseSchema,
  listQuotationsQuerySchema,
} = require('../validators/quotation.validator');

const router = express.Router();

// ============================================================
// PUBLIC ROUTES
// ============================================================

router.post(
  '/',
  optionalAuth,
  validate({ body: createQuotationRequestSchema }),
  quotationController.createRequest,
);

router.get(
  '/:id/view',
  quotationController.markViewed,
);

router.post(
  '/:id/respond',
  validate({ body: customerResponseSchema }),
  quotationController.customerResponse,
);

// ---------- PUBLIC PDF download ----------
router.get('/:id/pdf/download', async (req, res) => {
  try {
    const db = require('../config/db');
    const result = await db.query(
      `SELECT pdf_url FROM quotations WHERE id = $1`,
      [req.params.id],
    );

    if (result.rowCount === 0 || !result.rows[0].pdf_url) {
      return res.status(404).json({
        success: false,
        error: { code: 'PDF_NOT_FOUND', message: 'PDF not generated yet' },
      });
    }

    const pdfUrl = result.rows[0].pdf_url;
    const relativePath = pdfUrl.replace(/^\/uploads\//, '');
    const filePath = path.join(__dirname, '..', '..', '..', 'storage', 'uploads', relativePath);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({
        success: false,
        error: { code: 'FILE_NOT_FOUND', message: 'PDF file missing' },
      });
    }

    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `inline; filename="${path.basename(filePath)}"`);
    fs.createReadStream(filePath).pipe(res);
  } catch (err) {
    res.status(500).json({
      success: false,
      error: { code: 'PDF_ERROR', message: err.message },
    });
  }
});

// ============================================================
// PROTECTED ROUTES
// ============================================================

router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  validate({ query: listQuotationsQuerySchema }),
  quotationController.listQuotations,
);

router.get(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  quotationController.getQuotation,
);

router.post(
  '/:id/review',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.startReview,
);

router.post(
  '/:id/request-info',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  validate({ body: requestInfoSchema }),
  quotationController.requestInfo,
);

router.post(
  '/:id/verify',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.verifyInfo,
);

router.post(
  '/:id/pricing',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: configurePricingSchema }),
  quotationController.configurePricing,
);

router.post(
  '/:id/approve',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: approveQuotationSchema.optional() }),
  quotationController.approveQuotation,
);

router.post(
  '/:id/pdf-generated',
  authenticate,
  requireRoles('super_admin', 'admin'),
  quotationController.markPdfGenerated,
);

// Generate actual PDF file
router.post(
  '/:id/generate-pdf',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.generatePdf,
);

router.post(
  '/:id/send',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  quotationController.sendToCustomer,
);

// Update bank details for a quotation
router.patch(
  '/:id/bank',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  validate({ body: updateBankDetailsSchema }),
  quotationController.updateBankDetails,
);

module.exports = router;