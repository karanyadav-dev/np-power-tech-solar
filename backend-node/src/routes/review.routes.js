'use strict';

const express = require('express');
const reviewController = require('../controllers/review.controller');
const { validate } = require('../middleware/validate');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createReviewSchema,
  updateReviewSchema,
  listReviewsQuerySchema,
} = require('../validators/review.validator');

const router = express.Router();

// ---------- PUBLIC ----------
router.post('/', validate({ body: createReviewSchema }), reviewController.createReview);
router.get('/public', reviewController.listPublicReviews);

// ---------- PROTECTED ----------
router.get(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  validate({ query: listReviewsQuerySchema }),
  reviewController.listReviews,
);

router.get(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  reviewController.getReview,
);

router.patch(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  validate({ body: updateReviewSchema }),
  reviewController.updateReview,
);

router.delete(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  reviewController.deleteReview,
);

module.exports = router;