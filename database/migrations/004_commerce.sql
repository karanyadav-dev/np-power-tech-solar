-- ==============================================================
-- Migration 004: Quotations, Orders, Payments, Invoices
-- ==============================================================

-- ---------- QUOTATIONS ----------
CREATE TABLE quotations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  quotation_number VARCHAR(30) UNIQUE NOT NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
  survey_id UUID REFERENCES site_surveys(id) ON DELETE SET NULL,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  approved_by UUID REFERENCES users(id) ON DELETE SET NULL,
  system_size_kw NUMERIC(6,2),
  system_type VARCHAR(50),
  subtotal NUMERIC(12,2) DEFAULT 0 NOT NULL,
  discount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  gst_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  subsidy_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  final_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  payment_terms TEXT,
  warranty_terms TEXT,
  terms_conditions TEXT,
  valid_until DATE,
  version INTEGER DEFAULT 1 NOT NULL,
  is_latest BOOLEAN DEFAULT TRUE NOT NULL,
  status VARCHAR(30) DEFAULT 'DRAFT' NOT NULL CHECK (status IN (
    'DRAFT','CUSTOMER_SUBMITTED','ADMIN_REVIEW','INFORMATION_REQUIRED',
    'VERIFIED','PRICING_CONFIGURED','PENDING_APPROVAL','APPROVED',
    'PDF_GENERATED','SENT_TO_CUSTOMER','CUSTOMER_VIEWED',
    'CUSTOMER_ACCEPTED','CUSTOMER_REJECTED','CONVERTED_TO_ORDER','EXPIRED'
  )),
  pdf_url TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_quotations_number ON quotations(quotation_number) WHERE deleted_at IS NULL;
CREATE INDEX idx_quotations_customer_id ON quotations(customer_id);
CREATE INDEX idx_quotations_lead_id ON quotations(lead_id);
CREATE INDEX idx_quotations_status ON quotations(status);
CREATE INDEX idx_quotations_created_at ON quotations(created_at DESC);

-- ---------- QUOTATION ITEMS ----------
CREATE TABLE quotation_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  quotation_id UUID NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  item_name VARCHAR(255) NOT NULL,
  description TEXT,
  quantity NUMERIC(10,2) DEFAULT 1 NOT NULL,
  unit VARCHAR(20) DEFAULT 'pcs',
  unit_price NUMERIC(12,2) NOT NULL,
  total_price NUMERIC(12,2) NOT NULL,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_quotation_items_quotation_id ON quotation_items(quotation_id);

-- ---------- QUOTATION VERSIONS ----------
CREATE TABLE quotation_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  quotation_id UUID NOT NULL REFERENCES quotations(id) ON DELETE CASCADE,
  version INTEGER NOT NULL,
  snapshot JSONB NOT NULL,
  changed_by UUID REFERENCES users(id) ON DELETE SET NULL,
  change_reason TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_quotation_versions_quotation_id ON quotation_versions(quotation_id);

-- ---------- ORDERS ----------
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number VARCHAR(30) UNIQUE NOT NULL,
  quotation_id UUID REFERENCES quotations(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  created_by UUID REFERENCES users(id) ON DELETE SET NULL,
  total_amount NUMERIC(12,2) NOT NULL,
  paid_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  balance_amount NUMERIC(12,2) NOT NULL,
  status VARCHAR(30) DEFAULT 'PENDING_PAYMENT' NOT NULL CHECK (status IN (
    'PENDING_PAYMENT','PAYMENT_RECEIVED','MATERIAL_PREPARATION',
    'INSTALLATION_SCHEDULED','INSTALLATION_STARTED','INSTALLATION_COMPLETED',
    'COMMISSIONING','COMPLETED','CANCELLED'
  )),
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_orders_number ON orders(order_number) WHERE deleted_at IS NULL;
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_quotation_id ON orders(quotation_id);
CREATE INDEX idx_orders_status ON orders(status);

-- ---------- ORDER ITEMS ----------
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id) ON DELETE SET NULL,
  item_name VARCHAR(255) NOT NULL,
  description TEXT,
  quantity NUMERIC(10,2) DEFAULT 1 NOT NULL,
  unit VARCHAR(20) DEFAULT 'pcs',
  unit_price NUMERIC(12,2) NOT NULL,
  total_price NUMERIC(12,2) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- ---------- PAYMENTS ----------
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  payment_number VARCHAR(30) UNIQUE NOT NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  amount NUMERIC(12,2) NOT NULL,
  gateway VARCHAR(50),
  transaction_id VARCHAR(255),
  payment_method VARCHAR(50),
  payment_status VARCHAR(30) DEFAULT 'PENDING' NOT NULL CHECK (payment_status IN (
    'PENDING','SUCCESS','FAILED','REFUNDED','PARTIALLY_REFUNDED','CANCELLED'
  )),
  payment_date TIMESTAMP WITH TIME ZONE,
  refund_status VARCHAR(30),
  refund_amount NUMERIC(12,2),
  gateway_response JSONB,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_customer_id ON payments(customer_id);
CREATE INDEX idx_payments_status ON payments(payment_status);
CREATE INDEX idx_payments_transaction_id ON payments(transaction_id);

-- ---------- INVOICES ----------
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_number VARCHAR(30) UNIQUE NOT NULL,
  order_id UUID REFERENCES orders(id) ON DELETE SET NULL,
  customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
  subtotal NUMERIC(12,2) NOT NULL,
  gst_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  total_amount NUMERIC(12,2) NOT NULL,
  paid_amount NUMERIC(12,2) DEFAULT 0 NOT NULL,
  balance_amount NUMERIC(12,2) NOT NULL,
  invoice_date DATE DEFAULT CURRENT_DATE NOT NULL,
  due_date DATE,
  status VARCHAR(30) DEFAULT 'DRAFT' NOT NULL CHECK (status IN (
    'DRAFT','SENT','PAID','PARTIALLY_PAID','OVERDUE','CANCELLED'
  )),
  pdf_url TEXT,
  notes TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_invoices_number ON invoices(invoice_number);
CREATE INDEX idx_invoices_order_id ON invoices(order_id);
CREATE INDEX idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);

-- ---------- INVOICE ITEMS ----------
CREATE TABLE invoice_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  item_name VARCHAR(255) NOT NULL,
  description TEXT,
  quantity NUMERIC(10,2) DEFAULT 1 NOT NULL,
  unit_price NUMERIC(12,2) NOT NULL,
  total_price NUMERIC(12,2) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

CREATE INDEX idx_invoice_items_invoice_id ON invoice_items(invoice_id);

-- ---------- TRIGGERS ----------
CREATE TRIGGER quotations_updated_at
  BEFORE UPDATE ON quotations
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER orders_updated_at
  BEFORE UPDATE ON orders
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER payments_updated_at
  BEFORE UPDATE ON payments
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER invoices_updated_at
  BEFORE UPDATE ON invoices
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();