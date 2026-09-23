'use strict';

const { createClient } = require('redis');
const { env } = require('./env');
const logger = require('./logger');

/**
 * Redis client.
 * NOT the source of truth — used only for cache, rate limit, queues, sessions.
 */

let client = null;

async function connect() {
  if (client) {
    return client;
  }

  client = createClient({
    socket: {
      host: env.redis.host,
      port: env.redis.port,
      reconnectStrategy: (retries) => Math.min(retries * 100, 3000),
    },
    password: env.redis.password,
    database: env.redis.db,
  });

  client.on('error', (err) => {
    logger.error({ err }, '[redis] Client error');
  });

  client.on('connect', () => {
    logger.info('[redis] Connected');
  });

  await client.connect();
  return client;
}

async function getClient() {
  if (!client) {
    await connect();
  }
  return client;
}

async function healthCheck() {
  if (!client) {
    return false;
  }
  try {
    const pong = await client.ping();
    return pong === 'PONG';
  } catch (err) {
    logger.error({ err }, '[redis] Health check failed');
    return false;
  }
}

async function closeRedis() {
  if (client) {
    await client.quit();
    client = null;
    logger.info('[redis] Connection closed');
  }
}

module.exports = { connect, getClient, healthCheck, closeRedis };