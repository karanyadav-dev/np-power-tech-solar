'use strict';

const db = require('../config/db');

// ---------- PRODUCTS ----------

async function create(data) {
  const result = await db.query(
    `INSERT INTO products (
      name, slug, category_id, brand, model, capacity, specifications,
      price, warranty_years, description, is_available, is_featured
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    RETURNING *`,
    [
      data.name, data.slug, data.categoryId || null, data.brand || null,
      data.model || null, data.capacity || null,
      data.specifications ? JSON.stringify(data.specifications) : null,
      data.price || null, data.warrantyYears || null, data.description || null,
      data.isAvailable !== false, data.isFeatured === true,
    ],
  );
  return result.rows[0];
}

async function findById(id) {
  const result = await db.query(
    `SELECT p.*, pc.name AS category_name, pc.slug AS category_slug
     FROM products p
     LEFT JOIN product_categories pc ON pc.id = p.category_id
     WHERE p.id = $1 AND p.deleted_at IS NULL`,
    [id],
  );
  return result.rows[0] || null;
}

async function findBySlug(slug) {
  const result = await db.query(
    `SELECT p.*, pc.name AS category_name
     FROM products p
     LEFT JOIN product_categories pc ON pc.id = p.category_id
     WHERE p.slug = $1 AND p.deleted_at IS NULL`,
    [slug],
  );
  return result.rows[0] || null;
}

async function list({ page = 1, limit = 20, categoryId, brand, isFeatured, isAvailable, search }) {
  const conditions = ['p.deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (categoryId) {
    conditions.push(`p.category_id = $${idx++}`);
    params.push(categoryId);
  }
  if (brand) {
    conditions.push(`LOWER(p.brand) = LOWER($${idx++})`);
    params.push(brand);
  }
  if (isFeatured !== undefined) {
    conditions.push(`p.is_featured = $${idx++}`);
    params.push(isFeatured);
  }
  if (isAvailable !== undefined) {
    conditions.push(`p.is_available = $${idx++}`);
    params.push(isAvailable);
  }
  if (search) {
    conditions.push(`(LOWER(p.name) LIKE $${idx} OR LOWER(p.brand) LIKE $${idx} OR LOWER(p.model) LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM products p WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT p.id, p.name, p.slug, p.brand, p.model, p.capacity, p.price,
            p.warranty_years, p.is_available, p.is_featured, p.created_at,
            pc.name AS category_name
     FROM products p
     LEFT JOIN product_categories pc ON pc.id = p.category_id
     WHERE ${where}
     ORDER BY p.is_featured DESC, p.created_at DESC
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
    name: 'name',
    slug: 'slug',
    categoryId: 'category_id',
    brand: 'brand',
    model: 'model',
    capacity: 'capacity',
    specifications: 'specifications',
    price: 'price',
    warrantyYears: 'warranty_years',
    description: 'description',
    isAvailable: 'is_available',
    isFeatured: 'is_featured',
  };

  const updates = [];
  const params = [];
  let idx = 1;

  for (const [key, value] of Object.entries(data)) {
    const column = fieldMap[key];
    if (column) {
      updates.push(`${column} = $${idx++}`);
      if (key === 'specifications' && value !== null) {
        params.push(JSON.stringify(value));
      } else {
        params.push(value);
      }
    }
  }

  if (updates.length === 0) return null;

  params.push(id);
  const result = await db.query(
    `UPDATE products SET ${updates.join(', ')}
     WHERE id = $${idx} AND deleted_at IS NULL
     RETURNING *`,
    params,
  );
  return result.rows[0] || null;
}

async function softDelete(id) {
  const result = await db.query(
    `UPDATE products SET deleted_at = NOW()
     WHERE id = $1 AND deleted_at IS NULL
     RETURNING id`,
    [id],
  );
  return result.rowCount > 0;
}

async function slugExists(slug) {
  const result = await db.query(
    `SELECT 1 FROM products WHERE slug = $1 LIMIT 1`,
    [slug],
  );
  return result.rowCount > 0;
}

// ---------- CATEGORIES ----------

async function createCategory(data) {
  const result = await db.query(
    `INSERT INTO product_categories (name, slug, description, display_order)
     VALUES ($1, $2, $3, $4)
     RETURNING *`,
    [data.name, data.slug, data.description || null, data.displayOrder || 0],
  );
  return result.rows[0];
}

async function listCategories() {
  const result = await db.query(
    `SELECT * FROM product_categories WHERE is_active = TRUE ORDER BY display_order ASC, name ASC`,
  );
  return result.rows;
}

async function findCategoryById(id) {
  const result = await db.query(
    `SELECT * FROM product_categories WHERE id = $1`,
    [id],
  );
  return result.rows[0] || null;
}

module.exports = {
  create,
  findById,
  findBySlug,
  list,
  update,
  softDelete,
  slugExists,
  createCategory,
  listCategories,
  findCategoryById,
};