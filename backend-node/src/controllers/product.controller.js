'use strict';

const productService = require('../services/product.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createProduct = asyncHandler(async (req, res) => {
  const product = await productService.createProduct(req.body);
  return created(res, product, 'Product created');
});

const listProducts = asyncHandler(async (req, res) => {
  const result = await productService.listProducts(req.query);
  return success(res, result.data, 'Products fetched');
});

const getProduct = asyncHandler(async (req, res) => {
  const product = await productService.getProduct(req.params.id);
  return success(res, product, 'Product fetched');
});

const getProductBySlug = asyncHandler(async (req, res) => {
  const product = await productService.getProductBySlug(req.params.slug);
  return success(res, product, 'Product fetched');
});

const updateProduct = asyncHandler(async (req, res) => {
  const product = await productService.updateProduct(req.params.id, req.body);
  return success(res, product, 'Product updated');
});

const deleteProduct = asyncHandler(async (req, res) => {
  await productService.deleteProduct(req.params.id);
  return success(res, null, 'Product deleted');
});

const listCategories = asyncHandler(async (req, res) => {
  const categories = await productService.listCategories();
  return success(res, categories, 'Categories fetched');
});

const createCategory = asyncHandler(async (req, res) => {
  const category = await productService.createCategory(req.body);
  return created(res, category, 'Category created');
});

module.exports = {
  createProduct,
  listProducts,
  getProduct,
  getProductBySlug,
  updateProduct,
  deleteProduct,
  listCategories,
  createCategory,
};