'use strict';

const { z } = require('zod');

const createCustomerSchema = z.object({
  fullName: z.string().min(2).max(255),
  phone: z.string().regex(/^[0-9]{10,15}$/, 'Invalid phone (10-15 digits)'),
  whatsapp: z.string().regex(/^[0-9]{10,15}$/).optional().nullable(),
  email: z.string().email().optional().nullable(),
  address: z.string().max(500).optional().nullable(),
  city: z.string().max(100).optional().nullable(),
  state: z.string().max(100).optional().nullable(),
  pincode: z.string().max(10).optional().nullable(),
  gstNumber: z.string().max(20).optional().nullable(),
  customerType: z.enum(['residential', 'commercial', 'industrial']).optional(),
  notes: z.string().max(2000).optional().nullable(),
});

const updateCustomerSchema = createCustomerSchema.partial();

const listCustomersQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  customerType: z.enum(['residential', 'commercial', 'industrial']).optional(),
  pincode: z.string().max(10).optional(),
  search: z.string().max(100).optional(),
});

module.exports = {
  createCustomerSchema,
  updateCustomerSchema,
  listCustomersQuerySchema,
};