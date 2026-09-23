-- ==============================================================
-- Migration 006: Content, Reviews, Blog, Notifications, Pincode,
--                 Subsidy, Website Settings, Analytics
-- ==============================================================

-- ---------- REVIEWS ----------
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  customer_name VARCHAR(255) NOT NULL,
  customer_location VARCHAR(255),
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  title VARCHAR(255),
  review_text TEXT,
  is_verified BOOLEAN DEFAULT FALSE NOT NULL,
  is_published BOOLEAN DEFAULT FALSE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_reviews_published ON reviews(is_published) WHERE is_published = TRUE;
CREATE INDEX idx_reviews_rating ON reviews(rating);

-- ---------- BLOG CATEGORIES ----------
CREATE TABLE blog_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ---------- BLOG POSTS ----------
CREATE TABLE blog_posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id UUID REFERENCES blog_categories(id) ON DELETE SET NULL,
  author_id UUID REFERENCES users(id) ON DELETE SET NULL,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  excerpt TEXT,
  content TEXT NOT NULL,
  featured_image TEXT,
  meta_title VARCHAR(255),
  meta_description TEXT,
  tags TEXT[],
  status VARCHAR(30) DEFAULT 'DRAFT' NOT NULL CHECK (status IN ('DRAFT','PUBLISHED','ARCHIVED')),
  published_at TIMESTAMP WITH TIME ZONE,
  view_count INTEGER DEFAULT 0 NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_status ON blog_posts(status);
CREATE INDEX idx_blog_posts_published_at ON blog_posts(published_at DESC);

-- ---------- DOCUMENTS ----------
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  quotation_id UUID REFERENCES quotations(id) ON DELETE SET NULL,
  survey_id UUID REFERENCES site_surveys(id) ON DELETE SET NULL,
  warranty_id UUID REFERENCES warranties(id) ON DELETE SET NULL,
  document_type VARCHAR(50) NOT NULL CHECK (document_type IN (
    'electricity_bill','site_photo','quotation_pdf','invoice_pdf',
    'survey_report','installation_document','warranty_document','kyc','other'
  )),
  title VARCHAR(255) NOT NULL,
  file_url TEXT NOT NULL,
  file_size INTEGER,
  mime_type VARCHAR(100),
  uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_documents_customer_id ON documents(customer_id);
CREATE INDEX idx_documents_type ON documents(document_type);

-- ---------- NOTIFICATION TEMPLATES ----------
CREATE TABLE notification_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code VARCHAR(100) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  channel VARCHAR(20) NOT NULL CHECK (channel IN ('email','whatsapp','sms','inapp')),
  subject VARCHAR(255),
  body TEXT NOT NULL,
  variables JSONB,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ---------- NOTIFICATIONS ----------
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
  template_code VARCHAR(100),
  channel VARCHAR(20) DEFAULT 'inapp' CHECK (channel IN ('email','whatsapp','sms','inapp')),
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT FALSE NOT NULL,
  read_at TIMESTAMP WITH TIME ZONE,
  metadata JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_customer_id ON notifications(customer_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read) WHERE is_read = FALSE;

-- ---------- PINCODES (Serviceability) ----------
CREATE TABLE pincodes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pincode VARCHAR(10) UNIQUE NOT NULL,
  city VARCHAR(100),
  district VARCHAR(100),
  state VARCHAR(100),
  service_available BOOLEAN DEFAULT FALSE NOT NULL,
  installation_available BOOLEAN DEFAULT FALSE NOT NULL,
  survey_available BOOLEAN DEFAULT FALSE NOT NULL,
  delivery_available BOOLEAN DEFAULT FALSE NOT NULL,
  assigned_team VARCHAR(255),
  status VARCHAR(30) DEFAULT 'CONTACT_REQUIRED' NOT NULL CHECK (status IN (
    'SERVICE_AVAILABLE','SERVICE_NOT_AVAILABLE','CONTACT_REQUIRED'
  )),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_pincodes_pincode ON pincodes(pincode);
