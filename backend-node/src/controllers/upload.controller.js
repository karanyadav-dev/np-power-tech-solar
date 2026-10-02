'use strict';

const multer = require('multer');
const asyncHandler = require('../utils/asyncHandler');
const { success, created, badRequest } = require('../utils/response');
const uploadService = require('../services/upload.service');
const db = require('../config/db');

// Multer — memory storage (we save to disk ourselves for MIME validation)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
});

const uploadMiddleware = upload.single('file');

const uploadFile = asyncHandler(async (req, res) => {
  if (!req.file) {
    return badRequest(res, 'No file uploaded');
  }

  const uploadType = req.body.uploadType;
  const customerId = req.body.customerId || null;
  const leadId = req.body.leadId || null;
  const quotationId = req.body.quotationId || null;
  const description = req.body.description || null;

  if (!uploadType) {
    return badRequest(res, 'uploadType is required');
  }

  // Validate & save
  const fileInfo = await uploadService.validateAndSave(
    req.file.buffer,
    req.file.originalname,
    uploadType,
  );

  // Save metadata in DB (documents table)
  const doc = await db.query(
    `INSERT INTO documents (
      customer_id, order_id, quotation_id, survey_id, warranty_id,
      document_type, title, file_url, file_size, mime_type, uploaded_by
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    RETURNING id, document_type, title, file_url, file_size, mime_type, created_at`,
    [
      customerId, null, quotationId, null, null,
      uploadType,
      description || req.file.originalname,
      fileInfo.relativePath,
      fileInfo.size,
      fileInfo.mimetype,
      req.user?.id || null,
    ],
  );

  return created(res, {
    document: doc.rows[0],
    ...fileInfo,
  }, 'File uploaded successfully');
});

const listDocuments = asyncHandler(async (req, res) => {
  const { customerId, quotationId, documentType } = req.query;

  let query = `SELECT d.*, 
                      u.full_name AS uploaded_by_name,
                      c.full_name AS customer_name,
                      c.phone AS customer_phone,
                      c.city AS customer_city,
                      c.email AS customer_email
               FROM documents d
               LEFT JOIN users u ON u.id = d.uploaded_by
               LEFT JOIN customers c ON c.id = d.customer_id
               WHERE 1=1`;
  const params = [];
  let idx = 1;

  if (customerId) {
    query += ` AND d.customer_id = $${idx++}`;
    params.push(customerId);
  }
  if (quotationId) {
    query += ` AND d.quotation_id = $${idx++}`;
    params.push(quotationId);
  }
  if (documentType) {
    query += ` AND d.document_type = $${idx++}`;
    params.push(documentType);
  }

  query += ' ORDER BY d.created_at DESC';

  const result = await db.query(query, params);
  return success(res, result.rows, 'Documents fetched');
});

// ---------- Link document to customer ----------
const linkDocumentToCustomer = asyncHandler(async (req, res) => {
  const { id } = req.params;
  const { customerId } = req.body;

  if (!customerId) {
    return badRequest(res, 'customerId is required');
  }

  // Verify customer exists
  const customer = await db.query(
    `SELECT id, full_name, phone FROM customers WHERE id = $1 AND deleted_at IS NULL`,
    [customerId],
  );

  if (customer.rowCount === 0) {
    return badRequest(res, 'Customer not found');
  }

  // Update document
  const result = await db.query(
    `UPDATE documents SET customer_id = $1 WHERE id = $2 RETURNING *`,
    [customerId, id],
  );

  if (result.rowCount === 0) {
    return badRequest(res, 'Document not found');
  }

  return success(res, result.rows[0], 'Document linked to customer');
});

const deleteDocument = asyncHandler(async (req, res) => {
  const { id } = req.params;

  const doc = await db.query(`SELECT file_url FROM documents WHERE id = $1`, [id]);
  if (doc.rowCount === 0) {
    return badRequest(res, 'Document not found');
  }

  uploadService.deleteFile(doc.rows[0].file_url);
  await db.query(`DELETE FROM documents WHERE id = $1`, [id]);

  return success(res, null, 'Document deleted');
});

module.exports = {
  uploadMiddleware,
  uploadFile,
  listDocuments,
  linkDocumentToCustomer,
  deleteDocument,
};