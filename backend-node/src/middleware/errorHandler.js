'use strict';

const logger = require('../config/logger');
const { env } = require('../config/env');
const { serverError, notFound } = require('../utils/response');

/**
 * 404 handler.
 */
function notFoundHandler(req, res) {
  return notFound(res, `Route ${req.method} ${req.originalUrl} not found`);
}

/**
 * Central error handler.
 */
// eslint-disable-next-line no-unused-vars
function errorHandler(err, req, res, _next) {
  logger.error({ err, url: req.originalUrl }, '[errorHandler] Unhandled error');

  const status = err.status || err.statusCode || 500;

  if (status === 500) {
    return serverError(
      res,
      env.NODE_ENV === 'production' ? 'Internal server error' : err.message,
    );
  }

  return res.status(status).json({
    success: false,
    error: {
      code: err.code || 'ERROR',
      message: env.NODE_ENV === 'production' ? 'Request failed' : err.message,
    },
  });
}

module.exports = { notFoundHandler, errorHandler };