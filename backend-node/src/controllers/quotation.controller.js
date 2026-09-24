'use strict';

const quotationService = require('../services/quotation.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

// ---------- Customer: Submit quotation request ----------
const createRequest = asyncHandler(async (req, res) => {
  const quotation = await quotationService.createRequest(req.body);
  return created(res, quotation, 'Quotation request submitted successfully');
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

// ---------- Admin: Mark PDF generated ----------
const markPdfGenerated = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markPdfGenerated(
    req.params.id,
    req.body.pdfUrl,
    req.user.id,
  );
  return success(res, quotation, 'PDF marked as generated');
});

// ---------- Admin: Send to customer ----------
const sendToCustomer = asyncHandler(async (req, res) => {
  const quotation = await quotationService.sendToCustomer(req.params.id, req.user.id);
  return success(res, quotation, 'Quotation sent to customer');
});

// ---------- Customer: View quotation ----------
const markViewed = asyncHandler(async (req, res) => {
  const quotation = await quotationService.markViewed(req.params.id);
  return success(res, quotation, 'Quotation viewed');
});

// ---------- Customer: Accept/Reject ----------
const customerResponse = asyncHandler(async (req, res) => {
  const quotation = await quotationService.customerResponse(
    req.params.id,
    req.body.action,
    req.body.reason,
  );
  return success(res, quotation, `Quotation ${req.body.action}ed`);
});

module.exports = {
  createRequest,
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
};