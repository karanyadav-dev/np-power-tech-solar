-- ==============================================================
-- Seed 001: Roles and Permissions
-- ==============================================================

-- ---------- ROLES ----------
INSERT INTO roles (name, display_name, description, is_system) VALUES
  ('super_admin', 'Super Admin', 'Full system access including role management', TRUE),
  ('admin', 'Admin', 'All business modules access', TRUE),
  ('sales_manager', 'Sales Manager', 'Manage leads, CRM, quotes, orders', TRUE),
  ('sales_staff', 'Sales Staff', 'Own leads and quotes only', TRUE),
  ('technician', 'Technician', 'Assigned jobs and service tickets only', TRUE),
  ('accountant', 'Accountant', 'Payments, invoices, reports', TRUE),
  ('support_staff', 'Support Staff', 'Service tickets and customer read access', TRUE),
  ('content_manager', 'Content Manager', 'Blog, SEO, reviews, projects content', TRUE),
  ('customer', 'Customer', 'Own records only (customer portal)', TRUE)
ON CONFLICT (name) DO NOTHING;

-- ---------- PERMISSIONS ----------
INSERT INTO permissions (code, resource, action, description) VALUES
  -- Users
  ('users.read', 'users', 'read', 'View users'),
  ('users.create', 'users', 'create', 'Create users'),
  ('users.update', 'users', 'update', 'Update users'),
  ('users.delete', 'users', 'delete', 'Delete users'),

  -- Roles
  ('roles.read', 'roles', 'read', 'View roles'),
  ('roles.manage', 'roles', 'manage', 'Manage roles and permissions'),

  -- Customers
  ('customers.read', 'customers', 'read', 'View customers'),
  ('customers.create', 'customers', 'create', 'Create customers'),
  ('customers.update', 'customers', 'update', 'Update customers'),
  ('customers.delete', 'customers', 'delete', 'Delete customers'),

  -- Leads
  ('leads.read', 'leads', 'read', 'View leads'),
  ('leads.create', 'leads', 'create', 'Create leads'),
  ('leads.update', 'leads', 'update', 'Update leads'),
  ('leads.assign', 'leads', 'assign', 'Assign leads'),
  ('leads.delete', 'leads', 'delete', 'Delete leads'),

  -- Products
  ('products.read', 'products', 'read', 'View products'),
  ('products.create', 'products', 'create', 'Create products'),
  ('products.update', 'products', 'update', 'Update products'),
  ('products.delete', 'products', 'delete', 'Delete products'),

  -- Projects
  ('projects.read', 'projects', 'read', 'View projects'),
  ('projects.create', 'projects', 'create', 'Create projects'),
  ('projects.update', 'projects', 'update', 'Update projects'),
  ('projects.publish', 'projects', 'publish', 'Publish projects'),
  ('projects.delete', 'projects', 'delete', 'Delete projects'),

  -- Surveys
  ('surveys.read', 'surveys', 'read', 'View surveys'),
  ('surveys.create', 'surveys', 'create', 'Create surveys'),
  ('surveys.assign', 'surveys', 'assign', 'Assign surveys'),
  ('surveys.update', 'surveys', 'update', 'Update surveys'),

  -- Quotations
  ('quotes.read', 'quotes', 'read', 'View quotations'),
  ('quotes.create', 'quotes', 'create', 'Create quotations'),
  ('quotes.update', 'quotes', 'update', 'Update quotations'),
  ('quotes.approve', 'quotes', 'approve', 'Approve quotations'),
  ('quotes.send', 'quotes', 'send', 'Send quotations'),

  -- Orders
  ('orders.read', 'orders', 'read', 'View orders'),
  ('orders.create', 'orders', 'create', 'Create orders'),
  ('orders.update', 'orders', 'update', 'Update orders'),

  -- Payments
  ('payments.read', 'payments', 'read', 'View payments'),
  ('payments.verify', 'payments', 'verify', 'Verify payments'),
  ('payments.refund', 'payments', 'refund', 'Process refunds'),

  -- Invoices
  ('invoices.read', 'invoices', 'read', 'View invoices'),
  ('invoices.create', 'invoices', 'create', 'Create invoices'),
  ('invoices.send', 'invoices', 'send', 'Send invoices'),

  -- Installations
  ('installations.read', 'installations', 'read', 'View installations'),
  ('installations.schedule', 'installations', 'schedule', 'Schedule installations'),
  ('installations.assign', 'installations', 'assign', 'Assign technicians'),
  ('installations.update', 'installations', 'update', 'Update installation status'),

  -- Technicians
  ('technicians.read', 'technicians', 'read', 'View technicians'),
  ('technicians.create', 'technicians', 'create', 'Create technicians'),
  ('technicians.update', 'technicians', 'update', 'Update technicians'),

  -- Warranty
  ('warranty.read', 'warranty', 'read', 'View warranties'),
  ('warranty.create', 'warranty', 'create', 'Create warranties'),

  -- AMC
  ('amc.read', 'amc', 'read', 'View AMC contracts'),
  ('amc.create', 'amc', 'create', 'Create AMC contracts'),
  ('amc.renew', 'amc', 'renew', 'Renew AMC contracts'),

  -- Service
  ('service.read', 'service', 'read', 'View service requests'),
  ('service.create', 'service', 'create', 'Create service requests'),
  ('service.assign', 'service', 'assign', 'Assign service requests'),
  ('service.resolve', 'service', 'resolve', 'Resolve service requests'),

  -- Reviews
  ('reviews.read', 'reviews', 'read', 'View reviews'),
  ('reviews.moderate', 'reviews', 'moderate', 'Moderate reviews'),

  -- Blog
  ('blog.read', 'blog', 'read', 'View blog'),
  ('blog.create', 'blog', 'create', 'Create blog posts'),
  ('blog.update', 'blog', 'update', 'Update blog posts'),
  ('blog.publish', 'blog', 'publish', 'Publish blog posts'),

  -- SEO
  ('seo.read', 'seo', 'read', 'View SEO settings'),
  ('seo.manage', 'seo', 'manage', 'Manage SEO'),

  -- Subsidy
  ('subsidy.read', 'subsidy', 'read', 'View subsidy configs'),
  ('subsidy.manage', 'subsidy', 'manage', 'Manage subsidy configs'),

  -- Pincode
  ('pincode.read', 'pincode', 'read', 'View pincodes'),
  ('pincode.manage', 'pincode', 'manage', 'Manage pincodes'),

  -- Notifications
  ('notifications.read', 'notifications', 'read', 'View notifications'),
  ('notifications.send', 'notifications', 'send', 'Send notifications'),

  -- Analytics
  ('analytics.read', 'analytics', 'read', 'View analytics'),

  -- Settings
  ('settings.read', 'settings', 'read', 'View settings'),
  ('settings.manage', 'settings', 'manage', 'Manage settings'),

  -- Audit Logs
  ('audit_logs.read', 'audit_logs', 'read', 'View audit logs')
