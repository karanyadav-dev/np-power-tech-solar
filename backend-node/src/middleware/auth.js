'use strict';

const { verifyAccessToken } = require('../utils/jwt');
const { unauthorized } = require('../utils/response');

/**
 * JWT authentication middleware.
 */

async function authenticate(req, res, next) {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return unauthorized(res, 'Missing or invalid Authorization header');
    }

    const token = authHeader.substring(7);
    const payload = verifyAccessToken(token);
    if (!payload) {
      return unauthorized(res, 'Invalid or expired token');
    }

    req.user = {
      id: payload.sub,
      email: payload.email,
      roles: payload.roles || [],
    };

    return next();
  } catch (err) {
    return unauthorized(res, 'Authentication failed');
  }
}

async function optionalAuth(req, res, next) {
  try {
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      const payload = verifyAccessToken(token);
      if (payload) {
        req.user = {
          id: payload.sub,
          email: payload.email,
          roles: payload.roles || [],
        };
      }
    }
  } catch (err) {
    // ignore
  }
  return next();
}

module.exports = { authenticate, optionalAuth };