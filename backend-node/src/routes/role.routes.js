'use strict';

const express = require('express');
const roleController = require('../controllers/role.controller');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');

const router = express.Router();

router.use(authenticate);
router.use(requireRoles('super_admin', 'admin'));

router.get('/', roleController.listRoles);
router.get('/permissions', roleController.listPermissions);
router.get('/:roleName/permissions', roleController.getRolePermissions);

module.exports = router;