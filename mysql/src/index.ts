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

// Load configuration from config.json file
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

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load configuration from config.json file
const configPath = join(__dirname, '..', 'config.json');
const config = loadConfig(configPath);

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

// Use the first connection from config
// TODO: In future, we could implement a tool to switch between connections
if (config && config.connections && config.connections.length > 0) {
  const firstConn = config.connections[0];

  // Log which connection is being used (without password)
  console.error(`[MySQL MCP Wrapper] Using READ-ONLY connection: ${firstConn.name} (${firstConn.username}@${firstConn.host}:${firstConn.port}/${firstConn.database})`);

  if (config.connections.length > 1) {
    console.error(`[MySQL MCP Wrapper] Note: ${config.connections.length - 1} additional connection(s) configured but not active`);
    console.error(`[MySQL MCP Wrapper] Currently using first connection: ${firstConn.name}`);
  }

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