'use strict';

const db = require('../config/db');

async function create(data) {
  const result = await db.query(
    `INSERT INTO reviews (
      customer_id, order_id, customer_name, customer_location,
      rating, title, review_text, photo_urls, is_verified, is_published
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, FALSE, FALSE)
    RETURNING *`,
    [
      data.customerId || null,
      data.orderId || null,
      data.customerName,
      data.customerLocation || null,
      data.rating,
      data.title || null,
      data.reviewText,
      JSON.stringify(data.photoUrls || []),
    ],
  );
  return result.rows[0];
}

async function findById(id) {
  const result = await db.query(
    `SELECT * FROM reviews WHERE id = $1`,
    [id],
  );
  return result.rows[0] || null;
}

async function list({ page = 1, limit = 20, isPublished, rating }) {
  const conditions = [];
  const params = [];
  let idx = 1;

  if (isPublished !== undefined) {
    conditions.push(`is_published = $${idx++}`);
    params.push(isPublished);
  }
  if (rating) {
    conditions.push(`rating = $${idx++}`);
    params.push(rating);
  }

  const where = conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : '';
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM reviews ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT * FROM reviews ${where}
     ORDER BY is_published DESC, created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  const summaryResult = await db.query(
    `SELECT 
      COUNT(*)::INTEGER AS total,
      COALESCE(AVG(rating), 0)::NUMERIC(3,2) AS average,
      COUNT(CASE WHEN rating = 5 THEN 1 END)::INTEGER AS five_star,
      COUNT(CASE WHEN rating = 4 THEN 1 END)::INTEGER AS four_star,
      COUNT(CASE WHEN rating = 3 THEN 1 END)::INTEGER AS three_star,
      COUNT(CASE WHEN rating = 2 THEN 1 END)::INTEGER AS two_star,
      COUNT(CASE WHEN rating = 1 THEN 1 END)::INTEGER AS one_star
     FROM reviews WHERE is_published = TRUE`,
  );

  return {
    data: result.rows,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
    summary: summaryResult.rows[0],
  };
}

async function listPublic(limit = 6) {
  const result = await db.query(
    `SELECT id, customer_name, customer_location, rating, title, review_text, photo_urls, created_at
     FROM reviews
     WHERE is_published = TRUE
     ORDER BY created_at DESC
     LIMIT $1`,
    [limit],
  );
  return result.rows;
}

async function update(id, data) {
  const updates = [];
  const params = [];
  let idx = 1;

  if (data.isPublished !== undefined) {
    updates.push(`is_published = $${idx++}`);
    params.push(data.isPublished);
  }
  if (data.isVerified !== undefined) {
    updates.push(`is_verified = $${idx++}`);
    params.push(data.isVerified);
  }

  if (updates.length === 0) return null;

  params.push(id);
  const result = await db.query(
    `UPDATE reviews SET ${updates.join(', ')}
     WHERE id = $${idx}
     RETURNING *`,
    params,
  );
  return result.rows[0] || null;
}

async function softDelete(id) {
  const result = await db.query(
    `DELETE FROM reviews WHERE id = $1 RETURNING id`,
    [id],
  );
  return result.rowCount > 0;
}

module.exports = {
  create,
  findById,
  list,
  listPublic,
  update,
  softDelete,
};