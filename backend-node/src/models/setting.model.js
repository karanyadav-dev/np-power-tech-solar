'use strict';

const db = require('../config/db');

async function getAll() {
  const result = await db.query(
    `SELECT id, key, value, value_type, category, description, updated_at
     FROM website_settings
     ORDER BY category, key`,
  );
  return result.rows;
}

async function getByCategory(category) {
  const result = await db.query(
    `SELECT id, key, value, value_type, category, description, updated_at
     FROM website_settings
     WHERE category = $1
     ORDER BY key`,
    [category],
  );
  return result.rows;
}

async function getByKey(key) {
  const result = await db.query(
    `SELECT * FROM website_settings WHERE key = $1`,
    [key],
  );
  return result.rows[0] || null;
}

async function getPublicSettings() {
  // Only return safe-to-expose settings
  const result = await db.query(
    `SELECT key, value, value_type FROM website_settings
     WHERE category IN ('general', 'contact', 'branding', 'i18n')
     ORDER BY key`,
  );
  return result.rows;
}

async function update(key, value, updatedBy = null) {
  const result = await db.query(
    `UPDATE website_settings
     SET value = $1, updated_by = $2, updated_at = NOW()
     WHERE key = $3
     RETURNING *`,
    [value, updatedBy, key],
  );
  return result.rows[0] || null;
}

async function bulkUpdate(settings, updatedBy = null) {
  const client = await db.getClient();
  try {
    await client.query('BEGIN');
    const updated = [];
    for (const s of settings) {
      const r = await client.query(
        `UPDATE website_settings
         SET value = $1, updated_by = $2, updated_at = NOW()
         WHERE key = $3
         RETURNING *`,
        [s.value, updatedBy, s.key],
      );
      if (r.rows[0]) updated.push(r.rows[0]);
    }
    await client.query('COMMIT');
    return updated;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

module.exports = {
  getAll,
  getByCategory,
  getByKey,
  getPublicSettings,
  update,
  bulkUpdate,
};