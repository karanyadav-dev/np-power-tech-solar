'use strict';

const db = require('../config/db');

/**
 * Quotation model — parameterized queries only.
 * NEVER logs pricing details.
 * Supports per-quotation bank details.
 */

// ---------- Generate unique quotation number ----------
async function generateQuotationNumber() {
  const result = await db.query(
    `SELECT 'QT-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' ||
            LPAD((COALESCE(MAX(CAST(SUBSTRING(quotation_number FROM '\\d+$') AS INTEGER)), 0) + 1)::TEXT, 5, '0')
            AS next_number
     FROM quotations
     WHERE quotation_number LIKE 'QT-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-%'`,
  );
  return result.rows[0].next_number;
}

// ---------- Create quotation request (WITH bank details) ----------
async function create(data) {
  const quotationNumber = await generateQuotationNumber();

  const client = await db.getClient();
  try {
    await client.query('BEGIN');

    // 1. Ensure customer exists (create if not)
    let customerId = null;
    const cust = data.customerInfo;

    const existingCustomer = await client.query(
      `SELECT id FROM customers WHERE phone = $1 AND deleted_at IS NULL LIMIT 1`,
      [cust.phone],
    );

    if (existingCustomer.rowCount > 0) {
      customerId = existingCustomer.rows[0].id;
      await client.query(
        `UPDATE customers
         SET full_name = $1, whatsapp = COALESCE($2, whatsapp),
             email = COALESCE($3, email), address = COALESCE($4, address),
             city = COALESCE($5, city), state = COALESCE($6, state),
             pincode = COALESCE($7, pincode)
         WHERE id = $8`,
        [
          cust.fullName, cust.whatsapp || null, cust.email || null,
          cust.address || null, cust.city || null, cust.state || null,
          cust.pincode || null, customerId,
        ],
      );
    } else {
      const newCust = await client.query(
        `INSERT INTO customers (full_name, phone, whatsapp, email, address, city, state, pincode, customer_type)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
         RETURNING id`,
        [
          cust.fullName, cust.phone, cust.whatsapp || null, cust.email || null,
          cust.address || null, cust.city || null, cust.state || null,
          cust.pincode || null, data.solarRequirement.customerType,
        ],
      );
      customerId = newCust.rows[0].id;
    }

    // 2. Ensure lead exists
    const existingLead = await client.query(
      `SELECT id FROM leads WHERE phone = $1 AND deleted_at IS NULL ORDER BY created_at DESC LIMIT 1`,
      [cust.phone],
    );

    let leadId;
    if (existingLead.rowCount > 0) {
      leadId = existingLead.rows[0].id;
    } else {
      const leadNumber = 'LD-' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + '-' +
        String(Math.floor(Math.random() * 99999)).padStart(5, '0');

      const newLead = await client.query(
        `INSERT INTO leads (
          lead_number, customer_id, full_name, phone, whatsapp, email,
          address, city, state, pincode, monthly_bill, monthly_units,
          system_size_kw, system_type, battery_required,
          status, priority, source_id
        ) VALUES (
          $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12,
          $13, $14, $15, 'NEW', 'high',
          (SELECT id FROM lead_sources WHERE code = 'website')
        ) RETURNING id`,
        [
          leadNumber, customerId, cust.fullName, cust.phone, cust.whatsapp || null, cust.email || null,
          cust.address || null, cust.city || null, cust.state || null, cust.pincode || null,
          data.electricityInfo.monthlyBill || null, data.electricityInfo.monthlyUnits || null,
          data.solarRequirement.systemSizeKw, data.solarRequirement.systemType,
          data.solarRequirement.batteryRequired || false,
        ],
      );
      leadId = newLead.rows[0].id;
    }

    // 3. Create quotation WITH bank details
    const bank = data.bankDetails || {};
    const quotationResult = await client.query(
      `INSERT INTO quotations (
        quotation_number, customer_id, lead_id, system_size_kw, system_type,
        bank_name, bank_account_no, bank_ifsc, bank_branch,
        status, notes
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, 'CUSTOMER_SUBMITTED', $10)
      RETURNING *`,
      [
        quotationNumber, customerId, leadId,
        data.solarRequirement.systemSizeKw,
        data.solarRequirement.systemType,
        bank.bankName || null,
        bank.bankAccountNo || null,
        bank.bankIfsc || null,
        bank.bankBranch || null,
        JSON.stringify({
          solarRequirement: data.solarRequirement,
          electricityInfo: data.electricityInfo,
          roofInfo: data.roofInfo,
          preferences: data.preferences,
        }),
      ],
    );

    const quotation = quotationResult.rows[0];

    // 4. Initial version snapshot
    await client.query(
      `INSERT INTO quotation_versions (quotation_id, version, snapshot, change_reason)
       VALUES ($1, 1, $2, 'Initial customer submission')`,
      [quotation.id, JSON.stringify({
        solarRequirement: data.solarRequirement,
        customerInfo: data.customerInfo,
        electricityInfo: data.electricityInfo,
        roofInfo: data.roofInfo,
        preferences: data.preferences,
        bankDetails: bank,
      })],
    );

    await client.query('COMMIT');
    return quotation;
  } catch (err) {
    await client.query('ROLLBACK');
    throw err;
  } finally {
    client.release();
  }
}

