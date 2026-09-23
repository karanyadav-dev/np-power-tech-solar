'use strict';

const express = require('express');
const productController = require('../controllers/product.controller');
const { validate } = require('../middleware/validate');
const { authenticate, optionalAuth } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createProductSchema,
  updateProductSchema,
  createCategorySchema,
  listProductsQuerySchema,
} = require('../validators/product.validator');

const router = express.Router();

// ---------- Categories (public read) ----------
router.get('/categories', productController.listCategories);
router.post(
  '/categories',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: createCategorySchema }),
  productController.createCategory,
);

// ---------- Products ----------
// Public: list & view
router.get('/', validate({ query: listProductsQuerySchema }), productController.listProducts);
router.get('/slug/:slug', productController.getProductBySlug);
router.get('/:id', productController.getProduct);

// Admin only: create, update, delete
router.post(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: createProductSchema }),
  productController.createProduct,
);

router.patch(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  validate({ body: updateProductSchema }),
  productController.updateProduct,
);

router.delete(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  productController.deleteProduct,
);

module.exports = router;