'use strict';

const express = require('express');
const uploadController = require('../controllers/upload.controller');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');

const router = express.Router();

// ============================================================
// PUBLIC ROUTES
// ============================================================

// Public upload (customers can upload bill/photos without login)
router.post(
  '/',
  optionalAuth,
  uploadController.uploadMiddleware,
  uploadController.uploadFile,
);

// ============================================================
// PROTECTED ROUTES (admin / staff only)
// ============================================================

// List documents
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  uploadController.listDocuments,
);

// Link document to a customer (admin manual linking)
router.post(
  '/:id/link-customer',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager'),
  uploadController.linkDocumentToCustomer,
);

// Delete document
router.delete(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  uploadController.deleteDocument,
);

module.exports = router;