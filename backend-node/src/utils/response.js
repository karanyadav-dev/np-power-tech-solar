'use strict';

/**
 * Consistent API response helpers.
 */

function success(res, data = null, message = 'Success', statusCode = 200) {
  return res.status(statusCode).json({
    success: true,
    message,
    data,
  });
}

function created(res, data = null, message = 'Created') {
  return success(res, data, message, 201);
}

function error(res, code, message, statusCode = 400, details = null) {
  const body = {
    success: false,
    error: { code, message },
  };
  if (details) {
    body.error.details = details;
  }
  return res.status(statusCode).json(body);
}

function notFound(res, message = 'Resource not found') {
  return error(res, 'NOT_FOUND', message, 404);
}

function unauthorized(res, message = 'Unauthorized') {
  return error(res, 'UNAUTHORIZED', message, 401);
}

function forbidden(res, message = 'Forbidden') {
  return error(res, 'FORBIDDEN', message, 403);
}

function badRequest(res, message = 'Bad request', details = null) {
  return error(res, 'BAD_REQUEST', message, 400, details);
}

function conflict(res, message = 'Conflict') {
  return error(res, 'CONFLICT', message, 409);
}

function serverError(res, message = 'Internal server error') {
  return error(res, 'INTERNAL_ERROR', message, 500);
}

module.exports = {
  success,
  created,
  error,
  notFound,
  unauthorized,
  forbidden,
  badRequest,
  conflict,
  serverError,
};