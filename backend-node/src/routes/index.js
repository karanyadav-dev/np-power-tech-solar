'use strict';

const express = require('express');

// ---------- Route Imports ----------
const authRoutes = require('./auth.routes');
const leadRoutes = require('./lead.routes');
const customerRoutes = require('./customer.routes');
const productRoutes = require('./product.routes');
const userRoutes = require('./user.routes');
const roleRoutes = require('./role.routes');
const quotationRoutes = require('./quotation.routes');
const uploadRoutes = require('./upload.routes');
const reviewRoutes = require('./review.routes');
const settingRoutes = require('./setting.routes');
const projectRoutes = require('./project.routes');

const router = express.Router();

// ============================================================
// API ROUTES
// ============================================================

// ---------- Auth ----------
router.use('/auth', authRoutes);

// ---------- Leads ----------
router.use('/leads', leadRoutes);

// ---------- Customers ----------
router.use('/customers', customerRoutes);

// ---------- Products ----------
router.use('/products', productRoutes);

// ---------- Users ----------
router.use('/users', userRoutes);

// ---------- Roles ----------
router.use('/roles', roleRoutes);

// ---------- Quotations ----------
router.use('/quotations', quotationRoutes);

// ---------- Uploads ----------
router.use('/uploads', uploadRoutes);

// ---------- Reviews ----------
router.use('/reviews', reviewRoutes);

// ---------- Settings ----------
router.use('/settings', settingRoutes);

// ---------- Projects ----------
router.use('/projects', projectRoutes);

// ============================================================
// FUTURE MODULES (uncomment when implemented)
// ============================================================
// router.use('/surveys', require('./survey.routes'));
// router.use('/orders', require('./order.routes'));
// router.use('/payments', require('./payment.routes'));
// router.use('/invoices', require('./invoice.routes'));
// router.use('/installations', require('./installation.routes'));
// router.use('/technicians', require('./technician.routes'));
// router.use('/warranty', require('./warranty.routes'));
// router.use('/amc', require('./amc.routes'));
// router.use('/service', require('./service.routes'));
// router.use('/pincode', require('./pincode.routes'));
// router.use('/subsidy', require('./subsidy.routes'));
// router.use('/blog', require('./blog.routes'));
// router.use('/notifications', require('./notification.routes'));
// router.use('/analytics', require('./analytics.routes'));

module.exports = router;