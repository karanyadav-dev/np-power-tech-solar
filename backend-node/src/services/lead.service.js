'use strict';

const leadModel = require('../models/lead.model');

/**
 * Lead business logic.
 */

async function createLead(data, userId = null) {
  // Duplicate detection
  const duplicate = await leadModel.findDuplicate(data.phone, data.email);
  if (duplicate) {
    const err = new Error(`Duplicate lead: similar lead exists (${duplicate.lead_number})`);
    err.code = 'DUPLICATE_LEAD';
    err.status = 409;
    err.details = { existingLeadId: duplicate.id, leadNumber: duplicate.lead_number };
    throw err;
  }

  const lead = await leadModel.create(data);

  // Log status history (initial)
  if (userId) {
    await leadModel.updateStatus(lead.id, { status: 'NEW', notes: 'Lead created' }, userId);
  }

  return lead;
}

async function getLead(id) {
  const lead = await leadModel.findById(id);
  if (!lead) {
    const err = new Error('Lead not found');
    err.code = 'LEAD_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return lead;
}

async function listLeads(query) {
  return leadModel.list(query);
}

async function updateLead(id, data) {
  await getLead(id); // ensure exists
  const updated = await leadModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }
  return updated;
}

async function changeStatus(id, payload, changedBy) {
  await getLead(id);
  const updated = await leadModel.updateStatus(id, payload, changedBy);
  if (!updated) {
    const err = new Error('Lead not found');
    err.code = 'LEAD_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return updated;
}

async function assignLead(id, { assignedTo }, assignedBy) {
  await getLead(id);
  const updated = await leadModel.assign(id, assignedTo, assignedBy);
  if (!updated) {
    const err = new Error('Lead not found');
    err.code = 'LEAD_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return updated;
}

async function addFollowup(id, data, userId) {
  await getLead(id);
  return leadModel.addFollowup(id, data, userId);
}

async function getFollowups(id) {
  await getLead(id);
  return leadModel.listFollowups(id);
}

module.exports = {
  createLead,
  getLead,
  listLeads,
  updateLead,
  changeStatus,
  assignLead,
  addFollowup,
  getFollowups,
};