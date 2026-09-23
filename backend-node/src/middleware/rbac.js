'use strict';

const { forbidden } = require('../utils/response');

/**
 * Role-based access control middleware.
 */

function requireRoles(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user || !Array.isArray(req.user.roles)) {
      return forbidden(res, 'No roles found');
    }

    const hasRole = req.user.roles.some((role) => allowedRoles.includes(role));
    if (!hasRole) {
      return forbidden(res, 'Insufficient permissions');
    }

    return next();
  };
}

function requirePermission(permissionCode) {
  return async (req, res, next) => {
    if (!req.user) {
      return forbidden(res, 'Not authenticated');
    }

    if (req.user.roles.includes('super_admin')) {
      return next();
    }

    return next();
  };
}

module.exports = { requireRoles, requirePermission };