'use strict';

const crypto = require('crypto');
const db = require('../config/db');

function hashToken(token) {
  return crypto.createHash('sha256').update(token).digest('hex');
}

async function create({ userId, refreshToken, ipAddress, userAgent, expiresAt }) {
  const tokenHash = hashToken(refreshToken);
  const result = await db.query(
    `INSERT INTO sessions (user_id, refresh_token_hash, ip_address, user_agent, expires_at)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING id, expires_at`,
    [userId, tokenHash, ipAddress || null, userAgent || null, expiresAt],
  );
  return result.rows[0];
}

async function findValidByToken(refreshToken) {
  const tokenHash = hashToken(refreshToken);
  const result = await db.query(
    `SELECT id, user_id, expires_at, revoked_at
     FROM sessions
     WHERE refresh_token_hash = $1
       AND revoked_at IS NULL
       AND expires_at > NOW()`,
    [tokenHash],
  );
  return result.rows[0] || null;
}

async function revoke(id) {
  await db.query(
    `UPDATE sessions SET revoked_at = NOW() WHERE id = $1`,
    [id],
  );
}

async function revokeByToken(refreshToken) {
  const tokenHash = hashToken(refreshToken);
  await db.query(
    `UPDATE sessions SET revoked_at = NOW()
     WHERE refresh_token_hash = $1 AND revoked_at IS NULL`,
    [tokenHash],
  );
}

async function revokeAllForUser(userId) {
  await db.query(
    `UPDATE sessions SET revoked_at = NOW()
     WHERE user_id = $1 AND revoked_at IS NULL`,
    [userId],
  );
}

module.exports = {
  create,
  findValidByToken,
  revoke,
  revokeByToken,
  revokeAllForUser,
};