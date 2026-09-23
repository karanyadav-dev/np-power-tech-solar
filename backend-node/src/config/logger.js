'use strict';

const pino = require('pino');
const { env } = require('./env');

/**
 * Structured JSON logger.
 * NEVER logs secrets, tokens, passwords.
 */

const logger = pino({
  level: env.NODE_ENV === 'production' ? 'info' : 'debug',
  redact: {
    paths: [
      'req.headers.authorization',
      'req.headers.cookie',
      'req.body.password',
      'req.body.passwordHash',
      'req.body.token',
      'req.body.refreshToken',
      '*.password',
      '*.passwordHash',
      '*.accessToken',
      '*.refreshToken',
      '*.jwt',
      '*.apiKey',
      '*.secret',
    ],
    censor: '[REDACTED]',
  },
  base: {
    service: 'np-power-tech-solar-api',
    env: env.NODE_ENV,
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

module.exports = logger;