'use strict';

const db = require('../config/db');

/**
 * Lead model — parameterized queries only.
 */

async function generateLeadNumber() {
  const result = await db.query(
    `SELECT 'LD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' ||
            LPAD((COALESCE(MAX(CAST(SUBSTRING(lead_number FROM '\\d+$') AS INTEGER)), 0) + 1)::TEXT, 5, '0')
            AS next_number
     FROM leads
     WHERE lead_number LIKE 'LD-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-%'`,
  );
  return result.rows[0].next_number;
}

async function create(data) {
  const leadNumber = await generateLeadNumber();

  const result = await db.query(
    `INSERT INTO leads (
      lead_number, full_name, phone, whatsapp, email, address, city, state, pincode,
      monthly_bill, monthly_units, system_size_kw, property_type, system_type,
      battery_required, message, source_id, priority,
      utm_source, utm_medium, utm_campaign, utm_content, landing_page, referrer,
      status
    ) VALUES (
      $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14,
      $15, $16, (SELECT id FROM lead_sources WHERE code = $17), $18,
      $19, $20, $21, $22, $23, $24, 'NEW'
    )
    RETURNING *`,
    [
      leadNumber, data.fullName, data.phone, data.whatsapp || null, data.email || null,
      data.address || null, data.city || null, data.state || null, data.pincode || null,
      data.monthlyBill || null, data.monthlyUnits || null, data.systemSizeKw || null,
      data.propertyType || null, data.systemType || null,
      data.batteryRequired || false, data.message || null,
      data.sourceCode || 'website', data.priority || 'medium',
      data.utmSource || null, data.utmMedium || null, data.utmCampaign || null,
      data.utmContent || null, data.landingPage || null, data.referrer || null,
    ],
  );
  return result.rows[0];
}

async function findById(id) {
  const result = await db.query(
    `SELECT l.*, ls.display_name AS source_name,
            u.full_name AS assigned_to_name
     FROM leads l
     LEFT JOIN lead_sources ls ON ls.id = l.source_id
     LEFT JOIN users u ON u.id = l.assigned_to
     WHERE l.id = $1 AND l.deleted_at IS NULL`,
    [id],
  );
  return result.rows[0] || null;
}

async function list({ page = 1, limit = 20, status, assignedTo, pincode, search, from, to }) {
  const conditions = ['l.deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (status) {
    conditions.push(`l.status = $${idx++}`);
    params.push(status);
  }
  if (assignedTo) {
    conditions.push(`l.assigned_to = $${idx++}`);
    params.push(assignedTo);
  }
  if (pincode) {
    conditions.push(`l.pincode = $${idx++}`);
    params.push(pincode);
  }
  if (search) {
    conditions.push(`(LOWER(l.full_name) LIKE $${idx} OR l.phone LIKE $${idx} OR LOWER(l.email) LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }
  if (from) {
    conditions.push(`l.created_at >= $${idx++}`);
    params.push(from);
  }
  if (to) {
    conditions.push(`l.created_at <= $${idx++}`);
    params.push(to);
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM leads l WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT l.id, l.lead_number, l.full_name, l.phone, l.email, l.city, l.pincode,
            l.system_size_kw, l.status, l.priority, l.created_at, l.assigned_to,
            ls.display_name AS source_name,
            u.full_name AS assigned_to_name
     FROM leads l
     LEFT JOIN lead_sources ls ON ls.id = l.source_id
     LEFT JOIN users u ON u.id = l.assigned_to
     WHERE ${where}
     ORDER BY l.created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  return {
    data: result.rows,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit),
    },
  };
}

async function update(id, data) {
  const allowed = [
    'full_name', 'phone', 'whatsapp', 'email', 'address', 'city', 'state', 'pincode',
    'monthly_bill', 'monthly_units', 'system_size_kw', 'property_type', 'system_type',
    'battery_required', 'message', 'priority',
  ];

  const updates = [];
  const params = [];
  let idx = 1;

  const fieldMap = {
    fullName: 'full_name',
    phone: 'phone',
    whatsapp: 'whatsapp',
    email: 'email',
    address: 'address',
    city: 'city',
    state: 'state',
    pincode: 'pincode',
    monthlyBill: 'monthly_bill',
    monthlyUnits: 'monthly_units',
    systemSizeKw: 'system_size_kw',
    propertyType: 'property_type',
    systemType: 'system_type',
    batteryRequired: 'battery_required',
    message: 'message',
    priority: 'priority',
  };

  for (const [key, value] of Object.entries(data)) {
    const column = fieldMap[key];
    if (column && allowed.includes(column)) {
      updates.push(`${column} = $${idx++}`);
      params.push(value);
    }
  }

  if (updates.length === 0) return null;

  params.push(id);
  const result = await db.query(
    `UPDATE leads SET ${updates.join(', ')}
     WHERE id = $${idx} AND deleted_at IS NULL
     RETURNING *`,
    params,
  );
  return result.rows[0] || null;
}

async function updateStatus(id, { status, notes, lostReason }, changedBy) {
  const client = await db.getClient();
  try {
    await client.query('BEGIN');

    const current = await client.query(
      `SELECT status FROM leads WHERE id = $1 AND deleted_at IS NULL`,
      [id],
    );
    if (current.rowCount === 0) {
      await client.query('ROLLBACK');
      return null;
    }

    const fromStatus = current.rows[0].status;

    const result = await client.query(
      `UPDATE leads SET status = $1, lost_reason = COALESCE($2, lost_reason)
       WHERE id = $3 RETURNING *`,
      [status, lostReason || null, id],
    );

    await client.query(
      `INSERT INTO lead_status_history (lead_id, from_status, to_status, changed_by, notes)
       VALUES ($1, $2, $3, $4, $5)`,
      [id, fromStatus, status, changedBy, notes || null],
    );

    await client.query('COMMIT');
    return result.rows[0];
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

async function assign(id, assignedTo, assignedBy) {
  const client = await db.getClient();
  try {
    await client.query('BEGIN');

    const result = await client.query(
      `UPDATE leads SET assigned_to = $1 WHERE id = $2 AND deleted_at IS NULL RETURNING *`,
      [assignedTo, id],
    );

    if (result.rowCount === 0) {
      await client.query('ROLLBACK');
      return null;
    }

    await client.query(
      `INSERT INTO lead_assignments (lead_id, assigned_to, assigned_by)
       VALUES ($1, $2, $3)`,
      [id, assignedTo, assignedBy],
    );

    await client.query('COMMIT');
    return result.rows[0];
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

async function addFollowup(leadId, data, userId) {
  const result = await db.query(
    `INSERT INTO lead_followups (lead_id, user_id, followup_type, scheduled_at, notes, outcome)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING *`,
    [leadId, userId, data.followupType, data.scheduledAt || null, data.notes || null, data.outcome || null],
  );
  return result.rows[0];
}

async function listFollowups(leadId) {
  const result = await db.query(
    `SELECT lf.*, u.full_name AS user_name
     FROM lead_followups lf
     LEFT JOIN users u ON u.id = lf.user_id
     WHERE lf.lead_id = $1
     ORDER BY lf.created_at DESC`,
    [leadId],
  );
  return result.rows;
}

async function findDuplicate(phone, email) {
  const result = await db.query(
    `SELECT id, lead_number, full_name, status
     FROM leads
     WHERE deleted_at IS NULL
       AND (phone = $1 OR (email IS NOT NULL AND LOWER(email) = LOWER($2)))
     ORDER BY created_at DESC
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
  updateStatus,
  assign,
  addFollowup,
  listFollowups,
  findDuplicate,
};