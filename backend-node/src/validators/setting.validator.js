'use strict';

const { z } = require('zod');

const updateSettingsSchema = z.object({
  settings: z.array(
    z.object({
      key: z.string().min(1).max(100),
      value: z.string().max(5000),
    })
  ).min(1),
});

const createSettingSchema = z.object({
  key: z.string().min(1).max(100),
  value: z.string().max(5000),
  valueType: z.enum(['string', 'number', 'boolean', 'json']).optional(),
  category: z.string().max(50).optional(),
  description: z.string().max(500).optional(),
});

module.exports = {
  updateSettingsSchema,
  createSettingSchema,
};