'use strict';

const userModel = require('../models/user.model');
const sessionModel = require('../models/session.model');
const { hashPassword, verifyPassword } = require('../utils/password');
const { signAccessToken, signRefreshToken, verifyRefreshToken } = require('../utils/jwt');

/**
 * Auth business logic.
 * NEVER logs passwords or tokens.
 */

const REFRESH_DAYS = 7;

function buildTokens(user, roles) {
  const payload = {
    sub: user.id,
    email: user.email,
    roles,
  };

  const accessToken = signAccessToken(payload);
  const refreshToken = signRefreshToken({ sub: user.id });

  return { accessToken, refreshToken };
}

async function register({ email, phone, password, fullName }, meta = {}) {
  // Check duplicates
  if (await userModel.emailExists(email)) {
    const err = new Error('Email already registered');
    err.code = 'EMAIL_EXISTS';
    err.status = 409;
    throw err;
  }
  if (await userModel.phoneExists(phone)) {
    const err = new Error('Phone already registered');
    err.code = 'PHONE_EXISTS';
    err.status = 409;
    throw err;
  }

  const passwordHash = await hashPassword(password);
  const user = await userModel.create({ email, phone, passwordHash, fullName });

  // Assign default customer role (self-registered users are customers)
  await userModel.assignRole(user.id, 'customer');

  const roles = await userModel.getUserRoles(user.id);
  const tokens = buildTokens(user, roles);

  // Persist refresh session
  const expiresAt = new Date(Date.now() + REFRESH_DAYS * 24 * 60 * 60 * 1000);
  await sessionModel.create({
    userId: user.id,
    refreshToken: tokens.refreshToken,
    ipAddress: meta.ipAddress,
    userAgent: meta.userAgent,
    expiresAt,
  });

  return {
    user: {
      id: user.id,
      email: user.email,
      phone: user.phone,
      fullName: user.full_name,
      roles,
    },
    ...tokens,
  };
}

async function login({ email, password }, meta = {}) {
  const user = await userModel.findByEmail(email);
  if (!user || !user.is_active) {
    const err = new Error('Invalid credentials');
    err.code = 'INVALID_CREDENTIALS';
    err.status = 401;
    throw err;
  }

  const ok = await verifyPassword(user.password_hash, password);
  if (!ok) {
    const err = new Error('Invalid credentials');
    err.code = 'INVALID_CREDENTIALS';
    err.status = 401;
    throw err;
  }

  const roles = await userModel.getUserRoles(user.id);
  const tokens = buildTokens(user, roles);

  const expiresAt = new Date(Date.now() + REFRESH_DAYS * 24 * 60 * 60 * 1000);
  await sessionModel.create({
    userId: user.id,
    refreshToken: tokens.refreshToken,
    ipAddress: meta.ipAddress,
    userAgent: meta.userAgent,
    expiresAt,
  });

  await userModel.updateLastLogin(user.id);

  return {
    user: {
      id: user.id,
      email: user.email,
      phone: user.phone,
      fullName: user.full_name,
      roles,
    },
    ...tokens,
  };
}

async function refresh({ refreshToken }) {
  const payload = verifyRefreshToken(refreshToken);
  if (!payload) {
    const err = new Error('Invalid refresh token');
    err.code = 'INVALID_REFRESH';
    err.status = 401;
    throw err;
  }

  const session = await sessionModel.findValidByToken(refreshToken);
  if (!session) {
    const err = new Error('Session expired or revoked');
    err.code = 'SESSION_INVALID';
    err.status = 401;
    throw err;
  }

  const user = await userModel.findById(payload.sub);
  if (!user || !user.is_active) {
    const err = new Error('User not found or inactive');
    err.code = 'USER_INVALID';
    err.status = 401;
    throw err;
  }

  const roles = await userModel.getUserRoles(user.id);
  const tokens = buildTokens(user, roles);

  // Rotate refresh token
  await sessionModel.revoke(session.id);
  const expiresAt = new Date(Date.now() + REFRESH_DAYS * 24 * 60 * 60 * 1000);
  await sessionModel.create({
    userId: user.id,
    refreshToken: tokens.refreshToken,
    ipAddress: session.ip_address,
    userAgent: session.user_agent,
    expiresAt,
  });

  return {
    user: {
      id: user.id,
      email: user.email,
      phone: user.phone,
      fullName: user.full_name,
      roles,
    },
    ...tokens,
  };
}

async function logout({ refreshToken }) {
  if (refreshToken) {
    await sessionModel.revokeByToken(refreshToken);
  }
}

async function me(userId) {
  const user = await userModel.findById(userId);
  if (!user) {
    const err = new Error('User not found');
    err.code = 'USER_NOT_FOUND';
    err.status = 404;
    throw err;
  }

  const roles = await userModel.getUserRoles(userId);

  return {
    id: user.id,
    email: user.email,
    phone: user.phone,
    fullName: user.full_name,
    roles,
    isActive: user.is_active,
    isEmailVerified: user.is_email_verified,
    isPhoneVerified: user.is_phone_verified,
    lastLoginAt: user.last_login_at,
    createdAt: user.created_at,
  };
}

module.exports = { register, login, refresh, logout, me };