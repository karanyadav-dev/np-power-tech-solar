'use strict';

const userModel = require('../models/user.model');
const { hashPassword } = require('../utils/password');

async function createUser(data) {
  if (await userModel.emailExists(data.email)) {
    const err = new Error('Email already exists');
    err.code = 'EMAIL_EXISTS';
    err.status = 409;
    throw err;
  }
  if (await userModel.phoneExists(data.phone)) {
    const err = new Error('Phone already exists');
    err.code = 'PHONE_EXISTS';
    err.status = 409;
    throw err;
  }

  const passwordHash = await hashPassword(data.password);
  const user = await userModel.create({
    email: data.email,
    phone: data.phone,
    passwordHash,
    fullName: data.fullName,
  });

  const roles = data.roles && data.roles.length > 0 ? data.roles : ['customer'];
  for (const role of roles) {
    await userModel.assignRole(user.id, role);
  }

  user.roles = await userModel.getUserRoles(user.id);
  return user;
}

async function getUser(id) {
  const user = await userModel.findById(id);
  if (!user) {
    const err = new Error('User not found');
    err.code = 'USER_NOT_FOUND';
    err.status = 404;
    throw err;
  }
  user.roles = await userModel.getUserRoles(id);
  return user;
}

async function listUsers(query) {
  return userModel.list(query);
}

async function updateUser(id, data) {
  await getUser(id);
  const updated = await userModel.update(id, data);
  if (!updated) {
    const err = new Error('No valid fields to update');
    err.code = 'NO_UPDATE';
    err.status = 400;
    throw err;
  }
  updated.roles = await userModel.getUserRoles(id);
  return updated;
}

async function deleteUser(id) {
  await getUser(id);
  const ok = await userModel.softDelete(id);
  if (!ok) {
    const err = new Error('Delete failed');
    err.code = 'DELETE_FAILED';
    err.status = 500;
    throw err;
  }
  return { id };
}

async function assignRoleToUser(id, roleName) {
  await getUser(id);
  await userModel.assignRole(id, roleName);
  return { id, roles: await userModel.getUserRoles(id) };
}

async function removeRoleFromUser(id, roleName) {
  await getUser(id);
  await userModel.removeRole(id, roleName);
  return { id, roles: await userModel.getUserRoles(id) };
}

module.exports = {
  createUser,
  getUser,
  listUsers,
  updateUser,
  deleteUser,
  assignRoleToUser,
  removeRoleFromUser,
};