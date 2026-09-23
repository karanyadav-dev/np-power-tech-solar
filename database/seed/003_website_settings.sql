-- ==============================================================
-- Seed 003: Website Settings (Placeholders)
-- ==============================================================
-- NOTE: Actual values to be filled by Admin via Admin Panel.
-- NEVER hardcode real company info here.

INSERT INTO website_settings (key, value, value_type, category, description) VALUES
  ('company_name', 'NP POWER TECH SOLAR', 'string', 'general', 'Company display name'),
  ('company_phone', '', 'string', 'contact', 'Primary phone number'),
  ('company_email', '', 'string', 'contact', 'Primary email address'),
  ('company_whatsapp', '', 'string', 'contact', 'WhatsApp number'),
  ('company_address', '', 'string', 'contact', 'Company address'),
  ('company_gst', '', 'string', 'legal', 'GST number'),
  ('company_logo_url', '', 'string', 'branding', 'Company logo URL'),
  ('default_language', 'en', 'string', 'i18n', 'Default language (en/hi)'),
  ('supported_languages', '["en","hi"]', 'json', 'i18n', 'Supported languages'),
  ('maintenance_mode', 'false', 'boolean', 'system', 'Enable maintenance mode'),
  ('notification_email_enabled', 'true', 'boolean', 'notifications', 'Enable email notifications'),
  ('notification_whatsapp_enabled', 'false', 'boolean', 'notifications', 'Enable WhatsApp notifications'),
  ('lead_auto_assign_enabled', 'false', 'boolean', 'leads', 'Auto-assign new leads'),
  ('quotation_default_validity_days', '30', 'number', 'quotations', 'Default quotation validity in days'),
  ('gst_percentage', '18', 'number', 'tax', 'Default GST percentage')
ON CONFLICT (key) DO NOTHING;