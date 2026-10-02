'use strict';

const quotationService = require('../services/quotation.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

// ---------- Customer: Submit quotation request ----------
const createRequest = asyncHandler(async (req, res) => {
  const quotation = await quotationService.createRequest(req.body);
  return created(res, quotation, 'Quotation request submitted successfully');
});

// ---------- Customer: Pre-create customer (wizard flow) ----------
const preCreateCustomer = asyncHandler(async (req, res) => {
  const db = require('../config/db');
  const { fullName, phone, email, address, city, state, pincode, customerType } = req.body;

  if (!fullName || !phone) {
    const err = new Error('Name and phone are required');
    err.code = 'VALIDATION_ERROR';
    err.status = 400;
    throw err;
  }

  // Check if customer already exists
  const existing = await db.query(
    `SELECT id, full_name, phone FROM customers 
     WHERE phone = $1 AND deleted_at IS NULL 
     LIMIT 1`,
    [phone],
  );

  if (existing.rowCount > 0) {
    return success(res, existing.rows[0], 'Existing customer found');
  }

  // Create new customer
  const result = await db.query(
    `INSERT INTO customers (full_name, phone, email, address, city, state, pincode, customer_type)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
     RETURNING id, full_name, phone`,
    [
      fullName,
      phone,
      email || null,
      address || null,
      city || null,
      state || null,
      pincode || null,
      customerType || 'residential',
    ],
  );

  return created(res, result.rows[0], 'Customer pre-created');
});

// ---------- List quotations (admin) ----------
const listQuotations = asyncHandler(async (req, res) => {
  const result = await quotationService.listQuotations(req.query);
  return success(res, result.data, 'Quotations fetched');
});

// ---------- Get single quotation ----------
const getQuotation = asyncHandler(async (req, res) => {
  const quotation = await quotationService.getQuotation(req.params.id);
  return success(res, quotation, 'Quotation fetched');
});

// ---------- Admin: Start review ----------
const startReview = asyncHandler(async (req, res) => {
  const quotation = await quotationService.startReview(req.params.id, req.user.id);
  return success(res, quotation, 'Review started');
});

// ---------- Admin: Request additional info ----------
const requestInfo = asyncHandler(async (req, res) => {
  const quotation = await quotationService.requestInfo(
    req.params.id,
    req.body,
    req.user.id,
  );
  return success(res, quotation, 'Additional information requested');
});

// ---------- Admin: Verify information ----------
const verifyInfo = asyncHandler(async (req, res) => {
  const quotation = await quotationService.verifyInformation(
    req.params.id,
    req.user.id,
    req.body?.notes,
  );
  return success(res, quotation, 'Information verified');
});

// ---------- Admin: Configure pricing ----------
const configurePricing = asyncHandler(async (req, res) => {
  const quotation = await quotationService.configurePricing(
    req.params.id,
    req.body,
    req.user.id,
  );
  return success(res, quotation, 'Pricing configured');
});

// ---------- Admin: Approve quotation ----------
const approveQuotation = asyncHandler(async (req, res) => {
  const quotation = await quotationService.approveQuotation(
    req.params.id,
    req.user.id,
    req.body?.notes,
  );
  return success(res, quotation, 'Quotation approved');
});

// ---------- Admin: Mark PDF generated (manual) ----------
const markPdfGenerated = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markPdfGenerated(
    req.params.id,
    req.body.pdfUrl,
    req.user.id,
  );
  return success(res, quotation, 'PDF marked as generated');
});

// ---------- Admin: Generate actual PDF file ----------
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

// ---------- Admin: Send to customer ----------
const sendToCustomer = asyncHandler(async (req, res) => {
  const quotation = await quotationService.sendToCustomer(req.params.id, req.user.id);
  return success(res, quotation, 'Quotation sent to customer');
});

// ---------- Customer: View quotation (public) ----------
const markViewed = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markViewed(req.params.id);
  return success(res, quotation, 'Quotation viewed');
});

// ---------- Customer: Accept/Reject (public) ----------
const customerResponse = asyncHandler(async (req, res) => {
  const quotation = await quotationService.customerResponse(
    req.params.id,
    req.body.action,
    req.body.reason,
  );
  return success(res, quotation, `Quotation ${req.body.action}ed`);
});

// ---------- Exports ----------
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
  generatePdf,
  sendToCustomer,
  markViewed,
  customerResponse,
};