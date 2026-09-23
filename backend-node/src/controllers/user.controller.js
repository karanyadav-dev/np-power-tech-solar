'use strict';

const userService = require('../services/user.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createUser = asyncHandler(async (req, res) => {
  const user = await userService.createUser(req.body);
  return created(res, user, 'User created');
});

const listUsers = asyncHandler(async (req, res) => {
  const result = await userService.listUsers(req.query);
  return success(res, result.data, 'Users fetched');
});

const getUser = asyncHandler(async (req, res) => {
  const user = await userService.getUser(req.params.id);
  return success(res, user, 'User fetched');
});

const updateUser = asyncHandler(async (req, res) => {
  const user = await userService.updateUser(req.params.id, req.body);
  return success(res, user, 'User updated');
});

const deleteUser = asyncHandler(async (req, res) => {
  await userService.deleteUser(req.params.id);
  return success(res, null, 'User deleted');
});

const assignRole = asyncHandler(async (req, res) => {
  const result = await userService.assignRoleToUser(req.params.id, req.body.roleName);
  return success(res, result, 'Role assigned');
});

const removeRole = asyncHandler(async (req, res) => {
  const result = await userService.removeRoleFromUser(req.params.id, req.body.roleName);
  return success(res, result, 'Role removed');
});

module.exports = {
  createUser,
  listUsers,
  getUser,
  updateUser,
  deleteUser,
  assignRole,
  removeRole,
};