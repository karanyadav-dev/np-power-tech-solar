'use strict';

const { z } = require('zod');

const uploadTypes = [
  'customer_documents',
  'site_photos',
  'roof_photos',
  'electricity_bills',
  'project_images',
];

const uploadMetadataSchema = z.object({
  uploadType: z.enum(uploadTypes),
  customerId: z.string().uuid().optional().nullable(),
  leadId: z.string().uuid().optional().nullable(),
  quotationId: z.string().uuid().optional().nullable(),
  description: z.string().max(500).optional().nullable(),
});

// Allowed MIME types
const ALLOWED_MIMES = {
  image: ['image/jpeg', 'image/png', 'image/webp', 'image/jpg'],
  pdf: ['application/pdf'],
  document: [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  ],
};

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

module.exports = {
  uploadMetadataSchema,
  ALLOWED_MIMES,
  MAX_FILE_SIZE,
  uploadTypes,
};