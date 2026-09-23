-- ==============================================================
-- Migration 003: Products, Categories, Projects, Surveys
-- ==============================================================

-- ---------- PRODUCT CATEGORIES ----------
CREATE TABLE product_categories (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL,
  slug VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  display_order INTEGER DEFAULT 0,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ---------- PRODUCTS ----------
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  category_id UUID REFERENCES product_categories(id) ON DELETE SET NULL,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  brand VARCHAR(100),
  model VARCHAR(100),
  capacity VARCHAR(50),
  specifications JSONB,
  price NUMERIC(12,2),
  warranty_years INTEGER,
  description TEXT,
  is_available BOOLEAN DEFAULT TRUE NOT NULL,
  is_featured BOOLEAN DEFAULT FALSE NOT NULL,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_slug ON products(slug) WHERE deleted_at IS NULL;
CREATE INDEX idx_products_is_featured ON products(is_featured) WHERE is_featured = TRUE;

-- ---------- PRODUCT IMAGES ----------
CREATE TABLE product_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  alt_text VARCHAR(255),
  is_primary BOOLEAN DEFAULT FALSE NOT NULL,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_product_images_product_id ON product_images(product_id);

-- ---------- PRODUCT DOCUMENTS ----------
CREATE TABLE product_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  document_url TEXT NOT NULL,
  document_type VARCHAR(50),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_product_documents_product_id ON product_documents(product_id);

-- ---------- PROJECTS ----------
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  location VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  pincode VARCHAR(10),
  system_size_kw NUMERIC(6,2),
  system_type VARCHAR(50),
  installation_date DATE,
  description TEXT,
  products_used JSONB,
  customer_approval BOOLEAN DEFAULT FALSE NOT NULL,
  is_published BOOLEAN DEFAULT FALSE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_projects_slug ON projects(slug) WHERE deleted_at IS NULL;
CREATE INDEX idx_projects_is_published ON projects(is_published) WHERE is_published = TRUE;
CREATE INDEX idx_projects_pincode ON projects(pincode);

-- ---------- PROJECT IMAGES ----------
CREATE TABLE project_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  alt_text VARCHAR(255),
  image_type VARCHAR(20) DEFAULT 'gallery' CHECK (image_type IN ('before','after','gallery','other')),
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_project_images_project_id ON project_images(project_id);

-- ---------- SITE SURVEYS ----------
CREATE TABLE site_surveys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  survey_number VARCHAR(30) UNIQUE NOT NULL,
  lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  assigned_to UUID REFERENCES users(id) ON DELETE SET NULL,
  scheduled_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  roof_type VARCHAR(50),
  roof_area NUMERIC(10,2),
  available_area NUMERIC(10,2),
  shading VARCHAR(50),
  orientation VARCHAR(50),
  electricity_connection VARCHAR(50),
  meter_information TEXT,
  estimated_system_size_kw NUMERIC(6,2),
  notes TEXT,
  status VARCHAR(30) DEFAULT 'SCHEDULED' NOT NULL CHECK (status IN (
    'SCHEDULED','ASSIGNED','IN_PROGRESS','COMPLETED','CANCELLED'
  )),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_site_surveys_lead_id ON site_surveys(lead_id);
CREATE INDEX idx_site_surveys_customer_id ON site_surveys(customer_id);
CREATE INDEX idx_site_surveys_assigned_to ON site_surveys(assigned_to);
CREATE INDEX idx_site_surveys_status ON site_surveys(status);

-- ---------- SURVEY IMAGES ----------
CREATE TABLE survey_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  survey_id UUID NOT NULL REFERENCES site_surveys(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  caption VARCHAR(255),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_survey_images_survey_id ON survey_images(survey_id);

-- ---------- TRIGGERS ----------
CREATE TRIGGER product_categories_updated_at
  BEFORE UPDATE ON product_categories
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER projects_updated_at
  BEFORE UPDATE ON projects
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER site_surveys_updated_at
  BEFORE UPDATE ON site_surveys
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();