'use strict';

const express = require('express');
const userController = require('../controllers/user.controller');
const { validate } = require('../middleware/validate');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createUserSchema,
  updateUserSchema,
  assignRoleSchema,
  listUsersQuerySchema,
} = require('../validators/user.validator');

const router = express.Router();

// All user management requires authentication
router.use(authenticate);

// Super admin + admin only
router.use(requireRoles('super_admin', 'admin'));

router.post('/', validate({ body: createUserSchema }), userController.createUser);
router.get('/', validate({ query: listUsersQuerySchema }), userController.listUsers);
router.get('/:id', userController.getUser);
router.patch('/:id', validate({ body: updateUserSchema }), userController.updateUser);
router.delete('/:id', requireRoles('super_admin'), userController.deleteUser);

// Role assignment (super_admin only)
router.post('/:id/roles', requireRoles('super_admin'), validate({ body: assignRoleSchema }), userController.assignRole);
router.delete('/:id/roles', requireRoles('super_admin'), validate({ body: assignRoleSchema }), userController.removeRole);

module.exports = router;