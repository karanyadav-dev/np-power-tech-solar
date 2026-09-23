'use strict';

const express = require('express');
const customerController = require('../controllers/customer.controller');
const { validate } = require('../middleware/validate');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createCustomerSchema,
  updateCustomerSchema,
  listCustomersQuerySchema,
} = require('../validators/customer.validator');

const router = express.Router();

// All customer routes require authentication
router.use(authenticate);
router.use(requireRoles('super_admin', 'admin', 'sales_manager', 'sales_staff', 'accountant', 'support_staff'));

router.post('/', validate({ body: createCustomerSchema }), customerController.createCustomer);
router.get('/', validate({ query: listCustomersQuerySchema }), customerController.listCustomers);
router.get('/:id', customerController.getCustomer);
router.patch('/:id', validate({ body: updateCustomerSchema }), customerController.updateCustomer);
router.delete('/:id', requireRoles('super_admin', 'admin'), customerController.deleteCustomer);

module.exports = router;