'use strict';

const { badRequest } = require('../utils/response');

/**
 * Zod validation middleware.
 */

function validate(schemas) {
  return (req, res, next) => {
    const errors = [];

    for (const [key, schema] of Object.entries(schemas)) {
      if (!schema) continue;

      const result = schema.safeParse(req[key]);
      if (!result.success) {
        const formatted = result.error.errors.map((e) => ({
          field: e.path.join('.'),
          message: e.message,
        }));
        errors.push({ source: key, issues: formatted });
      } else {
        req[key] = result.data;
      }
    }

    if (errors.length > 0) {
      return badRequest(res, 'Validation failed', errors);
    }

    return next();
  };
}

module.exports = { validate };