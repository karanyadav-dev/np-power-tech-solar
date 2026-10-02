'use strict';

const express = require('express');
const projectController = require('../controllers/project.controller');
const { validate } = require('../middleware/validate');
const { authenticate } = require('../middleware/auth');
const { requireRoles } = require('../middleware/rbac');
const {
  createProjectSchema,
  updateProjectSchema,
  listProjectsQuerySchema,
} = require('../validators/project.validator');

const router = express.Router();

// ---------- PUBLIC ----------
// Anyone can view published projects
router.get('/', validate({ query: listProjectsQuerySchema }), projectController.listProjects);

// ---------- PROTECTED (admin only) ----------
router.get(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  projectController.getProject,
);

router.post(
  '/',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  validate({ body: createProjectSchema }),
  projectController.createProject,
);

router.patch(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  validate({ body: updateProjectSchema }),
  projectController.updateProject,
);

router.delete(
  '/:id',
  authenticate,
  requireRoles('super_admin', 'admin'),
  projectController.deleteProject,
);

// Images
router.post(
  '/:id/images',
  authenticate,
  requireRoles('super_admin', 'admin', 'content_manager'),
  projectController.addImage,
);

router.delete(
  '/images/:imageId',
  authenticate,
  requireRoles('super_admin', 'admin'),
  projectController.deleteImage,
);

module.exports = router;