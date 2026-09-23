'use strict';

const db = require('../config/db');

async function create(data) {
  const result = await db.query(
    `INSERT INTO customers (
      full_name, phone, whatsapp, email, address, city, state, pincode,
      gst_number, customer_type, notes
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    RETURNING *`,
    [
      data.fullName, data.phone, data.whatsapp || null, data.email || null,
      data.address || null, data.city || null, data.state || null, data.pincode || null,
      data.gstNumber || null, data.customerType || 'residential', data.notes || null,
    ],
  );
  return result.rows[0];
}

async function findById(id) {
  const result = await db.query(
    `SELECT * FROM customers WHERE id = $1 AND deleted_at IS NULL`,
    [id],
  );
  return result.rows[0] || null;
}

async function list({ page = 1, limit = 20, customerType, pincode, search }) {
  const conditions = ['deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (customerType) {
    conditions.push(`customer_type = $${idx++}`);
    params.push(customerType);
  }
  if (pincode) {
    conditions.push(`pincode = $${idx++}`);
    params.push(pincode);
  }
  if (search) {
    conditions.push(`(LOWER(full_name) LIKE $${idx} OR phone LIKE $${idx} OR LOWER(email) LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM customers WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT * FROM customers WHERE ${where}
     ORDER BY created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  return {
    data: result.rows,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
  };
}

async function update(id, data) {
  const fieldMap = {
    fullName: 'full_name',
    phone: 'phone',
    whatsapp: 'whatsapp',
    email: 'email',
    address: 'address',
    city: 'city',
    state: 'state',
    pincode: 'pincode',
    gstNumber: 'gst_number',
    customerType: 'customer_type',
    notes: 'notes',
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
    `UPDATE customers SET ${updates.join(', ')}
     WHERE id = $${idx} AND deleted_at IS NULL
     RETURNING *`,
    params,
  );
  return result.rows[0] || null;
}

async function softDelete(id) {
  const result = await db.query(
    `UPDATE customers SET deleted_at = NOW()
     WHERE id = $1 AND deleted_at IS NULL
     RETURNING id`,
    [id],
  );
  return result.rowCount > 0;
}

async function findByPhoneOrEmail(phone, email) {
  const result = await db.query(
    `SELECT id, full_name, phone, email FROM customers
     WHERE deleted_at IS NULL
       AND (phone = $1 OR (email IS NOT NULL AND LOWER(email) = LOWER($2)))
     LIMIT 1`,
    [phone, email || ''],
  );
  return result.rows[0] || null;
}

module.exports = {
  create,
  findById,
  list,
  update,
  softDelete,
  findByPhoneOrEmail,
};