'use strict';

const argon2 = require('argon2');
const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

async function changePassword() {
  try {
    const newPassword = 'Dinesh@2025';
    const hash = await argon2.hash(newPassword, {
      type: argon2.argon2id,
      memoryCost: 2 ** 16,
      timeCost: 3,
      parallelism: 1,
    });

    const result = await pool.query(
      'UPDATE users SET password_hash = $1, updated_at = NOW() WHERE email = $2 RETURNING email',
      [hash, 'nppowertechsolar@gmail.com']
    );

    if (result.rowCount > 0) {
      console.log('✅ Password changed for:', result.rows[0].email);
    } else {
      console.log('❌ User not found');
    }
  } catch (err) {
    console.error('❌ Error:', err.message);
  } finally {
    await pool.end();
  }
}

changePassword();