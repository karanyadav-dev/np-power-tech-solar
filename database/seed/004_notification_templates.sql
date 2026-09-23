-- ==============================================================
-- Seed 004: Notification Templates
-- ==============================================================

INSERT INTO notification_templates (code, name, channel, subject, body, variables) VALUES
  ('lead_created', 'New Lead Created', 'inapp', 'New Lead',
   'New lead created: {{lead_number}} - {{customer_name}}', '{"lead_number":"","customer_name":""}'),

  ('quotation_submitted', 'Quotation Request Submitted', 'inapp', 'New Quotation Request',
   'New quotation request from {{customer_name}} ({{pincode}})', '{"customer_name":"","pincode":""}'),

  ('quotation_approved', 'Quotation Approved', 'inapp', 'Quotation Approved',
   'Quotation {{quotation_number}} has been approved', '{"quotation_number":""}'),

  ('quotation_sent', 'Quotation Sent to Customer', 'email', 'Your Quotation from NP POWER TECH SOLAR',
   'Dear {{customer_name}}, your quotation {{quotation_number}} is ready. Please review.', '{"customer_name":"","quotation_number":""}'),

  ('order_created', 'Order Created', 'inapp', 'New Order',
   'Order {{order_number}} created', '{"order_number":""}'),

  ('payment_received', 'Payment Received', 'inapp', 'Payment Received',
   'Payment of {{amount}} received for order {{order_number}}', '{"amount":"","order_number":""}'),

  ('installation_scheduled', 'Installation Scheduled', 'inapp', 'Installation Scheduled',
   'Installation scheduled for {{scheduled_date}}', '{"scheduled_date":""}'),

  ('installation_completed', 'Installation Completed', 'inapp', 'Installation Completed',
   'Installation completed for order {{order_number}}', '{"order_number":""}'),

  ('invoice_generated', 'Invoice Generated', 'email', 'Invoice from NP POWER TECH SOLAR',
   'Invoice {{invoice_number}} generated. Amount: {{amount}}', '{"invoice_number":"","amount":""}'),

  ('amc_renewal_reminder', 'AMC Renewal Reminder', 'email', 'AMC Renewal Reminder',
   'Your AMC contract {{contract_number}} will expire on {{end_date}}', '{"contract_number":"","end_date":""}'),

  ('service_ticket_created', 'Service Ticket Created', 'inapp', 'New Service Ticket',
   'Service ticket {{ticket_number}} created', '{"ticket_number":""}'),

  ('warranty_registered', 'Warranty Registered', 'inapp', 'Warranty Registered',
   'Warranty {{warranty_number}} registered', '{"warranty_number":""}')
ON CONFLICT (code) DO NOTHING;