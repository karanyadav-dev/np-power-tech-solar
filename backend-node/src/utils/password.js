'use strict';

const argon2 = require('argon2');

/**
 * Password hashing with argon2id.
 * NEVER logs passwords.
 */

async function hashPassword(password) {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 2 ** 16,
    timeCost: 3,
    parallelism: 1,
  });
}

async function verifyPassword(hash, password) {
  try {
    return await argon2.verify(hash, password);
  } catch (err) {
    return false;
  }
}

module.exports = { hashPassword, verifyPassword };