'use strict';

const quotationModel = require('../models/quotation.model');

/**
 * Quotation business logic.
 * Enforces status transitions and permissions.
 * NEVER logs pricing details or customer PII.
 */

// ---------- Status transitions map (allowed next states) ----------
const ALLOWED_TRANSITIONS = {
  DRAFT: ['CUSTOMER_SUBMITTED'],
  CUSTOMER_SUBMITTED: ['ADMIN_REVIEW'],
  ADMIN_REVIEW: ['INFORMATION_REQUIRED', 'VERIFIED', 'CUSTOMER_REJECTED'],
  INFORMATION_REQUIRED: ['CUSTOMER_SUBMITTED', 'ADMIN_REVIEW'],
  VERIFIED: ['PRICING_CONFIGURED'],
  PRICING_CONFIGURED: ['PENDING_APPROVAL'],
  PENDING_APPROVAL: ['APPROVED', 'ADMIN_REVIEW'],
  APPROVED: ['PDF_GENERATED'],
  PDF_GENERATED: ['SENT_TO_CUSTOMER'],
  SENT_TO_CUSTOMER: ['CUSTOMER_VIEWED', 'CUSTOMER_ACCEPTED', 'CUSTOMER_REJECTED'],
  CUSTOMER_VIEWED: ['CUSTOMER_ACCEPTED', 'CUSTOMER_REJECTED'],
  CUSTOMER_ACCEPTED: ['CONVERTED_TO_ORDER'],
  CUSTOMER_REJECTED: [],
  CONVERTED_TO_ORDER: [],
  EXPIRED: [],
};

// ---------- Create quotation request ----------
async function createRequest(data) {
  const quotation = await quotationModel.create(data);
  return quotation;
}

// ---------- Get by ID ----------
async function getQuotation(id) {
  const quotation = await quotationModel.findById(id);
  if (!quotation) {
    const err = new Error('Quotation not found');
    err.code = 'QUOTATION_NOT_FOUND';
    err.status = 404;
    throw err;
  }

  // Attach items and versions
  const [items, versions] = await Promise.all([
    quotationModel.getItems(id),
    quotationModel.getVersions(id),
  ]);

  return { ...quotation, items, versions };
}

// ---------- List quotations ----------
async function listQuotations(query) {
  return quotationModel.list(query);
}

// ---------- Admin: Review quotation ----------
async function startReview(id, userId) {
  const quotation = await getQuotation(id);

  if (!ALLOWED_TRANSITIONS[quotation.status]?.includes('ADMIN_REVIEW') && quotation.status !== 'ADMIN_REVIEW') {
    const err = new Error(`Cannot start review from status: ${quotation.status}`);
    err.code = 'INVALID_STATUS_TRANSITION';
    err.status = 400;
    throw err;
  }

  return quotationModel.updateStatus(id, 'ADMIN_REVIEW', userId, 'Admin started review');
}

// ---------- Admin: Request additional info ----------
async function requestInfo(id, { message, requiredFields }, userId) {
  const quotation = await getQuotation(id);

  if (quotation.status !== 'ADMIN_REVIEW') {
    const err = new Error('Can only request info from ADMIN_REVIEW status');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  return quotationModel.updateStatus(
    id,
    'INFORMATION_REQUIRED',
    userId,
    `Info requested: ${message}. Required: ${(requiredFields || []).join(', ')}`,
  );
}

// ---------- Admin: Verify information ----------
async function verifyInformation(id, userId, notes) {
  const quotation = await getQuotation(id);

  if (!['ADMIN_REVIEW', 'INFORMATION_REQUIRED'].includes(quotation.status)) {
    const err = new Error('Can only verify from ADMIN_REVIEW or INFORMATION_REQUIRED');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  return quotationModel.updateStatus(id, 'VERIFIED', userId, notes || 'Information verified');
}

// ---------- Admin: Configure pricing ----------
async function configurePricing(id, pricing, userId) {
  const quotation = await getQuotation(id);

  if (quotation.status !== 'VERIFIED') {
    const err = new Error('Can only configure pricing from VERIFIED status');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  // Validate items
  if (!pricing.items || pricing.items.length === 0) {
    const err = new Error('At least one line item is required');
    err.code = 'NO_ITEMS';
    err.status = 400;
    throw err;
  }

  return quotationModel.savePricing(id, pricing, userId);
}

// ---------- Admin: Approve quotation ----------
async function approveQuotation(id, userId, notes) {
  const quotation = await getQuotation(id);

  if (quotation.status !== 'PENDING_APPROVAL') {
    const err = new Error('Can only approve from PENDING_APPROVAL status');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  // Simulate PDF generation (mark as PDF_GENERATED after approval)
  const updated = await quotationModel.updateStatus(id, 'APPROVED', userId, notes || 'Admin approved');
  return updated;
}

// ---------- Admin: Mark PDF generated ----------
async function markPdfGenerated(id, pdfUrl, userId) {
  const quotation = await getQuotation(id);

  if (quotation.status !== 'APPROVED') {
    const err = new Error('PDF can only be generated after approval');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  // Update PDF URL in DB
  // (we'll extend model if needed, but for now just change status)
  return quotationModel.updateStatus(id, 'PDF_GENERATED', userId, `PDF generated at ${pdfUrl}`);
}

// ---------- Admin: Send to customer ----------
async function sendToCustomer(id, userId) {
  const quotation = await getQuotation(id);

  if (quotation.status !== 'PDF_GENERATED') {
    const err = new Error('Can only send from PDF_GENERATED status');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  return quotationModel.updateStatus(id, 'SENT_TO_CUSTOMER', userId, 'Sent to customer');
}

// ---------- Customer: View quotation ----------
async function markViewed(id) {
  const quotation = await getQuotation(id);

  if (quotation.status === 'SENT_TO_CUSTOMER') {
    return quotationModel.updateStatus(id, 'CUSTOMER_VIEWED', null, 'Customer viewed');
  }

  return quotation;
}

// ---------- Customer: Accept/Reject ----------
async function customerResponse(id, action, reason) {
  const quotation = await getQuotation(id);

  if (!['SENT_TO_CUSTOMER', 'CUSTOMER_VIEWED'].includes(quotation.status)) {
    const err = new Error('Can only respond after quotation is sent');
    err.code = 'INVALID_STATUS';
    err.status = 400;
    throw err;
  }

  const result = await quotationModel.customerResponse(id, action, reason);
  if (result.rowCount === 0) {
    const err = new Error('Customer response failed');
    err.code = 'RESPONSE_FAILED';
    err.status = 500;
    throw err;
  }

  return result.rows[0];
}

module.exports = {
  createRequest,
  getQuotation,
  listQuotations,
  startReview,
  requestInfo,
  verifyInformation,
  configurePricing,
  approveQuotation,
  markPdfGenerated,
  sendToCustomer,
  markViewed,
  customerResponse,
};