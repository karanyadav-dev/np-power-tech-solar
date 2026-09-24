'use strict';

const settingModel = require('../models/setting.model');

async function getAllSettings() {
  return settingModel.getAll();
}

async function getPublicSettings() {
  return settingModel.getPublicSettings();
}

async function updateSetting(key, value, updatedBy) {
  const existing = await settingModel.getByKey(key);
  if (!existing) {
    const err = new Error(`Setting '${key}' not found`);
    err.code = 'SETTING_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return settingModel.update(key, value, updatedBy);
}

async function bulkUpdateSettings(settings, updatedBy) {
  return settingModel.bulkUpdate(settings, updatedBy);
}

module.exports = {
  getAllSettings,
  getPublicSettings,
  updateSetting,
  bulkUpdateSettings,
};