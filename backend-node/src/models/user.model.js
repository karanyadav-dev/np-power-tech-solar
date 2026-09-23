'use strict';

const db = require('../config/db');

/**
 * User model — all queries parameterized.
 * NEVER logs passwords.
 */

async function findById(id) {
  const result = await db.query(
    `SELECT id, email, phone, full_name, is_active,
            is_email_verified, is_phone_verified, last_login_at,
            created_at, updated_at
     FROM users
     WHERE id = $1 AND deleted_at IS NULL`,
    [id],
  );
  return result.rows[0] || null;
}

async function findByEmail(email) {
  const result = await db.query(
    `SELECT * FROM users
     WHERE LOWER(email) = LOWER($1) AND deleted_at IS NULL`,
    [email],
  );
  return result.rows[0] || null;
}

async function findByPhone(phone) {
  const result = await db.query(
    `SELECT * FROM users
     WHERE phone = $1 AND deleted_at IS NULL`,
    [phone],
  );
  return result.rows[0] || null;
}

async function create({ email, phone, passwordHash, fullName }) {
  const result = await db.query(
    `INSERT INTO users (email, phone, password_hash, full_name)
     VALUES ($1, $2, $3, $4)
     RETURNING id, email, phone, full_name, created_at`,
    [email, phone, passwordHash, fullName],
  );
  return result.rows[0];
}

async function updateLastLogin(id) {
  await db.query(
    `UPDATE users SET last_login_at = NOW() WHERE id = $1`,
    [id],
  );
}

async function getUserRoles(userId) {
  const result = await db.query(
    `SELECT r.name
     FROM user_roles ur
     JOIN roles r ON r.id = ur.role_id
     WHERE ur.user_id = $1`,
    [userId],
  );
  return result.rows.map((r) => r.name);
}

async function assignRole(userId, roleName) {
  await db.query(
    `INSERT INTO user_roles (user_id, role_id)
     SELECT $1, id FROM roles WHERE name = $2
     ON CONFLICT DO NOTHING`,
    [userId, roleName],
  );
}

async function emailExists(email) {
  const result = await db.query(
    `SELECT 1 FROM users WHERE LOWER(email) = LOWER($1) LIMIT 1`,
    [email],
  );
  return result.rowCount > 0;
}

async function phoneExists(phone) {
  const result = await db.query(
    `SELECT 1 FROM users WHERE phone = $1 LIMIT 1`,
    [phone],
  );
  return result.rowCount > 0;
}

module.exports = {
  findById,
  findByEmail,
  findByPhone,
  create,
  updateLastLogin,
  getUserRoles,
  assignRole,
  emailExists,
  phoneExists,
};