'use strict';

/**
 * NP POWER TECH SOLAR - Database Migration Runner
 * 
 * Usage:
 *   node scripts/migrate.js up       — Run all pending migrations
 *   node scripts/migrate.js status   — Show migration status
 *   node scripts/migrate.js down     — Rollback last migration (use carefully)
 */

const fs = require('fs');
const path = require('path');
const { Pool } = require('pg');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const MIGRATIONS_DIR = path.join(__dirname, '..', '..', 'database', 'migrations');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

async function ensureMigrationsTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      id SERIAL PRIMARY KEY,
      filename VARCHAR(255) UNIQUE NOT NULL,
      applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
    );
  `);
}

async function getAppliedMigrations() {
  const result = await pool.query('SELECT filename FROM schema_migrations ORDER BY filename');
  return result.rows.map((r) => r.filename);
}

async function getMigrationFiles() {
  if (!fs.existsSync(MIGRATIONS_DIR)) {
    console.error(`[migrate] Migrations directory not found: ${MIGRATIONS_DIR}`);
    process.exit(1);
  }
  return fs
    .readdirSync(MIGRATIONS_DIR)
    .filter((f) => f.endsWith('.sql'))
    .sort();
}

async function up() {
  console.log('[migrate] Running migrations...\n');
  await ensureMigrationsTable();

  const applied = await getAppliedMigrations();
  const files = await getMigrationFiles();
  const pending = files.filter((f) => !applied.includes(f));

  if (pending.length === 0) {
    console.log('[migrate] ✅ No pending migrations. Database is up to date.');
    return;
  }

  for (const file of pending) {
    const filePath = path.join(MIGRATIONS_DIR, file);
    const sql = fs.readFileSync(filePath, 'utf8');

    console.log(`[migrate] Applying: ${file}`);

    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      await client.query(sql);
      await client.query('INSERT INTO schema_migrations (filename) VALUES ($1)', [file]);
      await client.query('COMMIT');
      console.log(`[migrate] ✅ Applied: ${file}\n`);
    } catch (err) {
      await client.query('ROLLBACK');
      console.error(`[migrate] ❌ Failed: ${file}`);
      console.error(`[migrate] Error: ${err.message}\n`);
      throw err;
    } finally {
      client.release();
    }
  }

  console.log(`[migrate] ✅ Completed ${pending.length} migration(s).`);
}

async function status() {
  await ensureMigrationsTable();
  const applied = await getAppliedMigrations();
  const files = await getMigrationFiles();

  console.log('\n=== MIGRATION STATUS ===\n');
  for (const file of files) {
    const isApplied = applied.includes(file);
    const icon = isApplied ? '✅' : '⏳';
    const label = isApplied ? 'applied' : 'pending';
    console.log(`  ${icon}  ${file}  [${label}]`);
  }
  console.log(`\nTotal: ${files.length} | Applied: ${applied.length} | Pending: ${files.length - applied.length}\n`);
}

async function down() {
  console.log('[migrate] Rollback is not supported automatically. Run manual SQL if needed.');
}

async function main() {
  const cmd = process.argv[2] || 'up';

  try {
    if (cmd === 'up') {
      await up();
    } else if (cmd === 'status') {
      await status();
    } else if (cmd === 'down') {
      await down();
    } else {
      console.log('Usage: node scripts/migrate.js [up|status|down]');
    }
  } catch (err) {
    console.error('[migrate] Fatal:', err.message);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

main();