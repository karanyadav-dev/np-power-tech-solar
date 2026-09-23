'use strict';

const db = require('../config/db');

async function listRoles() {
  const result = await db.query(
    `SELECT id, name, display_name, description, is_system, created_at
     FROM roles ORDER BY name ASC`,
  );
  return result.rows;
}

async function listPermissions() {
  const result = await db.query(
    `SELECT id, code, resource, action, description
     FROM permissions ORDER BY resource ASC, action ASC`,
  );
  return result.rows;
}

async function getRolePermissions(roleName) {
  const result = await db.query(
    `SELECT p.code, p.resource, p.action
     FROM roles r
     JOIN role_permissions rp ON rp.role_id = r.id
     JOIN permissions p ON p.id = rp.permission_id
     WHERE r.name = $1
     ORDER BY p.resource, p.action`,
    [roleName],
  );
  return result.rows;
}

module.exports = { listRoles, listPermissions, getRolePermissions };