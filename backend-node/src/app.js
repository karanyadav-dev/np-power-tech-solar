'use strict';

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const pinoHttp = require('pino-http');

const logger = require('./config/logger');
const { env } = require('./config/env');

/**
 * Express application factory.
 */

const app = express();

// Trust proxy (behind Nginx/Caddy)
app.set('trust proxy', 1);

// Security headers
if (env.helmetEnabled) {
  app.use(helmet());
}

// CORS
app.use(
  cors({
    origin: env.CORS_ORIGIN.split(',').map((o) => o.trim()),
    credentials: true,
  }),
);

// Body parsers
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true, limit: '1mb' }));

// HTTP request logging
app.use(
  pinoHttp({
    logger,
    autoLogging: {
      ignore: (req) => req.url === '/health' || req.url === '/api/health',
    },
  }),
);

// Global rate limiter
const globalLimiter = rateLimit({
  windowMs: env.rateLimit.windowMs,
  max: env.rateLimit.max,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    success: false,
    error: { code: 'RATE_LIMITED', message: 'Too many requests, please try again later.' },
  },
});
app.use(globalLimiter);

// Health check (no auth)
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'np-power-tech-solar-api', time: new Date().toISOString() });
});
app.get('/api/health', (_req, res) => {
  res.json({ status: 'ok', service: 'np-power-tech-solar-api', time: new Date().toISOString() });
});

// API routes will be mounted here in later phases
// app.use('/api/v1', require('./routes'));

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: { code: 'NOT_FOUND', message: `Route ${req.method} ${req.originalUrl} not found` },
  });
});

// Central error handler
// eslint-disable-next-line no-unused-vars
app.use((err, req, res, _next) => {
  logger.error({ err, url: req.originalUrl }, '[app] Unhandled error');
  const status = err.status || 500;
  res.status(status).json({
    success: false,
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: env.NODE_ENV === 'production' ? 'Internal server error' : err.message,
    },
  });
});

module.exports = app;