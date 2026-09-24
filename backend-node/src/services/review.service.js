'use strict';

const reviewModel = require('../models/review.model');

async function createReview(data) {
  return reviewModel.create(data);
}

async function getReview(id) {
  const review = await reviewModel.findById(id);
  if (!review) {
    const err = new Error('Review not found');
    err.code = 'REVIEW_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return review;
}

async function listReviews(query) {
  return reviewModel.list(query);
}

async function listPublicReviews(limit = 6) {
  return reviewModel.listPublic(limit);
}

async function updateReview(id, data) {
  await getReview(id);
  const updated = await reviewModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }
  return updated;
}

async function deleteReview(id) {
  await getReview(id);
  await reviewModel.softDelete(id);
  return { id };
}

module.exports = {
  createReview,
  getReview,
  listReviews,
  listPublicReviews,
  updateReview,
  deleteReview,
};