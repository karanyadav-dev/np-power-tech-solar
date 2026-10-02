'use strict';

const quotationService = require('../services/quotation.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createRequest = asyncHandler(async (req, res) => {
  const quotation = await quotationService.createRequest(req.body);
  return created(res, quotation, 'Quotation request submitted successfully');
});

// ---------- Pre-create customer (Step 2) ----------
const preCreateCustomer = asyncHandler(async (req, res) => {
  const db = require('../config/db');
  const { fullName, phone, whatsapp, email, address, city, state, pincode } = req.body;

  if (!phone) {
    const err = new Error('Phone is required');
    err.code = 'PHONE_REQUIRED';
    err.status = 400;
    throw err;
  }

  // Check if customer exists
  const existing = await db.query(
    `SELECT id, full_name, phone, email FROM customers WHERE phone = $1 AND deleted_at IS NULL LIMIT 1`,
    [phone],
  );

  if (existing.rowCount > 0) {
    return success(res, { customer: existing.rows[0], exists: true }, 'Customer already exists');
  }

  // Create new customer (partial — will be completed on submission)
  const result = await db.query(
    `INSERT INTO customers (full_name, phone, whatsapp, email, address, city, state, pincode)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
     RETURNING id, full_name, phone, email`,
    [
      fullName || 'New Customer',
      phone,
      whatsapp || null,
      email || null,
      address || null,
      city || null,
      state || null,
      pincode || null,
    ],
  );

  return created(res, { customer: result.rows[0], exists: false }, 'Customer pre-created');
});

const listQuotations = asyncHandler(async (req, res) => {
  const result = await quotationService.listQuotations(req.query);
  return success(res, result.data, 'Quotations fetched');
});

const getQuotation = asyncHandler(async (req, res) => {
  const quotation = await quotationService.getQuotation(req.params.id);
  return success(res, quotation, 'Quotation fetched');
});

const startReview = asyncHandler(async (req, res) => {
  const quotation = await quotationService.startReview(req.params.id, req.user.id);
  return success(res, quotation, 'Review started');
});

const requestInfo = asyncHandler(async (req, res) => {
  const quotation = await quotationService.requestInfo(req.params.id, req.body, req.user.id);
  return success(res, quotation, 'Additional information requested');
});

const verifyInfo = asyncHandler(async (req, res) => {
  const quotation = await quotationService.verifyInformation(req.params.id, req.user.id, req.body?.notes);
  return success(res, quotation, 'Information verified');
});

const configurePricing = asyncHandler(async (req, res) => {
  const quotation = await quotationService.configurePricing(req.params.id, req.body, req.user.id);
  return success(res, quotation, 'Pricing configured');
});

const approveQuotation = asyncHandler(async (req, res) => {
  const quotation = await quotationService.approveQuotation(req.params.id, req.user.id, req.body?.notes);
  return success(res, quotation, 'Quotation approved');
});

const markPdfGenerated = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markPdfGenerated(req.params.id, req.body.pdfUrl, req.user.id);
  return success(res, quotation, 'PDF marked as generated');
});

const sendToCustomer = asyncHandler(async (req, res) => {
  const quotation = await quotationService.sendToCustomer(req.params.id, req.user.id);
  return success(res, quotation, 'Quotation sent to customer');
});

const markViewed = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markViewed(req.params.id);
  return success(res, quotation, 'Quotation viewed');
});

const customerResponse = asyncHandler(async (req, res) => {
  const quotation = await quotationService.customerResponse(req.params.id, req.body.action, req.body.reason);
  return success(res, quotation, `Quotation ${req.body.action}ed`);
});

const generatePdf = asyncHandler(async (req, res) => {
  const pdfService = require('../services/pdf.service');
  const db = require('../config/db');

  const quotation = await quotationService.getQuotation(req.params.id);
  const items = quotation.items || [];

  const customerResult = await db.query(
    `SELECT * FROM customers WHERE id = $1`,
    [quotation.customer_id],
  );
  const customer = customerResult.rows[0] || {};

  const pdfInfo = await pdfService.generateQuotationPDF(quotation, customer, items);

  await db.query(
    `UPDATE quotations SET pdf_url = $1 WHERE id = $2`,
    [pdfInfo.relativePath, req.params.id],
  );

  return success(res, {
    pdfUrl: pdfInfo.relativePath,
    filename: pdfInfo.filename,
  }, 'PDF generated successfully');
});

const updateBankDetails = asyncHandler(async (req, res) => {
  const quotation = await quotationService.updateBankDetails(req.params.id, req.body);
  return success(res, quotation, 'Bank details updated');
});

module.exports = {
  createRequest,
  preCreateCustomer,
  listQuotations,
  getQuotation,
  startReview,
  requestInfo,
  verifyInfo,
  configurePricing,
  approveQuotation,
  markPdfGenerated,
  sendToCustomer,
  markViewed,
  customerResponse,
  generatePdf,
  updateBankDetails,
};