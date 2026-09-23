'use strict';

const { Pool } = require('pg');
const { env } = require('./env');
const logger = require('./logger');

/**
 * PostgreSQL connection pool.
 * Source of truth for all persistent data.
 */

const pool = new Pool({
  host: env.db.host,
  port: env.db.port,
  database: env.db.name,
  user: env.db.user,
  password: env.db.password,
  min: env.db.poolMin,
  max: env.db.poolMax,
  ssl: env.db.ssl ? { rejectUnauthorized: false } : false,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  logger.error({ err }, '[db] Unexpected pool error');
});

/**
 * Execute a query.
 * NEVER interpolate user input directly — use $1, $2 placeholders.
 */
async function query(text, params) {
  const start = Date.now();
  try {
    const result = await pool.query(text, params);
    const duration = Date.now() - start;
    if (duration > 500) {
      logger.warn({ duration, text }, '[db] Slow query');
    }
    return result;
  } catch (err) {
    logger.error({ err, text }, '[db] Query error');
    throw err;
  }
}

/**
 * Get a client for transactions.
 */
async function getClient() {
  return pool.connect();
}

/**
 * Health check.
 */
async function healthCheck() {
  const result = await pool.query('SELECT 1 AS ok');
  return result.rows[0].ok === 1;
}

/**
 * Graceful shutdown.
 */
async function closePool() {
  await pool.end();
  logger.info('[db] Pool closed');
}

module.exports = { pool, query, getClient, healthCheck, closePool };