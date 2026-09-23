-- ==============================================================
-- Seed 002: Lead Sources
-- ==============================================================

INSERT INTO lead_sources (code, display_name, is_active) VALUES
  ('website', 'Website', TRUE),
  ('google', 'Google', TRUE),
  ('facebook', 'Facebook', TRUE),
  ('instagram', 'Instagram', TRUE),
  ('whatsapp', 'WhatsApp', TRUE),
  ('referral', 'Referral', TRUE),
  ('walkin', 'Walk-in', TRUE),
  ('existing_customer', 'Existing Customer', TRUE),
  ('other', 'Other', TRUE)
ON CONFLICT (code) DO NOTHING;