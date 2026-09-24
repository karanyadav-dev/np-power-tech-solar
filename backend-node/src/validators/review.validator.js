'use strict';

const { z } = require('zod');

const createReviewSchema = z.object({
  customerName: z.string().min(2).max(255),
  customerLocation: z.string().max(255).optional().nullable(),
  customerPhone: z.string().regex(/^[0-9]{10,15}$/).optional().nullable(),
  customerEmail: z.string().email().optional().nullable(),
  rating: z.number().int().min(1).max(5),
  title: z.string().max(255).optional().nullable(),
  reviewText: z.string().min(10).max(2000),
  orderId: z.string().uuid().optional().nullable(),
  customerId: z.string().uuid().optional().nullable(),
});

const updateReviewSchema = z.object({
  isPublished: z.boolean().optional(),
  isVerified: z.boolean().optional(),
});

const listReviewsQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  isPublished: z.coerce.boolean().optional(),
  rating: z.coerce.number().int().min(1).max(5).optional(),
});

module.exports = {
  createReviewSchema,
  updateReviewSchema,
  listReviewsQuerySchema,
};