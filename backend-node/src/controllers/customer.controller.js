'use strict';

const customerService = require('../services/customer.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createCustomer = asyncHandler(async (req, res) => {
  const customer = await customerService.createCustomer(req.body);
  return created(res, customer, 'Customer created');
});

const listCustomers = asyncHandler(async (req, res) => {
  const result = await customerService.listCustomers(req.query);
  return success(res, result.data, 'Customers fetched');
});

const getCustomer = asyncHandler(async (req, res) => {
  const customer = await customerService.getCustomer(req.params.id);
  return success(res, customer, 'Customer fetched');
});

const updateCustomer = asyncHandler(async (req, res) => {
  const customer = await customerService.updateCustomer(req.params.id, req.body);
  return success(res, customer, 'Customer updated');
});

const deleteCustomer = asyncHandler(async (req, res) => {
  await customerService.deleteCustomer(req.params.id);
  return success(res, null, 'Customer deleted');
});

module.exports = {
  createCustomer,
  listCustomers,
  getCustomer,
  updateCustomer,
  deleteCustomer,
};