'use strict';

const db = require('../config/db');

async function create(data) {
  const result = await db.query(
    `INSERT INTO projects (
      project_name, slug, location, city, state, pincode,
      system_size_kw, system_type, installation_date, description,
      customer_approval, is_published
    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
    RETURNING *`,
    [
      data.projectName, data.slug, data.location || null,
      data.city || null, data.state || null, data.pincode || null,
      data.systemSizeKw || null, data.systemType || null,
      data.installationDate || null, data.description || null,
      data.customerApproval || false, data.isPublished || false,
    ],
  );
  return result.rows[0];
}

async function findById(id) {
  const result = await db.query(
    `SELECT * FROM projects WHERE id = $1 AND deleted_at IS NULL`,
    [id],
  );
  if (!result.rows[0]) return null;

  const project = result.rows[0];
  const imagesResult = await db.query(
    `SELECT id, image_url, alt_text, image_type, display_order
     FROM project_images
     WHERE project_id = $1
     ORDER BY display_order, created_at`,
    [id],
  );
  project.images = imagesResult.rows;
  return project;
}

async function findBySlug(slug) {
  const result = await db.query(
    `SELECT * FROM projects WHERE slug = $1 AND deleted_at IS NULL`,
    [slug],
  );
  return result.rows[0] || null;
}

async function list({ page = 1, limit = 20, isPublished, city, search }) {
  const conditions = ['deleted_at IS NULL'];
  const params = [];
  let idx = 1;

  if (isPublished !== undefined) {
    conditions.push(`is_published = $${idx++}`);
    params.push(isPublished);
  }
  if (city) {
    conditions.push(`LOWER(city) = LOWER($${idx++})`);
    params.push(city);
  }
  if (search) {
    conditions.push(`(LOWER(project_name) LIKE $${idx} OR LOWER(description) LIKE $${idx})`);
    params.push(`%${search.toLowerCase()}%`);
    idx++;
  }

  const where = conditions.join(' AND ');
  const offset = (page - 1) * limit;

  const countResult = await db.query(
    `SELECT COUNT(*)::INTEGER AS total FROM projects WHERE ${where}`,
    params,
  );
  const total = countResult.rows[0].total;

  const result = await db.query(
    `SELECT * FROM projects WHERE ${where}
     ORDER BY is_published DESC, created_at DESC
     LIMIT $${idx++} OFFSET $${idx++}`,
    [...params, limit, offset],
  );

  // Attach images
  for (const p of result.rows) {
    const imgs = await db.query(
      `SELECT image_url FROM project_images WHERE project_id = $1 ORDER BY display_order LIMIT 3`,
      [p.id],
    );
    p.images = imgs.rows.map((i) => i.image_url);
  }

  return {
    data: result.rows,
    pagination: { page, limit, total, pages: Math.ceil(total / limit) },
  };
}

async function update(id, data) {
  const fieldMap = {
    projectName: 'project_name',
    slug: 'slug',
    location: 'location',
    city: 'city',
    state: 'state',
    pincode: 'pincode',
    systemSizeKw: 'system_size_kw',
    systemType: 'system_type',
    installationDate: 'installation_date',
    description: 'description',
    customerApproval: 'customer_approval',
    isPublished: 'is_published',
  };

  const updates = [];
  const params = [];
  let idx = 1;

  for (const [key, value] of Object.entries(data)) {
    const column = fieldMap[key];
    if (column !== undefined) {
      updates.push(`${column} = $${idx++}`);
      params.push(value);
    }
  }

  if (updates.length === 0) return null;

  params.push(id);
  const result = await db.query(
    `UPDATE projects SET ${updates.join(', ')}
     WHERE id = $${idx} AND deleted_at IS NULL
     RETURNING *`,
    params,
  );
  return result.rows[0] || null;
}

async function addImage(projectId, imageUrl, altText = null, imageType = 'gallery', displayOrder = 0) {
  const result = await db.query(
    `INSERT INTO project_images (project_id, image_url, alt_text, image_type, display_order)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING *`,
    [projectId, imageUrl, altText, imageType, displayOrder],
  );
  return result.rows[0];
}

async function deleteImage(imageId) {
  const result = await db.query(
    `DELETE FROM project_images WHERE id = $1 RETURNING id`,
    [imageId],
  );
  return result.rowCount > 0;
}

async function softDelete(id) {
  const result = await db.query(
    `UPDATE projects SET deleted_at = NOW() WHERE id = $1 AND deleted_at IS NULL RETURNING id`,
    [id],
  );
  return result.rowCount > 0;
}

module.exports = {
  create,
  findById,
  findBySlug,
  list,
  update,
  addImage,
  deleteImage,
  softDelete,
};