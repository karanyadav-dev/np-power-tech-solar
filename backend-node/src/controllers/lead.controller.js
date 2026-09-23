'use strict';

const leadService = require('../services/lead.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createLead = asyncHandler(async (req, res) => {
  const lead = await leadService.createLead(req.body, req.user?.id || null);
  return created(res, lead, 'Lead created successfully');
});

const listLeads = asyncHandler(async (req, res) => {
  const result = await leadService.listLeads(req.query);
  return success(res, result.data, 'Leads fetched', 200);
});

const getLead = asyncHandler(async (req, res) => {
  const lead = await leadService.getLead(req.params.id);
  return success(res, lead, 'Lead fetched');
});

const updateLead = asyncHandler(async (req, res) => {
  const lead = await leadService.updateLead(req.params.id, req.body);
  return success(res, lead, 'Lead updated');
});

const updateStatus = asyncHandler(async (req, res) => {
  const lead = await leadService.changeStatus(req.params.id, req.body, req.user.id);
  return success(res, lead, 'Lead status updated');
});

const assignLead = asyncHandler(async (req, res) => {
  const lead = await leadService.assignLead(req.params.id, req.body, req.user.id);
  return success(res, lead, 'Lead assigned');
});

const addFollowup = asyncHandler(async (req, res) => {
  const followup = await leadService.addFollowup(req.params.id, req.body, req.user.id);
  return created(res, followup, 'Follow-up added');
});

const listFollowups = asyncHandler(async (req, res) => {
  const followups = await leadService.getFollowups(req.params.id);
  return success(res, followups, 'Follow-ups fetched');
});

module.exports = {
  createLead,
  listLeads,
  getLead,
  updateLead,
  updateStatus,
  assignLead,
  addFollowup,
  listFollowups,
};