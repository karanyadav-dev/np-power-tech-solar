'use strict';

const { badRequest } = require('../utils/response');

/**
 * Zod validation middleware.
 * Usage: validate({ body: schema, query: schema, params: schema })
 *
 * Note: In Express 5, req.query and req.params are read-only getters.
 * We use Object.defineProperty to override them safely.
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
        continue;
      }

      // Safe assignment — Express 5 compat
      if (key === 'body') {
        req.body = result.data;
      } else {
        // For query/params, override the getter
        Object.defineProperty(req, key, {
          value: result.data,
          writable: true,
          configurable: true,
          enumerable: true,
        });
      }
    }

    if (errors.length > 0) {
      return badRequest(res, 'Validation failed', errors);
    }

    return next();
  };
}

module.exports = { validate };