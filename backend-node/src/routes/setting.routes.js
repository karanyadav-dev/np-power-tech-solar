'use strict';

const express = require('express');
const settingController = require('../controllers/setting.controller');
const { validate } = require('../middleware/validate');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  updateSettingsSchema,
  createSettingSchema,
} = require('../validators/setting.validator');

const router = express.Router();

// ---------- PUBLIC ----------
router.get('/public', settingController.getPublicSettings);

// ---------- PROTECTED (admin only) ----------
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin'),
  settingController.getAllSettings,
);

router.patch(
  '/bulk',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: updateSettingsSchema }),
  settingController.bulkUpdateSettings,
);

router.patch(
  '/:key',
  authenticate,
  requireRoles('super_admin', 'admin'),
  settingController.updateSetting,
);

module.exports = router;