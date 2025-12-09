# MCP Docker

An MCP server for managing Docker with natural language!

## 🪩 What can it do?

- 🚀 Compose containers with natural language
- 🔍 Introspect & debug running containers
- 📀 Manage persistent data with Docker volumes

## ❓ Who is this for?

- **Server administrators**: connect to remote Docker engines for managing a public-facing website
- **Tinkerers**: spin up containers locally, without running a single command yourself

## 🏎️ Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

Add the following to your Claude Desktop config file:

```json
{
  "mcpServers": {
    "docker": {
      "command": "node",
      "args": ["/path/to/mcp-docker/build/index.js"],
      "env": {
        "DOCKER_SOCKET_PATH": "/var/run/docker.sock",
        "DOCKER_PROJECT_PREFIX": "mcp-"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

#### Install with `npm`

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-docker.git
cd mcp-docker

# Install dependencies
npm install

# Build the project
npm run build

# Start the server
npm start
```

## 🔨 Tools

### Containers

- **list_containers**: List all Docker containers
- **create_container**: Create a new Docker container without starting it
- **run_container**: Create and start a new Docker container
- **recreate_container**: Recreate a Docker container with the same or updated configuration
- **start_container**: Start a Docker container
- **fetch_container_logs**: Fetch logs from a Docker container
- **stop_container**: Stop a Docker container
- **remove_container**: Remove a Docker container

### Images

- **list_images**: List all Docker images
- **pull_image**: Pull a Docker image from a registry
- **push_image**: Push a Docker image to a registry
- **build_image**: Build a Docker image from a Dockerfile
- **remove_image**: Remove a Docker image

### Networks

- **list_networks**: List all Docker networks
- **create_network**: Create a Docker network
- **remove_network**: Remove a Docker network

### Volumes

- **list_volumes**: List all Docker volumes
- **create_volume**: Create a Docker volume
- **remove_volume**: Remove a Docker volume

## 📔 Resources

The server implements resources for Docker components:

- **docker://containers**: List of all Docker containers
- **docker://images**: List of all Docker images
- **docker://volumes**: List of all Docker volumes
- **docker://networks**: List of all Docker networks
- **docker://container/{id}/logs**: Logs for a specific container
- **docker://container/{id}/stats**: Stats for a specific container

## Configuration

The MCP Docker server can be configured using environment variables:

- `DOCKER_SOCKET_PATH`: Path to the Docker socket (default: `/var/run/docker.sock` on Unix, `//./pipe/docker_engine` on Windows)
- `DOCKER_HOST`: Docker host (used instead of socket path)
- `DOCKER_PORT`: Docker port (used with host)
- `DOCKER_PROTOCOL`: Docker protocol (http or https)
- `DOCKER_CA`: Path to CA certificate for secure connection
- `DOCKER_CERT`: Path to client certificate for secure connection
- `DOCKER_KEY`: Path to client key for secure connection
- `DOCKER_API_VERSION`: Docker API version to use
- `DOCKER_PROJECT_PREFIX`: Prefix for container names (default: `mcp-`)

## Development

```bash
# Install dependencies
npm install

# Build the project
npm run build

# Start the server
npm start

# Watch for changes during development
npm run dev
```

## Example Usage

### Creating and Running a Container

```json
{
  "name": "nginx-web",
  "image": "nginx:latest",
  "ports": [
    {
      "container": 80,
      "host": 8080
    }
  ],
  "volumes": [
    {
      "source": "nginx-data",
      "target": "/usr/share/nginx/html"
    }
  ]
}
```

### Composing Multiple Containers

You can use natural language to describe your container setup, and the LLM will translate it into the appropriate Docker commands:

"Deploy a WordPress site with a MySQL database, exposing WordPress on port 8080 and using persistent volumes for both the database and WordPress files."
