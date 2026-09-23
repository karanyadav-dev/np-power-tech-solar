-- ==============================================================
-- Migration 005: Installations, Technicians, Warranty, AMC, Service
-- ==============================================================

-- ---------- INSTALLATIONS ----------
CREATE TABLE installations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  installation_number VARCHAR(30) UNIQUE NOT NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  technician_id UUID REFERENCES technicians(id) ON DELETE SET NULL,
  scheduled_at TIMESTAMP WITH TIME ZONE,
  started_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  status VARCHAR(30) DEFAULT 'SCHEDULED' NOT NULL CHECK (status IN (
    'SCHEDULED','ASSIGNED','MATERIAL_READY','IN_PROGRESS',
    'COMPLETED','COMMISSIONING','DONE','CANCELLED'
  )),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_installations_order_id ON installations(order_id);
CREATE INDEX idx_installations_customer_id ON installations(customer_id);
CREATE INDEX idx_installations_technician_id ON installations(technician_id);
CREATE INDEX idx_installations_status ON installations(status);

-- ---------- INSTALLATION STEPS ----------
CREATE TABLE installation_steps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  installation_id UUID NOT NULL REFERENCES installations(id) ON DELETE CASCADE,
  step_name VARCHAR(100) NOT NULL,
  step_order INTEGER DEFAULT 0,
  is_completed BOOLEAN DEFAULT FALSE NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_installation_steps_installation_id ON installation_steps(installation_id);

-- ---------- TECHNICIAN ASSIGNMENTS ----------
CREATE TABLE technician_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  technician_id UUID NOT NULL REFERENCES technicians(id) ON DELETE CASCADE,
  installation_id UUID REFERENCES installations(id) ON DELETE CASCADE,
  service_request_id UUID,
  assigned_by UUID REFERENCES users(id) ON DELETE SET NULL,
  assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  completed_at TIMESTAMP WITH TIME ZONE,
  status VARCHAR(30) DEFAULT 'ASSIGNED' NOT NULL CHECK (status IN ('ASSIGNED','IN_PROGRESS','COMPLETED','CANCELLED'))
);

CREATE INDEX idx_technician_assignments_technician_id ON technician_assignments(technician_id);
CREATE INDEX idx_technician_assignments_installation_id ON technician_assignments(installation_id);

-- ---------- INSTALLATION CHECKLISTS ----------
CREATE TABLE installation_checklists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  installation_id UUID NOT NULL REFERENCES installations(id) ON DELETE CASCADE,
  item VARCHAR(255) NOT NULL,
  is_checked BOOLEAN DEFAULT FALSE NOT NULL,
  checked_by UUID REFERENCES users(id) ON DELETE SET NULL,
  checked_at TIMESTAMP WITH TIME ZONE,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_installation_checklists_installation_id ON installation_checklists(installation_id);

-- ---------- INSTALLATION IMAGES ----------
CREATE TABLE installation_images (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  installation_id UUID NOT NULL REFERENCES installations(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  caption VARCHAR(255),
  image_type VARCHAR(30) DEFAULT 'general' CHECK (image_type IN ('general','before','after','panel','inverter','wiring')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_installation_images_installation_id ON installation_images(installation_id);

-- ---------- WARRANTIES ----------
CREATE TABLE warranties (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  warranty_number VARCHAR(30) UNIQUE NOT NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  product_name VARCHAR(255),
  serial_number VARCHAR(100),
  installation_date DATE,
  warranty_start DATE NOT NULL,
  warranty_end DATE NOT NULL,
  warranty_type VARCHAR(50) DEFAULT 'standard' CHECK (warranty_type IN ('standard','extended','manufacturer','installation')),
  documents JSONB,
  notes TEXT,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_warranties_order_id ON warranties(order_id);
CREATE INDEX idx_warranties_customer_id ON warranties(customer_id);
CREATE INDEX idx_warranties_serial_number ON warranties(serial_number);

-- ---------- AMC PLANS ----------
CREATE TABLE amc_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  price NUMERIC(10,2) NOT NULL,
  duration_months INTEGER NOT NULL,
  service_frequency INTEGER,
  features JSONB,
  is_active BOOLEAN DEFAULT TRUE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- ---------- AMC CONTRACTS ----------
CREATE TABLE amc_contracts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_number VARCHAR(30) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  amc_plan_id UUID REFERENCES amc_plans(id) ON DELETE SET NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  price NUMERIC(10,2) NOT NULL,
  renewal_date DATE,
  status VARCHAR(30) DEFAULT 'ACTIVE' NOT NULL CHECK (status IN ('ACTIVE','EXPIRED','CANCELLED','RENEWED')),
  payment_status VARCHAR(30) DEFAULT 'PENDING' CHECK (payment_status IN ('PENDING','PAID','PARTIAL')),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_amc_contracts_customer_id ON amc_contracts(customer_id);
CREATE INDEX idx_amc_contracts_status ON amc_contracts(status);
CREATE INDEX idx_amc_contracts_end_date ON amc_contracts(end_date);

-- ---------- AMC VISITS ----------
CREATE TABLE amc_visits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  contract_id UUID NOT NULL REFERENCES amc_contracts(id) ON DELETE CASCADE,
  technician_id UUID REFERENCES technicians(id) ON DELETE SET NULL,
  scheduled_at TIMESTAMP WITH TIME ZONE,
  completed_at TIMESTAMP WITH TIME ZONE,
  status VARCHAR(30) DEFAULT 'SCHEDULED' NOT NULL CHECK (status IN ('SCHEDULED','COMPLETED','MISSED','CANCELLED')),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_amc_visits_contract_id ON amc_visits(contract_id);
CREATE INDEX idx_amc_visits_technician_id ON amc_visits(technician_id);

-- ---------- SERVICE REQUESTS ----------
CREATE TABLE service_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_number VARCHAR(30) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  warranty_id UUID REFERENCES warranties(id) ON DELETE SET NULL,
  assigned_to UUID REFERENCES technicians(id) ON DELETE SET NULL,
  subject VARCHAR(255) NOT NULL,
  description TEXT,
  priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low','medium','high','urgent')),
  status VARCHAR(30) DEFAULT 'NEW' NOT NULL CHECK (status IN (
    'NEW','ASSIGNED','SCHEDULED','IN_PROGRESS','RESOLVED','CUSTOMER_CONFIRMED','CLOSED','CANCELLED'
  )),
  scheduled_at TIMESTAMP WITH TIME ZONE,
  resolved_at TIMESTAMP WITH TIME ZONE,
  resolution_notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_service_requests_customer_id ON service_requests(customer_id);
CREATE INDEX idx_service_requests_status ON service_requests(status);
CREATE INDEX idx_service_requests_assigned_to ON service_requests(assigned_to);

-- ---------- SERVICE REQUEST UPDATES ----------
CREATE TABLE service_request_updates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  service_request_id UUID NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  update_type VARCHAR(30) DEFAULT 'note' CHECK (update_type IN ('note','status_change','assignment','schedule','resolution')),
  from_status VARCHAR(30),
  to_status VARCHAR(30),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_service_request_updates_request_id ON service_request_updates(service_request_id);

-- ---------- TRIGGERS ----------
CREATE TRIGGER installations_updated_at
  BEFORE UPDATE ON installations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER warranties_updated_at
  BEFORE UPDATE ON warranties
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER amc_plans_updated_at
  BEFORE UPDATE ON amc_plans
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER amc_contracts_updated_at
  BEFORE UPDATE ON amc_contracts
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER service_requests_updated_at
  BEFORE UPDATE ON service_requests
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();