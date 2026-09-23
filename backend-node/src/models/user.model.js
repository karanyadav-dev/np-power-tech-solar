'use strict';

const db = require('../config/db');

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
    `SELECT * FROM users WHERE phone = $1 AND deleted_at IS NULL`,
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
  await db.query(`UPDATE users SET last_login_at = NOW() WHERE id = $1`, [id]);
}

async function getUserRoles(userId) {
  const result = await db.query(
    `SELECT r.name FROM user_roles ur
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

async function removeRole(userId, roleName) {
  await db.query(
    `DELETE FROM user_roles
     WHERE user_id = $1
       AND role_id = (SELECT id FROM roles WHERE name = $2)`,
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

async function list({ page = 1, limit = 20, search, isActive, roleName }) {
  const conditions = ['u.deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (search) {
    conditions.push(`(LOWER(u.full_name) LIKE $${idx} OR u.phone LIKE $${idx} OR LOWER(u.email) LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }
  if (isActive !== undefined) {
    conditions.push(`u.is_active = $${idx++}`);
    params.push(isActive);
  }

  let joinClause = '';
  if (roleName) {
    joinClause = 'JOIN user_roles ur ON ur.user_id = u.id JOIN roles r ON r.id = ur.role_id';
    conditions.push(`r.name = $${idx++}`);
    params.push(roleName);
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(DISTINCT u.id)::INTEGER AS total FROM users u ${joinClause} WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT DISTINCT u.id, u.email, u.phone, u.full_name, u.is_active,
            u.is_email_verified, u.is_phone_verified, u.last_login_at, u.created_at
     FROM users u ${joinClause}
     WHERE ${where}
     ORDER BY u.created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  for (const user of result.rows) {
    user.roles = await getUserRoles(user.id);
  }

  return {
    data: result.rows,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
  };
}

async function update(id, data) {
  const fieldMap = {
    fullName: 'full_name',
    phone: 'phone',
    isActive: 'is_active',
    isEmailVerified: 'is_email_verified',
    isPhoneVerified: 'is_phone_verified',
  };

  const updates = [];
  const params = [];
  let idx = 1;

  for (const [key, value] of Object.entries(data)) {
    const column = fieldMap[key];
    if (column) {
      updates.push(`${column} = $${idx++}`);
      params.push(value);
    }
  }

  if (updates.length === 0) return null;

  params.push(id);
  const result = await db.query(
    `UPDATE users SET ${updates.join(', ')}
     WHERE id = $${idx} AND deleted_at IS NULL
     RETURNING id, email, phone, full_name, is_active, is_email_verified, is_phone_verified, created_at, updated_at`,
    params,
  );
  return result.rows[0] || null;
}

async function softDelete(id) {
  const result = await db.query(
    `UPDATE users SET deleted_at = NOW() WHERE id = $1 AND deleted_at IS NULL RETURNING id`,
    [id],
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
  removeRole,
  emailExists,
  phoneExists,
  list,
  update,
  softDelete,
};