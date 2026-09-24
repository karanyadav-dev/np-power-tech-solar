'use strict';

const path = require('path');
const fs = require('fs');

/**
 * Storage configuration.
 * Development: local filesystem
 * Production: S3 (configure via env)
 */

const STORAGE_ROOT = path.join(__dirname, '..', '..', '..', 'storage', 'uploads');

// Subfolders for organized storage
const UPLOAD_TYPES = {
  customer_documents: 'documents',
  site_photos: 'site_photos',
  roof_photos: 'roof_photos',
  electricity_bills: 'electricity_bills',
  quotation_pdfs: 'quotation_pdfs',
  invoice_pdfs: 'invoice_pdfs',
  project_images: 'project_images',
};

function ensureDirectoryExists(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function getUploadPath(uploadType) {
  const subfolder = UPLOAD_TYPES[uploadType] || 'misc';
  const fullPath = path.join(STORAGE_ROOT, subfolder);
  ensureDirectoryExists(fullPath);
  return fullPath;
}

function getRelativePath(uploadType, filename) {
  const subfolder = UPLOAD_TYPES[uploadType] || 'misc';
  return `/uploads/${subfolder}/${filename}`;
}

module.exports = {
  STORAGE_ROOT,
  UPLOAD_TYPES,
  getUploadPath,
  getRelativePath,
  ensureDirectoryExists,
};