'use strict';

const app = require('./app');
const { env, validateEnv } = require('./config/env');
const logger = require('./config/logger');
const db = require('./config/db');
const redis = require('./config/redis');

/**
 * Server bootstrap.
 */

async function start() {
  try {
    validateEnv();

    try {
      await db.healthCheck();
      logger.info('[server] Database connected');
    } catch (err) {
      logger.warn({ err }, '[server] Database connection failed (continuing)');
    }

    try {
      await redis.connect();
      await redis.healthCheck();
      logger.info('[server] Redis connected');
    } catch (err) {
      logger.warn({ err }, '[server] Redis connection failed (continuing)');
    }

    const server = app.listen(env.PORT, () => {
      logger.info(`[server] Listening on port ${env.PORT} (${env.NODE_ENV})`);
    });

    const shutdown = async (signal) => {
      logger.info(`[server] Received ${signal} — shutting down`);
      server.close(async () => {
        try {
          await db.closePool();
          await redis.closeRedis();
          logger.info('[server] Shutdown complete');
          process.exit(0);
        } catch (err) {
          logger.error({ err }, '[server] Error during shutdown');
          process.exit(1);
        }
      });

      setTimeout(() => {
        logger.error('[server] Forced shutdown');
        process.exit(1);
      }, 15000);
    };

    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));

    process.on('unhandledRejection', (reason) => {
      logger.error({ reason }, '[server] Unhandled promise rejection');
    });

    process.on('uncaughtException', (err) => {
      logger.fatal({ err }, '[server] Uncaught exception');
      process.exit(1);
    });
  } catch (err) {
    logger.fatal({ err }, '[server] Failed to start');
    process.exit(1);
  }
}

start();