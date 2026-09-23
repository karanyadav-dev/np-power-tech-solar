'use strict';

const { z } = require('zod');

const createProductSchema = z.object({
  name: z.string().min(2).max(255),
  slug: z.string().min(2).max(255).regex(/^[a-z0-9-]+$/, 'Slug must be lowercase alphanumeric with hyphens'),
  categoryId: z.string().uuid().optional().nullable(),
  brand: z.string().max(100).optional().nullable(),
  model: z.string().max(100).optional().nullable(),
  capacity: z.string().max(50).optional().nullable(),
  specifications: z.record(z.any()).optional().nullable(),
  price: z.number().nonnegative().optional().nullable(),
  warrantyYears: z.number().int().nonnegative().optional().nullable(),
  description: z.string().max(5000).optional().nullable(),
  isAvailable: z.boolean().optional(),
  isFeatured: z.boolean().optional(),
});

const updateProductSchema = createProductSchema.partial();

const createCategorySchema = z.object({
  name: z.string().min(2).max(100),
  slug: z.string().min(2).max(100).regex(/^[a-z0-9-]+$/),
  description: z.string().max(2000).optional().nullable(),
  displayOrder: z.number().int().nonnegative().optional(),
});

const listProductsQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  categoryId: z.string().uuid().optional(),
  brand: z.string().max(100).optional(),
  isFeatured: z.coerce.boolean().optional(),
  isAvailable: z.coerce.boolean().optional(),
  search: z.string().max(100).optional(),
});

module.exports = {
  createProductSchema,
  updateProductSchema,
  createCategorySchema,
  listProductsQuerySchema,
};