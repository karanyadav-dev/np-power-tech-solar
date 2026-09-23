'use strict';

/**
 * NP POWER TECH SOLAR - Database Seed Runner
 * 
 * Usage:
 *   node scripts/seed.js             — Run all pending seeds
 *   node scripts/seed.js status      — Show seed status
 */

const fs = require('fs');
const path = require('path');
const { Pool } = require('pg');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const SEEDS_DIR = path.join(__dirname, '..', '..', 'database', 'seed');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432', 10),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
});

async function ensureSeedsTable() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS schema_seeds (
      id SERIAL PRIMARY KEY,
      filename VARCHAR(255) UNIQUE NOT NULL,
      applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
    );
  `);
}

async function getAppliedSeeds() {
  const result = await pool.query('SELECT filename FROM schema_seeds ORDER BY filename');
  return result.rows.map((r) => r.filename);
}

async function getSeedFiles() {
  if (!fs.existsSync(SEEDS_DIR)) {
    console.error(`[seed] Seeds directory not found: ${SEEDS_DIR}`);
    process.exit(1);
  }
  return fs
    .readdirSync(SEEDS_DIR)
    .filter((f) => f.endsWith('.sql'))
    .sort();
}

async function run() {
  console.log('[seed] Running seeds...\n');
  await ensureSeedsTable();

  const applied = await getAppliedSeeds();
  const files = await getSeedFiles();
  const pending = files.filter((f) => !applied.includes(f));

  if (pending.length === 0) {
    console.log('[seed] ✅ No pending seeds. Database is up to date.');
    return;
  }

  for (const file of pending) {
    const filePath = path.join(SEEDS_DIR, file);
    const sql = fs.readFileSync(filePath, 'utf8');

    console.log(`[seed] Applying: ${file}`);

    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      await client.query(sql);
      await client.query('INSERT INTO schema_seeds (filename) VALUES ($1)', [file]);
      await client.query('COMMIT');
      console.log(`[seed] ✅ Applied: ${file}\n`);
    } catch (err) {
      await client.query('ROLLBACK');
      console.error(`[seed] ❌ Failed: ${file}`);
      console.error(`[seed] Error: ${err.message}\n`);
      throw err;
    } finally {
      client.release();
    }
  }

  console.log(`[seed] ✅ Completed ${pending.length} seed(s).`);
}

async function status() {
  await ensureSeedsTable();
  const applied = await getAppliedSeeds();
  const files = await getSeedFiles();

  console.log('\n=== SEED STATUS ===\n');
  for (const file of files) {
    const isApplied = applied.includes(file);
    const icon = isApplied ? '✅' : '⏳';
    console.log(`  ${icon}  ${file}  [${isApplied ? 'applied' : 'pending'}]`);
  }
  console.log(`\nTotal: ${files.length} | Applied: ${applied.length}\n`);
}

async function main() {
  const cmd = process.argv[2] || 'run';

  try {
    if (cmd === 'run') {
      await run();
    } else if (cmd === 'status') {
      await status();
    } else {
      console.log('Usage: node scripts/seed.js [run|status]');
    }
  } catch (err) {
    console.error('[seed] Fatal:', err.message);
    process.exit(1);
  } finally {
    await pool.end();
  }
}

main();