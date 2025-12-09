interface DockerConfig {
  socketPath?: string;
  host?: string;
  port?: number;
  protocol?: string;
  ca?: string;
  cert?: string;
  key?: string;
  version?: string;
  projectPrefix?: string;
}

export function getConfig(): DockerConfig {
  const socketPath = process.env.DOCKER_SOCKET_PATH;
  const host = process.env.DOCKER_HOST;
  const port = process.env.DOCKER_PORT ? parseInt(process.env.DOCKER_PORT, 10) : undefined;
  const protocol = process.env.DOCKER_PROTOCOL;
  const ca = process.env.DOCKER_CA;
  const cert = process.env.DOCKER_CERT;
  const key = process.env.DOCKER_KEY;
  const version = process.env.DOCKER_API_VERSION;
  const projectPrefix = process.env.DOCKER_PROJECT_PREFIX || 'mcp-';

  // Default to socket path if no host is provided
  if (!socketPath && !host) {
    // Default socket paths based on OS
    if (process.platform === 'win32') {
      return { socketPath: '//./pipe/docker_engine', projectPrefix };
    } else {
      return { socketPath: '/var/run/docker.sock', projectPrefix };
    }
  }

  return {
    socketPath,
    host,
    port,
    protocol,
    ca,
    cert,
    key,
    version,
    projectPrefix
  };
}
