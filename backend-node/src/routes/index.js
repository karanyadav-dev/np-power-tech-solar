'use strict';

const express = require('express');
const authRoutes = require('./auth.routes');

/**
 * API v1 router — mounts all module routes.
 */

const router = express.Router();

router.use('/auth', authRoutes);

// Future modules will be mounted here:
// router.use('/users', userRoutes);
// router.use('/leads', leadRoutes);
// router.use('/customers', customerRoutes);
// router.use('/products', productRoutes);
// router.use('/quotes', quoteRoutes);
// router.use('/orders', orderRoutes);
// router.use('/payments', paymentRoutes);
// router.use('/invoices', invoiceRoutes);
// router.use('/surveys', surveyRoutes);
// router.use('/installations', installationRoutes);
// router.use('/technicians', technicianRoutes);
// router.use('/warranty', warrantyRoutes);
// router.use('/amc', amcRoutes);
// router.use('/service', serviceRoutes);
// router.use('/pincode', pincodeRoutes);
// router.use('/subsidy', subsidyRoutes);
// router.use('/reviews', reviewRoutes);
// router.use('/blog', blogRoutes);
// router.use('/notifications', notificationRoutes);
// router.use('/analytics', analyticsRoutes);

module.exports = router;