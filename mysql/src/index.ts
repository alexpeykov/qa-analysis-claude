#!/usr/bin/env node

/**
 * MySQL MCP Wrapper
 *
 * This is a lightweight wrapper that launches the dpflucas/mysql-mcp-server from the upstream submodule.
 * The actual implementation is in the upstream submodule at ./upstream
 * This server provides READ-ONLY access to MySQL databases.
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';
import dotenv from 'dotenv';

interface MySQLConfig {
  connections: Array<{
    id: string;
    name: string;
    host: string;
    port: number;
    database: string;
    username: string;
    password: string;
  }>;
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env file
const envPath = join(__dirname, '..', '..', '.env');
dotenv.config({ path: envPath });

// Build configuration from environment variables
const buildConfigFromEnv = (): MySQLConfig => {
  const connections: MySQLConfig['connections'] = [];

  // Helper function to add connection if all required fields are present
  const addConnection = (id: string, name: string, prefix: string) => {
    const host = process.env[`${prefix}_HOST`];
    const port = process.env[`${prefix}_PORT`];
    const database = process.env[`${prefix}_DATABASE`];
    const username = process.env[`${prefix}_USER`];
    const password = process.env[`${prefix}_PASSWORD`];

    if (host && port && database && username && password) {
      connections.push({
        id,
        name,
        host,
        port: parseInt(port, 10),
        database,
        username,
        password
      });
    }
  };

  // Add all configured connections
  addConnection('default', 'Default MySQL', 'MYSQL');
  addConnection('evpbank-local', 'EVPBank Local', 'EVPBANK_LOCAL');
  addConnection('evpbank-remote', 'EVPBank Remote', 'EVPBANK_REMOTE');
  addConnection('mokejimai-local', 'Mokejimai Local', 'MOKEJIMAI_LOCAL');
  addConnection('mokejimai-remote', 'Mokejimai Remote', 'MOKEJIMAI_REMOTE');

  return { connections };
};

// Load configuration from config.json file (fallback)
const loadConfig = (configPath: string): MySQLConfig | null => {
  if (fs.existsSync(configPath)) {
    try {
      const configFile = fs.readFileSync(configPath, 'utf8');
      const config = JSON.parse(configFile);
      return config;
    } catch (error) {
      console.error('[MySQL MCP Wrapper] Error parsing config.json:', error);
      process.exit(1);
    }
  }
  return null;
};

// Try to load from config.json first, then fall back to environment variables
const configPath = join(__dirname, '..', 'config.json');
let config = loadConfig(configPath);

// If no config.json, build from environment variables
if (!config || !config.connections || config.connections.length === 0) {
  console.error('[MySQL MCP Wrapper] No config.json found, loading from environment variables...');
  config = buildConfigFromEnv();
}

// Path to the upstream MySQL MCP server
const upstreamPath = join(__dirname, '..', 'upstream', 'build', 'index.js');

// Check if the upstream server exists
if (!fs.existsSync(upstreamPath)) {
  console.error('[MySQL MCP Wrapper] Error: Upstream MySQL MCP server not found.');
  console.error('[MySQL MCP Wrapper] Please ensure the submodule is initialized and built:');
  console.error('[MySQL MCP Wrapper]   git submodule update --init --recursive');
  console.error('[MySQL MCP Wrapper]   cd mcp-mysql/upstream && npm install && npm run build');
  process.exit(1);
}

// Check if configuration is available
if (!config || !config.connections || config.connections.length === 0) {
  console.error('[MySQL MCP Wrapper] Error: No MySQL connections configured in config.json');
  console.error('[MySQL MCP Wrapper] Please run the setup script to configure MySQL MCP.');
  process.exit(1);
}

// Select connection based on MYSQL_CONNECTION_ID environment variable, or use first connection
if (config && config.connections && config.connections.length > 0) {
  const selectedConnectionId = process.env.MYSQL_CONNECTION_ID;
  let selectedConn = config.connections[0];

  // If a specific connection ID is requested, try to find it
  if (selectedConnectionId) {
    const found = config.connections.find(conn => conn.id === selectedConnectionId);
    if (found) {
      selectedConn = found;
      console.error(`[MySQL MCP Wrapper] Selected connection by ID: ${selectedConnectionId}`);
    } else {
      console.error(`[MySQL MCP Wrapper] Warning: Connection ID '${selectedConnectionId}' not found, using first connection`);
    }
  }

  // Log which connection is being used (without password)
  console.error(`[MySQL MCP Wrapper] Using READ-ONLY connection: ${selectedConn.name} (${selectedConn.username}@${selectedConn.host}:${selectedConn.port}/${selectedConn.database})`);

  if (config.connections.length > 1) {
    console.error(`[MySQL MCP Wrapper] Note: ${config.connections.length - 1} additional connection(s) configured but not active`);
    console.error(`[MySQL MCP Wrapper] Available connections: ${config.connections.map(c => c.id).join(', ')}`);
    console.error(`[MySQL MCP Wrapper] Set MYSQL_CONNECTION_ID environment variable to switch connections`);
  }

  const firstConn = selectedConn;

  // Prepare environment variables for dpflucas/mysql-mcp-server
  // It expects MYSQL_* environment variables
  const envVars = {
    ...process.env,
    MYSQL_HOST: firstConn.host,
    MYSQL_PORT: firstConn.port.toString(),
    MYSQL_DATABASE: firstConn.database,
    MYSQL_USER: firstConn.username,
    MYSQL_PASSWORD: firstConn.password
  };

  // Launch the upstream MySQL MCP server
  const child = spawn('node', [upstreamPath], {
    stdio: 'inherit',
    env: envVars
  });

  // Handle process termination
  child.on('error', (error) => {
    console.error('[MySQL MCP Wrapper] Failed to start MySQL MCP server:', error);
    console.error('[MySQL MCP Wrapper] Make sure Node.js is installed and dependencies are available.');
    process.exit(1);
  });

  child.on('exit', (code, signal) => {
    if (code !== null) {
      process.exit(code);
    } else if (signal) {
      console.error(`[MySQL MCP Wrapper] Process terminated by signal: ${signal}`);
      process.exit(1);
    }
  });

  // Forward termination signals to the child process
  ['SIGINT', 'SIGTERM', 'SIGHUP'].forEach(signal => {
    process.on(signal as any, () => {
      child.kill(signal as any);
    });
  });
}