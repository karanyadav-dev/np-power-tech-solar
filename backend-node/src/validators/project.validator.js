'use strict';

const { z } = require('zod');

const createProjectSchema = z.object({
  projectName: z.string().min(2).max(255),
  slug: z.string().min(2).max(255).regex(/^[a-z0-9-]+$/, 'Slug must be lowercase with hyphens'),
  location: z.string().max(255).optional().nullable(),
  city: z.string().max(100).optional().nullable(),
  state: z.string().max(100).optional().nullable(),
  pincode: z.string().max(10).optional().nullable(),
  systemSizeKw: z.number().positive().optional().nullable(),
  systemType: z.string().max(50).optional().nullable(),
  installationDate: z.string().optional().nullable(),
  description: z.string().max(5000).optional().nullable(),
  customerApproval: z.boolean().optional().default(false),
  isPublished: z.boolean().optional().default(false),
  images: z.array(z.string().max(500)).optional().default([]),
});

const updateProjectSchema = createProjectSchema.partial();

const listProjectsQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  isPublished: z.coerce.boolean().optional(),
  city: z.string().max(100).optional(),
  search: z.string().max(100).optional(),
});

module.exports = {
  createProjectSchema,
  updateProjectSchema,
  listProjectsQuerySchema,
};