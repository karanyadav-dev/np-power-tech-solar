'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { fileTypeFromBuffer } = require('file-type');
const storage = require('../config/storage');
const { ALLOWED_MIMES, MAX_FILE_SIZE } = require('../validators/upload.validator');

/**
 * File upload service.
 * Validates MIME via magic bytes (not just extension).
 */

const ALL_ALLOWED_MIMES = [
  ...ALLOWED_MIMES.image,
  ...ALLOWED_MIMES.pdf,
  ...ALLOWED_MIMES.document,
];

function safeFilename(originalName) {
  const ext = path.extname(originalName).toLowerCase();
  const random = crypto.randomBytes(16).toString('hex');
  const timestamp = Date.now();
  return `${timestamp}-${random}${ext}`;
}

async function validateAndSave(buffer, originalName, uploadType) {
  // Size check
  if (buffer.length > MAX_FILE_SIZE) {
    const err = new Error(`File too large (max ${MAX_FILE_SIZE / 1024 / 1024} MB)`);
    err.code = 'FILE_TOO_LARGE';
    err.status = 400;
    throw err;
  }

  // Magic byte validation (don't trust extension)
  const detected = await fileTypeFromBuffer(buffer);
  if (!detected || !ALL_ALLOWED_MIMES.includes(detected.mime)) {
    const err = new Error('Invalid file type (MIME check failed)');
    err.code = 'INVALID_FILE_TYPE';
    err.status = 400;
    throw err;
  }

  // Safe filename
  const filename = safeFilename(originalName);

  // Save to disk
  const dir = storage.getUploadPath(uploadType);
  const filepath = path.join(dir, filename);
  fs.writeFileSync(filepath, buffer);

  // Return relative path (for DB storage + URL access)
  const relativePath = storage.getRelativePath(uploadType, filename);

  return {
    filename,
    originalName,
    filepath,
    relativePath,
    mimetype: detected.mime,
    size: buffer.length,
    uploadedAt: new Date(),
  };
}

function deleteFile(relativePath) {
  try {
    const cleanPath = relativePath.replace(/^\/uploads\//, '');
    const fullPath = path.join(storage.STORAGE_ROOT, cleanPath);
    if (fs.existsSync(fullPath)) {
      fs.unlinkSync(fullPath);
      return true;
    }
  } catch (err) {
    return false;
  }
  return false;
}

module.exports = { validateAndSave, deleteFile };