'use strict';

const authService = require('../services/auth.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

/**
 * Auth controllers — thin layer, all logic in service.
 */

const register = asyncHandler(async (req, res) => {
  const meta = {
    ipAddress: req.ip,
    userAgent: req.headers['user-agent'],
  };
  const result = await authService.register(req.body, meta);
  return created(res, result, 'Registration successful');
});

const login = asyncHandler(async (req, res) => {
  const meta = {
    ipAddress: req.ip,
    userAgent: req.headers['user-agent'],
  };
  const result = await authService.login(req.body, meta);
  return success(res, result, 'Login successful');
});

const refresh = asyncHandler(async (req, res) => {
  const result = await authService.refresh(req.body);
  return success(res, result, 'Token refreshed');
});

const logout = asyncHandler(async (req, res) => {
  await authService.logout(req.body || {});
  return success(res, null, 'Logout successful');
});

const me = asyncHandler(async (req, res) => {
  const result = await authService.me(req.user.id);
  return success(res, result, 'Profile fetched');
});

module.exports = { register, login, refresh, logout, me };