'use strict';

const customerModel = require('../models/customer.model');

async function createCustomer(data) {
  const existing = await customerModel.findByPhoneOrEmail(data.phone, data.email);
  if (existing) {
    const err = new Error('Customer with this phone/email already exists');
    err.code = 'CUSTOMER_EXISTS';
    err.status = 409;
    throw err;
  }
  return customerModel.create(data);
}

async function getCustomer(id) {
  const customer = await customerModel.findById(id);
  if (!customer) {
    const err = new Error('Customer not found');
    err.code = 'CUSTOMER_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return customer;
}

async function listCustomers(query) {
  return customerModel.list(query);
}

async function updateCustomer(id, data) {
  await getCustomer(id);
  const updated = await customerModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }
  return updated;
}

async function deleteCustomer(id) {
  await getCustomer(id);
  const ok = await customerModel.softDelete(id);
  if (!ok) {
    const err = new Error('Delete failed');
    err.code = 'DELETE_FAILED';
    err.status = 500;
    throw err;
  }
  return { id };
}

module.exports = {
  createCustomer,
  getCustomer,
  listCustomers,
  updateCustomer,
  deleteCustomer,
};