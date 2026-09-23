'use strict';

const roleService = require('../services/role.service');
const asyncHandler = require('../utils/asyncHandler');
const { success } = require('../utils/response');

const listRoles = asyncHandler(async (req, res) => {
  const roles = await roleService.listRoles();
  return success(res, roles, 'Roles fetched');
});

const listPermissions = asyncHandler(async (req, res) => {
  const permissions = await roleService.listPermissions();
  return success(res, permissions, 'Permissions fetched');
});

const getRolePermissions = asyncHandler(async (req, res) => {
  const permissions = await roleService.getRolePermissions(req.params.roleName);
  return success(res, permissions, 'Role permissions fetched');
});

module.exports = { listRoles, listPermissions, getRolePermissions };