CREATE INDEX idx_pincodes_status ON pincodes(status);
CREATE INDEX idx_pincodes_state ON pincodes(state);

-- ---------- SERVICE AREAS ----------
CREATE TABLE service_areas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  state VARCHAR(100),
  district VARCHAR(100),
  city VARCHAR(100),
  pincodes TEXT[],
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ---------- SUBSIDY CONFIGURATIONS ----------
CREATE TABLE subsidy_configurations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  state VARCHAR(100) NOT NULL,
  scheme_name VARCHAR(255) NOT NULL,
  description TEXT,
  eligibility TEXT,
  effective_from DATE,
  effective_to DATE,
  source_reference TEXT,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_subsidy_configurations_state ON subsidy_configurations(state);
CREATE INDEX idx_subsidy_configurations_active ON subsidy_configurations(is_active);

-- ---------- SUBSIDY SLABS ----------
CREATE TABLE subsidy_slabs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  configuration_id UUID NOT NULL REFERENCES subsidy_configurations(id) ON DELETE CASCADE,
  min_capacity_kw NUMERIC(6,2) NOT NULL,
  max_capacity_kw NUMERIC(6,2),
  subsidy_amount NUMERIC(12,2),
  subsidy_percentage NUMERIC(5,2),
  max_subsidy NUMERIC(12,2),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_subsidy_slabs_config_id ON subsidy_slabs(configuration_id);

-- ---------- WEBSITE SETTINGS ----------
CREATE TABLE website_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key VARCHAR(100) UNIQUE NOT NULL,
  value TEXT,
  value_type VARCHAR(20) DEFAULT 'string' CHECK (value_type IN ('string','number','boolean','json')),
  category VARCHAR(50),
  description TEXT,
  updated_by UUID REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_website_settings_key ON website_settings(key);
CREATE INDEX idx_website_settings_category ON website_settings(category);

-- ---------- SEO METADATA ----------
CREATE TABLE seo_metadata (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page_path VARCHAR(255) UNIQUE NOT NULL,
  title VARCHAR(255),
  meta_description TEXT,
  og_title VARCHAR(255),
  og_description TEXT,
  og_image TEXT,
  canonical_url TEXT,
  structured_data JSONB,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_seo_metadata_path ON seo_metadata(page_path);

-- ---------- ANALYTICS EVENTS ----------
CREATE TABLE analytics_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type VARCHAR(100) NOT NULL,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
  session_id VARCHAR(255),
  page_path TEXT,
  metadata JSONB,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_analytics_events_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_events_created_at ON analytics_events(created_at DESC);
CREATE INDEX idx_analytics_events_lead_id ON analytics_events(lead_id);

-- ---------- UTM ATTRIBUTIONS ----------
CREATE TABLE utm_attributions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  utm_source VARCHAR(100),
  utm_medium VARCHAR(100),
  utm_campaign VARCHAR(100),
  utm_content VARCHAR(100),
  utm_term VARCHAR(100),
  landing_page TEXT,
  referrer TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_utm_attributions_lead_id ON utm_attributions(lead_id);

-- ---------- PAGE VIEWS ----------
CREATE TABLE page_views (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  page_path TEXT NOT NULL,
  session_id VARCHAR(255),
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  referrer TEXT,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_page_views_path ON page_views(page_path);
CREATE INDEX idx_page_views_created_at ON page_views(created_at DESC);

-- ---------- TRIGGERS ----------
CREATE TRIGGER reviews_updated_at
  BEFORE UPDATE ON reviews
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER blog_posts_updated_at
  BEFORE UPDATE ON blog_posts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER notification_templates_updated_at
  BEFORE UPDATE ON notification_templates
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER pincodes_updated_at
  BEFORE UPDATE ON pincodes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER subsidy_configurations_updated_at
  BEFORE UPDATE ON subsidy_configurations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER website_settings_updated_at
  BEFORE UPDATE ON website_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER seo_metadata_updated_at
  BEFORE UPDATE ON seo_metadata
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();