// ---------- Find by ID ----------
async function findById(id) {
  const result = await db.query(
    `SELECT q.*, c.full_name AS customer_name, c.phone AS customer_phone,
            c.email AS customer_email, c.address AS customer_address,
            c.city AS customer_city, c.state AS customer_state, c.pincode AS customer_pincode,
            u.full_name AS created_by_name,
            u2.full_name AS approved_by_name
     FROM quotations q
     LEFT JOIN customers c ON c.id = q.customer_id
     LEFT JOIN users u ON u.id = q.created_by
     LEFT JOIN users u2 ON u2.id = q.approved_by
     WHERE q.id = $1 AND q.deleted_at IS NULL`,
    [id],
  );
  return result.rows[0] || null;
}

// ---------- List ----------
async function list({ page = 1, limit = 20, status, customerId, leadId, search }) {
  const conditions = ['q.deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (status) {
    conditions.push(`q.status = $${idx++}`);
    params.push(status);
  }
  if (customerId) {
    conditions.push(`q.customer_id = $${idx++}`);
    params.push(customerId);
  }
  if (leadId) {
    conditions.push(`q.lead_id = $${idx++}`);
    params.push(leadId);
  }
  if (search) {
    conditions.push(`(LOWER(q.quotation_number) LIKE $${idx} OR LOWER(c.full_name) LIKE $${idx} OR c.phone LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM quotations q
     LEFT JOIN customers c ON c.id = q.customer_id
     WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT q.id, q.quotation_number, q.system_size_kw, q.system_type,
            q.final_amount, q.status, q.created_at, q.valid_until,
            c.full_name AS customer_name, c.phone AS customer_phone,
            c.city AS customer_city, c.pincode AS customer_pincode
     FROM quotations q
     LEFT JOIN customers c ON c.id = q.customer_id
     WHERE ${where}
     ORDER BY q.created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  return {
    data: result.rows,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
  };
}

// ---------- Update status ----------
async function updateStatus(id, newStatus, changedBy, notes = null) {
  const client = await db.getClient();
  try {
    await client.query('BEGIN');

    const current = await client.query(
      `SELECT status FROM quotations WHERE id = $1 AND deleted_at IS NULL`,
      [id],
    );
    if (current.rowCount === 0) {
      await client.query('ROLLBACK');
      return null;
    }

    const oldStatus = current.rows[0].status;

    const result = await client.query(
      `UPDATE quotations SET status = $1 WHERE id = $2 RETURNING *`,
      [newStatus, id],
    );

    await client.query(
      `INSERT INTO quotation_versions (quotation_id, version, snapshot, changed_by, change_reason)
       VALUES (
         $1,
         (SELECT COALESCE(MAX(version), 0) + 1 FROM quotation_versions WHERE quotation_id = $1),
         $2, $3, $4
       )`,
      [
        id,
        JSON.stringify({ status_change: { from: oldStatus, to: newStatus } }),
        changedBy,
        notes || `Status: ${oldStatus} → ${newStatus}`,
      ],
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

// ---------- Update bank details ----------
async function updateBankDetails(id, bank) {
  const result = await db.query(
    `UPDATE quotations
     SET bank_name = $1, bank_account_no = $2, bank_ifsc = $3, bank_branch = $4,
         updated_at = NOW()
     WHERE id = $5 AND deleted_at IS NULL
     RETURNING id, bank_name, bank_account_no, bank_ifsc, bank_branch`,
    [
      bank.bankName || null,
      bank.bankAccountNo || null,
      bank.bankIfsc || null,
      bank.bankBranch || null,
      id,
    ],
  );
  return result.rows[0] || null;
}

// ---------- Save admin pricing configuration ----------
async function savePricing(id, pricing, changedBy) {
  const client = await db.getClient();
  try {
    await client.query('BEGIN');

    const subtotal = pricing.items.reduce((sum, i) => sum + (i.quantity * i.unitPrice), 0);
    const discount = pricing.discount || 0;
    const gstAmount = ((subtotal - discount) * (pricing.gstPercentage || 18)) / 100;
    const subsidyAmount = pricing.subsidyAmount || 0;
    const finalAmount = subtotal - discount + gstAmount - subsidyAmount;

    await client.query(`DELETE FROM quotation_items WHERE quotation_id = $1`, [id]);

    for (const item of pricing.items) {
      await client.query(
        `INSERT INTO quotation_items (quotation_id, item_name, description, quantity, unit, unit_price, total_price)
         VALUES ($1, $2, $3, $4, $5, $6, $7)`,
        [
          id, item.itemName, item.description || null,
          item.quantity, item.unit || 'pcs',
          item.unitPrice, item.quantity * item.unitPrice,
        ],
      );
    }

    const validUntil = new Date(Date.now() + (pricing.validUntilDays || 30) * 24 * 60 * 60 * 1000);
    const result = await client.query(
      `UPDATE quotations
       SET subtotal = $1, discount = $2, gst_amount = $3, subsidy_amount = $4,
           final_amount = $5, payment_terms = $6, warranty_terms = $7,
           terms_conditions = $8, valid_until = $9, notes = $10,
           status = 'PENDING_APPROVAL'
       WHERE id = $11
       RETURNING *`,
      [
        subtotal, discount, gstAmount, subsidyAmount, finalAmount,
        pricing.paymentTerms || null, pricing.warrantyTerms || null,
        pricing.termsConditions || null, validUntil,
        pricing.adminNotes || null, id,
      ],
    );

    await client.query(
      `INSERT INTO quotation_versions (quotation_id, version, snapshot, changed_by, change_reason)
       VALUES (
         $1,
         (SELECT COALESCE(MAX(version), 0) + 1 FROM quotation_versions WHERE quotation_id = $1),
         $2, $3, $4
       )`,
      [id, JSON.stringify({ pricing, totals: { subtotal, discount, gstAmount, subsidyAmount, finalAmount } }), changedBy, 'Admin configured pricing'],
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

// ---------- Get items ----------
async function getItems(id) {
  const result = await db.query(
    `SELECT * FROM quotation_items WHERE quotation_id = $1 ORDER BY display_order, created_at`,
    [id],
  );
  return result.rows;
}

// ---------- Get versions ----------
async function getVersions(id) {
  const result = await db.query(
    `SELECT qv.*, u.full_name AS changed_by_name
     FROM quotation_versions qv
     LEFT JOIN users u ON u.id = qv.changed_by
     WHERE qv.quotation_id = $1
     ORDER BY qv.version DESC`,
    [id],
  );
  return result.rows;
}

// ---------- Customer response ----------
async function customerResponse(id, action, reason) {
  const newStatus = action === 'accept' ? 'CUSTOMER_ACCEPTED' : 'CUSTOMER_REJECTED';
  return db.query(
    `UPDATE quotations
     SET status = $1, notes = COALESCE($2, notes)
     WHERE id = $3 AND deleted_at IS NULL AND status IN ('SENT_TO_CUSTOMER', 'CUSTOMER_VIEWED')
     RETURNING *`,
    [newStatus, reason || null, id],
  );
}

module.exports = {
  create,
  findById,
  list,
  updateStatus,
  updateBankDetails,
  savePricing,
  getItems,
  getVersions,
  customerResponse,
};