'use strict';

const { z } = require('zod');

const LEAD_STATUSES = [
  'NEW', 'CONTACTED', 'QUALIFIED', 'SITE_SURVEY', 'QUOTATION',
  'NEGOTIATION', 'APPROVED', 'ORDER', 'INSTALLATION', 'COMPLETED', 'AMC', 'LOST',
];

const createLeadSchema = z.object({
  fullName: z.string().min(2).max(255),
  phone: z.string().regex(/^[0-9]{10,15}$/, 'Invalid phone (10-15 digits)'),
  whatsapp: z.string().regex(/^[0-9]{10,15}$/).optional().nullable(),
  email: z.string().email().optional().nullable(),
  address: z.string().max(500).optional().nullable(),
  city: z.string().max(100).optional().nullable(),
  state: z.string().max(100).optional().nullable(),
  pincode: z.string().max(10).optional().nullable(),
  monthlyBill: z.number().nonnegative().optional().nullable(),
  monthlyUnits: z.number().int().nonnegative().optional().nullable(),
  systemSizeKw: z.number().nonnegative().optional().nullable(),
  propertyType: z.string().max(50).optional().nullable(),
  systemType: z.string().max(50).optional().nullable(),
  batteryRequired: z.boolean().optional(),
  message: z.string().max(2000).optional().nullable(),
  sourceCode: z.string().max(50).optional().nullable(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']).optional(),
  utmSource: z.string().max(100).optional().nullable(),
  utmMedium: z.string().max(100).optional().nullable(),
  utmCampaign: z.string().max(100).optional().nullable(),
  utmContent: z.string().max(100).optional().nullable(),
  landingPage: z.string().max(500).optional().nullable(),
  referrer: z.string().max(500).optional().nullable(),
});

const updateLeadSchema = z.object({
  fullName: z.string().min(2).max(255).optional(),
  phone: z.string().regex(/^[0-9]{10,15}$/).optional(),
  whatsapp: z.string().regex(/^[0-9]{10,15}$/).optional().nullable(),
  email: z.string().email().optional().nullable(),
  address: z.string().max(500).optional().nullable(),
  city: z.string().max(100).optional().nullable(),
  state: z.string().max(100).optional().nullable(),
  pincode: z.string().max(10).optional().nullable(),
  monthlyBill: z.number().nonnegative().optional().nullable(),
  monthlyUnits: z.number().int().nonnegative().optional().nullable(),
  systemSizeKw: z.number().nonnegative().optional().nullable(),
  propertyType: z.string().max(50).optional().nullable(),
  systemType: z.string().max(50).optional().nullable(),
  batteryRequired: z.boolean().optional(),
  message: z.string().max(2000).optional().nullable(),
  priority: z.enum(['low', 'medium', 'high', 'urgent']).optional(),
});

const updateStatusSchema = z.object({
  status: z.enum(LEAD_STATUSES),
  notes: z.string().max(1000).optional().nullable(),
  lostReason: z.string().max(500).optional().nullable(),
});

const assignLeadSchema = z.object({
  assignedTo: z.string().uuid(),
});

const followupSchema = z.object({
  followupType: z.enum(['call', 'whatsapp', 'email', 'meeting', 'site_visit', 'other']),
  scheduledAt: z.string().datetime().optional().nullable(),
  notes: z.string().max(2000).optional().nullable(),
  outcome: z.string().max(100).optional().nullable(),
});

const listLeadsQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  status: z.enum(LEAD_STATUSES).optional(),
  assignedTo: z.string().uuid().optional(),
  pincode: z.string().max(10).optional(),
  search: z.string().max(100).optional(),
  from: z.string().optional(),
  to: z.string().optional(),
});

module.exports = {
  LEAD_STATUSES,
  createLeadSchema,
  updateLeadSchema,
  updateStatusSchema,
  assignLeadSchema,
  followupSchema,
  listLeadsQuerySchema,
};