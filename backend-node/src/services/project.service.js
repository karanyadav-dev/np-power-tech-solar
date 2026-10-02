'use strict';

const projectModel = require('../models/project.model');

async function createProject(data) {
  const existing = await projectModel.findBySlug(data.slug);
  if (existing) {
    const err = new Error('Project slug already exists');
    err.code = 'SLUG_EXISTS';
    err.status = 409;
    throw err;
  }

  const project = await projectModel.create(data);

  // Add images if provided
  if (data.images && data.images.length > 0) {
    for (let i = 0; i < data.images.length; i++) {
      await projectModel.addImage(project.id, data.images[i], null, 'gallery', i);
    }
  }

  return projectModel.findById(project.id);
}

async function getProject(id) {
  const project = await projectModel.findById(id);
  if (!project) {
    const err = new Error('Project not found');
    err.code = 'PROJECT_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  return project;
}

async function listProjects(query) {
  return projectModel.list(query);
}

async function updateProject(id, data) {
  await getProject(id);

  if (data.slug) {
    const existing = await projectModel.findBySlug(data.slug);
    if (existing && existing.id !== id) {
      const err = new Error('Project slug already exists');
      err.code = 'SLUG_EXISTS';
      err.status = 409;
      throw err;
    }
  }

  const updated = await projectModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }

  // Update images if provided
  if (data.images !== undefined) {
    // Delete old images
    const current = await projectModel.findById(id);
    for (const img of current.images || []) {
      await projectModel.deleteImage(img.id);
    }

    // Add new
    for (let i = 0; i < data.images.length; i++) {
      await projectModel.addImage(id, data.images[i], null, 'gallery', i);
    }
  }

  return projectModel.findById(id);
}

async function addProjectImage(projectId, imageUrl, altText, imageType) {
  await getProject(projectId);
  return projectModel.addImage(projectId, imageUrl, altText, imageType);
}

async function deleteProjectImage(imageId) {
  return projectModel.deleteImage(imageId);
}

async function deleteProject(id) {
  await getProject(id);
  await projectModel.softDelete(id);
  return { id };
}

module.exports = {
  createProject,
  getProject,
  listProjects,
  updateProject,
  addProjectImage,
  deleteProjectImage,
  deleteProject,
};