ON CONFLICT (code) DO NOTHING;

-- ---------- ROLE-PERMISSION MAPPINGS ----------

-- Super Admin: ALL permissions
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'super_admin'
ON CONFLICT DO NOTHING;

-- Admin: All except roles.manage
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'admin' AND p.code != 'roles.manage'
ON CONFLICT DO NOTHING;

-- Sales Manager
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'sales_manager'
  AND p.resource IN ('leads', 'customers', 'quotes', 'orders', 'surveys', 'products', 'projects')
ON CONFLICT DO NOTHING;

-- Sales Staff
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'sales_staff'
  AND p.code IN (
    'leads.read', 'leads.create', 'leads.update',
    'customers.read', 'customers.create',
    'quotes.read', 'quotes.create',
    'products.read', 'projects.read'
  )
ON CONFLICT DO NOTHING;

-- Technician
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'technician'
  AND p.code IN (
    'installations.read', 'installations.update',
    'service.read', 'service.resolve',
    'customers.read'
  )
ON CONFLICT DO NOTHING;

-- Accountant
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'accountant'
  AND p.resource IN ('payments', 'invoices', 'orders', 'customers', 'analytics')
ON CONFLICT DO NOTHING;

-- Support Staff
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'support_staff'
  AND p.code IN (
    'service.read', 'service.create', 'service.assign',
    'customers.read', 'leads.read', 'orders.read'
  )
ON CONFLICT DO NOTHING;

-- Content Manager
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'content_manager'
  AND p.resource IN ('blog', 'reviews', 'seo', 'projects')
ON CONFLICT DO NOTHING;

-- Customer (minimal — own records only, enforced by backend)
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r CROSS JOIN permissions p
WHERE r.name = 'customer'
  AND p.code IN ('quotes.read', 'orders.read', 'payments.read', 'invoices.read', 'warranty.read', 'amc.read', 'service.create', 'service.read')
ON CONFLICT DO NOTHING;