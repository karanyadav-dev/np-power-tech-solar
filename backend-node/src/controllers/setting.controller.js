'use strict';

const settingService = require('../services/setting.service');
const asyncHandler = require('../utils/asyncHandler');
const { success } = require('../utils/response');

// Public — safe to expose
const getPublicSettings = asyncHandler(async (req, res) => {
  const settings = await settingService.getPublicSettings();
  // Convert array to key-value map
  const map = {};
  for (const s of settings) {
    map[s.key] = s.value;
  }
  return success(res, map, 'Public settings fetched');
});

// Admin
const getAllSettings = asyncHandler(async (req, res) => {
  const settings = await settingService.getAllSettings();
  return success(res, settings, 'Settings fetched');
});

const updateSetting = asyncHandler(async (req, res) => {
  const { key } = req.params;
  const { value } = req.body;
  const setting = await settingService.updateSetting(key, value, req.user.id);
  return success(res, setting, 'Setting updated');
});

const bulkUpdateSettings = asyncHandler(async (req, res) => {
  const { settings } = req.body;
  const updated = await settingService.bulkUpdateSettings(settings, req.user.id);
  return success(res, updated, 'Settings updated');
});

module.exports = {
  getPublicSettings,
  getAllSettings,
  updateSetting,
  bulkUpdateSettings,
};