'use strict';

const { z } = require('zod');

// Step 1: Solar Requirement
const solarRequirementSchema = z.object({
  systemSizeKw: z.number().positive().max(1000),
  customerType: z.enum(['residential', 'commercial', 'industrial']),
  systemType: z.enum(['on-grid', 'off-grid', 'hybrid']),
  batteryRequired: z.boolean().optional(),
});

// Step 2: Customer Info
const customerInfoSchema = z.object({
  fullName: z.string().min(2).max(255),
  phone: z.string().regex(/^[0-9]{10,15}$/),
  whatsapp: z.string().regex(/^[0-9]{10,15}$/).optional().nullable(),
  email: z.string().email().optional().nullable(),
  address: z.string().max(500),
  city: z.string().max(100),
  state: z.string().max(100),
  pincode: z.string().max(10),
});

// Step 3: Electricity Info
const electricityInfoSchema = z.object({
  discomName: z.string().max(100).optional().nullable(),
  monthlyBill: z.number().nonnegative().optional().nullable(),
  monthlyUnits: z.number().int().nonnegative().optional().nullable(),
  sanctionedLoad: z.number().nonnegative().optional().nullable(),
  connectionType: z.string().max(50).optional().nullable(),
});

// Step 4: Roof/Site Info
const roofInfoSchema = z.object({
  roofArea: z.number().nonnegative().optional().nullable(),
  roofType: z.string().max(50).optional().nullable(),
  buildingType: z.string().max(50).optional().nullable(),
  roofOwnership: z.string().max(50).optional().nullable(),
  additionalInfo: z.string().max(2000).optional().nullable(),
});

// Step 5: Preferences
const preferencesSchema = z.object({
  financingRequired: z.boolean().optional(),
  notes: z.string().max(2000).optional().nullable(),
});

// Complete wizard submission
const createQuotationRequestSchema = z.object({
  solarRequirement: solarRequirementSchema,
  customerInfo: customerInfoSchema,
  electricityInfo: electricityInfoSchema,
  roofInfo: roofInfoSchema,
  preferences: preferencesSchema,
});

// Admin review — mark information status
const reviewInfoSchema = z.object({
  status: z.enum(['complete', 'missing', 'needs_correction', 'verified', 'rejected']),
  notes: z.string().max(1000).optional().nullable(),
});

// Admin — request additional info
const requestInfoSchema = z.object({
  message: z.string().min(10).max(2000),
  requiredFields: z.array(z.string()).optional(),
});

// Admin — configure pricing
const configurePricingSchema = z.object({
  items: z.array(z.object({
    itemName: z.string().min(1).max(255),
    description: z.string().max(1000).optional().nullable(),
    quantity: z.number().positive(),
    unit: z.string().max(20).optional().default('pcs'),
    unitPrice: z.number().nonnegative(),
  })).min(1),
  discount: z.number().nonnegative().optional().default(0),
  gstPercentage: z.number().min(0).max(28).optional().default(18),
  subsidyAmount: z.number().nonnegative().optional().default(0),
  paymentTerms: z.string().max(1000).optional().nullable(),
  warrantyTerms: z.string().max(1000).optional().nullable(),
  termsConditions: z.string().max(5000).optional().nullable(),
  validUntilDays: z.number().int().positive().optional().default(30),
  adminNotes: z.string().max(2000).optional().nullable(),
});

// Admin — approve
const approveQuotationSchema = z.object({
  notes: z.string().max(1000).optional().nullable(),
});

// Customer — accept / reject
const customerResponseSchema = z.object({
  action: z.enum(['accept', 'reject']),
  reason: z.string().max(1000).optional().nullable(),
});

// List query
const listQuotationsQuerySchema = z.object({
  page: z.coerce.number().int().positive().optional().default(1),
  limit: z.coerce.number().int().positive().max(100).optional().default(20),
  status: z.string().max(50).optional(),
  customerId: z.string().uuid().optional(),
  leadId: z.string().uuid().optional(),
  search: z.string().max(100).optional(),
});

module.exports = {
  createQuotationRequestSchema,
  reviewInfoSchema,
  requestInfoSchema,
  configurePricingSchema,
  approveQuotationSchema,
  customerResponseSchema,
  listQuotationsQuerySchema,
};