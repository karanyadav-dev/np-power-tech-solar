'use strict';

const productModel = require('../models/product.model');

async function createProduct(data) {
  if (await productModel.slugExists(data.slug)) {
    const err = new Error('Product slug already exists');
    err.code = 'SLUG_EXISTS';
    err.status = 409;
    throw err;
  }
  return productModel.create(data);
}

async function getProduct(id) {
  const product = await productModel.findById(id);
  if (!product) {
    const err = new Error('Product not found');
    err.code = 'PRODUCT_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return product;
}

async function getProductBySlug(slug) {
  const product = await productModel.findBySlug(slug);
  if (!product) {
    const err = new Error('Product not found');
    err.code = 'PRODUCT_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return product;
}

async function listProducts(query) {
  return productModel.list(query);
}

async function updateProduct(id, data) {
  await getProduct(id);
  if (data.slug) {
    const existing = await productModel.findBySlug(data.slug);
    if (existing && existing.id !== id) {
      const err = new Error('Product slug already exists');
      err.code = 'SLUG_EXISTS';
      err.status = 409;
      throw err;
    }
  }
  const updated = await productModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }
  return updated;
}

async function deleteProduct(id) {
  await getProduct(id);
  const ok = await productModel.softDelete(id);
  if (!ok) {
    const err = new Error('Delete failed');
    err.code = 'DELETE_FAILED';
    err.status = 500;
    throw err;
  }
  return { id };
}

async function listCategories() {
  return productModel.listCategories();
}

async function createCategory(data) {
  return productModel.createCategory(data);
}

module.exports = {
  createProduct,
  getProduct,
  getProductBySlug,
  listProducts,
  updateProduct,
  deleteProduct,
  listCategories,
  createCategory,
};