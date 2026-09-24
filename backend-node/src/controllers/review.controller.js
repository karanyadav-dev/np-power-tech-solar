'use strict';

const reviewService = require('../services/review.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createReview = asyncHandler(async (req, res) => {
  const review = await reviewService.createReview(req.body);
  return created(res, review, 'Review submitted — pending approval');
});

const listReviews = asyncHandler(async (req, res) => {
  const result = await reviewService.listReviews(req.query);
  return success(res, {
    reviews: result.data,
    pagination: result.pagination,
    summary: result.summary,
  }, 'Reviews fetched');
});

const listPublicReviews = asyncHandler(async (req, res) => {
  const limit = parseInt(req.query.limit) || 6;
  const reviews = await reviewService.listPublicReviews(limit);
  return success(res, reviews, 'Public reviews fetched');
});

const getReview = asyncHandler(async (req, res) => {
  const review = await reviewService.getReview(req.params.id);
  return success(res, review, 'Review fetched');
});

const updateReview = asyncHandler(async (req, res) => {
  const review = await reviewService.updateReview(req.params.id, req.body);
  return success(res, review, 'Review updated');
});

const deleteReview = asyncHandler(async (req, res) => {
  await reviewService.deleteReview(req.params.id);
  return success(res, null, 'Review deleted');
});

module.exports = {
  createReview,
  listReviews,
  listPublicReviews,
  getReview,
  updateReview,
  deleteReview,
};