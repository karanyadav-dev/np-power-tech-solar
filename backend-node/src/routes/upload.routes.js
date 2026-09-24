'use strict';

const express = require('express');
const uploadController = require('../controllers/upload.controller');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');

const router = express.Router();

// Public upload (customers can upload bill/photos without login)
router.post(
  '/',
  optionalAuth,
  uploadController.uploadMiddleware,
  uploadController.uploadFile,
);

// Protected — list and delete (admin only)
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff'),
  uploadController.listDocuments,
);

router.delete(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  uploadController.deleteDocument,
);

module.exports = router;