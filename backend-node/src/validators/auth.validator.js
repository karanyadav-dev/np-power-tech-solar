'use strict';

const { z } = require('zod');

const registerSchema = z.object({
  email: z.string().email('Invalid email').max(255),
  phone: z.string().regex(/^[0-9]{10,15}$/, 'Invalid phone (10-15 digits)'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .max(128, 'Password too long'),
  fullName: z.string().min(2, 'Name too short').max(255),
});

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password required'),
});

const refreshSchema = z.object({
  refreshToken: z.string().min(10, 'Invalid refresh token'),
});

module.exports = {
  registerSchema,
  loginSchema,
  refreshSchema,
};