'use strict';

const projectService = require('../services/project.service');
const asyncHandler = require('../utils/asyncHandler');
const { success, created } = require('../utils/response');

const createProject = asyncHandler(async (req, res) => {
  const project = await projectService.createProject(req.body);
  return created(res, project, 'Project created successfully');
});

const listProjects = asyncHandler(async (req, res) => {
  const result = await projectService.listProjects(req.query);
  return success(res, result.data, 'Projects fetched');
});

const getProject = asyncHandler(async (req, res) => {
  const project = await projectService.getProject(req.params.id);
  return success(res, project, 'Project fetched');
});

const updateProject = asyncHandler(async (req, res) => {
  const project = await projectService.updateProject(req.params.id, req.body);
  return success(res, project, 'Project updated');
});

const addImage = asyncHandler(async (req, res) => {
  const { imageUrl, altText, imageType } = req.body;
  const image = await projectService.addProjectImage(
    req.params.id, imageUrl, altText, imageType,
  );
  return created(res, image, 'Image added');
});

const deleteImage = asyncHandler(async (req, res) => {
  await projectService.deleteProjectImage(req.params.imageId);
  return success(res, null, 'Image deleted');
});

const deleteProject = asyncHandler(async (req, res) => {
  await projectService.deleteProject(req.params.id);
  return success(res, null, 'Project deleted');
});

module.exports = {
  createProject,
  listProjects,
  getProject,
  updateProject,
  addImage,
  deleteImage,
  deleteProject,
};