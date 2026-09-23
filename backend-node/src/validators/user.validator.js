'use strict';

const { z } = require('zod');

const createUserSchema = z.object({
  email: z.string().email().max(255),
  phone: z.string().regex(/^[0-9]{10,15}$/),
  password: z.string().min(8).max(128),
  fullName: z.string().min(2).max(255),
  roles: z.array(z.string()).optional(),
  isActive: z.boolean().optional(),
});

const updateUserSchema = z.object({
  fullName: z.string().min(2).max(255).optional(),
  phone: z.string().regex(/^[0-9]{10,15}$/).optional(),
  isActive: z.boolean().optional(),
  isEmailVerified: z.boolean().optional(),
  isPhoneVerified: z.boolean().optional(),
});

const assignRoleSchema = z.object({
  roleName: z.string().min(2).max(50),
});

const listUsersQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  search: z.string().max(100).optional(),
  isActive: z.coerce.boolean().optional(),
  roleName: z.string().max(50).optional(),
});

module.exports = {
  createUserSchema,
  updateUserSchema,
  assignRoleSchema,
  listUsersQuerySchema,
};