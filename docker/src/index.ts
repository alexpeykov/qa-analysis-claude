#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  McpError,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { DockerClient } from './docker-client.js';

class DockerServer {
  private server: Server;
  private dockerClient: DockerClient;

  constructor() {
    this.server = new Server(
      {
        name: 'mcp-docker',
        version: '1.0.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.dockerClient = new DockerClient();
    this.setupResourceHandlers();
    this.setupToolHandlers();
    
    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupResourceHandlers() {
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => ({
      resources: [
        {
          uri: 'docker://containers',
          name: 'Docker Containers',
          description: 'List of all Docker containers',
          mimeType: 'application/json',
        },
        {
          uri: 'docker://images',
          name: 'Docker Images',
          description: 'List of all Docker images',
          mimeType: 'application/json',
        },
        {
          uri: 'docker://volumes',
          name: 'Docker Volumes',
          description: 'List of all Docker volumes',
          mimeType: 'application/json',
        },
        {
          uri: 'docker://networks',
          name: 'Docker Networks',
          description: 'List of all Docker networks',
          mimeType: 'application/json',
        },
      ],
    }));

    // Handle resource requests
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      try {
        const { uri } = request.params;
        let content = '';

        switch (uri) {
          case 'docker://containers':
            const containers = await this.dockerClient.listContainers();
            content = JSON.stringify(containers, null, 2);
            break;
          
          case 'docker://images':
            const images = await this.dockerClient.listImages();
            content = JSON.stringify(images, null, 2);
            break;
          
          case 'docker://volumes':
            const volumes = await this.dockerClient.listVolumes();
            content = JSON.stringify(volumes, null, 2);
            break;
          
          case 'docker://networks':
            const networks = await this.dockerClient.listNetworks();
            content = JSON.stringify(networks, null, 2);
            break;
          
          default:
            if (uri.startsWith('docker://container/')) {
              const containerId = uri.replace('docker://container/', '');
              if (uri.endsWith('/logs')) {
                const logs = await this.dockerClient.getContainerLogs(containerId);
                content = logs;
              } else if (uri.endsWith('/stats')) {
                const stats = await this.dockerClient.getContainerStats(containerId);
                content = JSON.stringify(stats, null, 2);
              } else {
                throw new McpError(ErrorCode.InvalidRequest, `Unknown container resource: ${uri}`);
              }
            } else {
              throw new McpError(ErrorCode.InvalidRequest, `Unknown resource: ${uri}`);
            }
        }

        return {
          contents: [
            {
              uri: request.params.uri,
              mimeType: 'application/json',
              text: content,
            },
          ],
        };
      } catch (error) {
        if (error instanceof McpError) throw error;
        throw new McpError(
          ErrorCode.InternalError,
          error instanceof Error ? error.message : 'Unknown error occurred'
        );
      }
    });
  }

  private setupToolHandlers() {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        // Container operations
        {
          name: 'list_containers',
          description: 'List all Docker containers',
          inputSchema: {
            type: 'object',
            properties: {
              projectName: {
                type: 'string',
                description: 'Filter containers by project name',
              },
            },
          },
        },
        {
          name: 'create_container',
          description: 'Create a new Docker container without starting it',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Container name',
              },
              image: {
                type: 'string',
                description: 'Image name (e.g., nginx:latest)',
              },
              projectName: {
                type: 'string',
                description: 'Project name for grouping containers',
              },
              env: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'Environment variables (e.g., ["KEY=value"])',
              },
              ports: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    container: {
                      type: 'number',
                      description: 'Container port',
                    },
                    host: {
                      type: 'number',
                      description: 'Host port',
                    },
                  },
                  required: ['container', 'host'],
                },
                description: 'Port mappings',
              },
              volumes: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    source: {
                      type: 'string',
                      description: 'Source path or volume name',
                    },
                    target: {
                      type: 'string',
                      description: 'Target path in container',
                    },
                  },
                  required: ['source', 'target'],
                },
                description: 'Volume mappings',
              },
              cmd: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'Command to run in the container',
              },
              networkMode: {
                type: 'string',
                description: 'Network mode (e.g., bridge, host, none)',
              },
              restart: {
                type: 'string',
                description: 'Restart policy (e.g., no, always, on-failure)',
              },
            },
            required: ['name', 'image'],
          },
        },
        {
          name: 'run_container',
          description: 'Create and start a new Docker container',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Container name',
              },
              image: {
                type: 'string',
                description: 'Image name (e.g., nginx:latest)',
              },
              projectName: {
                type: 'string',
                description: 'Project name for grouping containers',
              },
              env: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'Environment variables (e.g., ["KEY=value"])',
              },
              ports: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    container: {
                      type: 'number',
                      description: 'Container port',
                    },
                    host: {
                      type: 'number',
                      description: 'Host port',
                    },
                  },
                  required: ['container', 'host'],
                },
                description: 'Port mappings',
              },
              volumes: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    source: {
                      type: 'string',
                      description: 'Source path or volume name',
                    },
                    target: {
                      type: 'string',
                      description: 'Target path in container',
                    },
                  },
                  required: ['source', 'target'],
                },
                description: 'Volume mappings',
              },
              cmd: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'Command to run in the container',
              },
              networkMode: {
                type: 'string',
                description: 'Network mode (e.g., bridge, host, none)',
              },
              restart: {
                type: 'string',
                description: 'Restart policy (e.g., no, always, on-failure)',
              },
            },
            required: ['name', 'image'],
          },
        },
        {
          name: 'recreate_container',
          description: 'Recreate a Docker container with the same or updated configuration',
          inputSchema: {
            type: 'object',
            properties: {
              containerId: {
                type: 'string',
                description: 'Container ID or name',
              },
              image: {
                type: 'string',
                description: 'New image name (optional)',
              },
              env: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'New environment variables (optional)',
              },
              cmd: {
                type: 'array',
                items: {
                  type: 'string',
                },
                description: 'New command (optional)',
              },
            },
            required: ['containerId'],
          },
        },
        {
          name: 'start_container',
          description: 'Start a Docker container',
          inputSchema: {
            type: 'object',
            properties: {
              containerId: {
                type: 'string',
                description: 'Container ID or name',
              },
            },
            required: ['containerId'],
          },
        },
        {
          name: 'fetch_container_logs',
          description: 'Fetch logs from a Docker container',
          inputSchema: {
            type: 'object',
            properties: {
              containerId: {
                type: 'string',
                description: 'Container ID or name',
              },
              tail: {
                type: 'number',
                description: 'Number of lines to fetch from the end',
                default: 100,
              },
            },
            required: ['containerId'],
          },
        },
        {
          name: 'stop_container',
          description: 'Stop a Docker container',
          inputSchema: {
            type: 'object',
            properties: {
              containerId: {
                type: 'string',
                description: 'Container ID or name',
              },
            },
            required: ['containerId'],
          },
        },
        {
          name: 'remove_container',
          description: 'Remove a Docker container',
          inputSchema: {
            type: 'object',
            properties: {
              containerId: {
                type: 'string',
                description: 'Container ID or name',
              },
              force: {
                type: 'boolean',
                description: 'Force removal of running container',
                default: false,
              },
            },
            required: ['containerId'],
          },
        },
        
        // Image operations
        {
          name: 'list_images',
          description: 'List all Docker images',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'pull_image',
          description: 'Pull a Docker image from a registry',
          inputSchema: {
            type: 'object',
            properties: {
              imageName: {
                type: 'string',
                description: 'Image name to pull (e.g., nginx:latest)',
              },
            },
            required: ['imageName'],
          },
        },
        {
          name: 'push_image',
          description: 'Push a Docker image to a registry',
          inputSchema: {
            type: 'object',
            properties: {
              imageName: {
                type: 'string',
                description: 'Image name to push',
              },
            },
            required: ['imageName'],
          },
        },
        {
          name: 'build_image',
          description: 'Build a Docker image from a Dockerfile',
          inputSchema: {
            type: 'object',
            properties: {
              tarContext: {
                type: 'string',
                description: 'Path to tar file containing build context',
              },
              tag: {
                type: 'string',
                description: 'Tag for the built image',
              },
              dockerfile: {
                type: 'string',
                description: 'Path to Dockerfile (relative to context)',
              },
            },
            required: ['tarContext', 'tag'],
          },
        },
        {
          name: 'remove_image',
          description: 'Remove a Docker image',
          inputSchema: {
            type: 'object',
            properties: {
              imageId: {
                type: 'string',
                description: 'Image ID or name',
              },
              force: {
                type: 'boolean',
                description: 'Force removal of the image',
                default: false,
              },
            },
            required: ['imageId'],
          },
        },
        
        // Network operations
        {
          name: 'list_networks',
          description: 'List all Docker networks',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'create_network',
          description: 'Create a Docker network',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Network name',
              },
              driver: {
                type: 'string',
                description: 'Network driver (e.g., bridge, overlay)',
                default: 'bridge',
              },
              internal: {
                type: 'boolean',
                description: 'Restrict external access to the network',
                default: false,
              },
            },
            required: ['name'],
          },
        },
        {
          name: 'remove_network',
          description: 'Remove a Docker network',
          inputSchema: {
            type: 'object',
            properties: {
              networkId: {
                type: 'string',
                description: 'Network ID or name',
              },
            },
            required: ['networkId'],
          },
        },
        
        // Volume operations
        {
          name: 'list_volumes',
          description: 'List all Docker volumes',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'create_volume',
          description: 'Create a Docker volume',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Volume name',
              },
              driver: {
                type: 'string',
                description: 'Volume driver',
                default: 'local',
              },
              labels: {
                type: 'object',
                description: 'Volume labels',
              },
            },
            required: ['name'],
          },
        },
        {
          name: 'remove_volume',
          description: 'Remove a Docker volume',
          inputSchema: {
            type: 'object',
            properties: {
              name: {
                type: 'string',
                description: 'Volume name',
              },
              force: {
                type: 'boolean',
                description: 'Force removal of the volume',
                default: false,
              },
            },
            required: ['name'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const { name, arguments: args } = request.params;
        
        switch (name) {
          // Container operations
          case 'list_containers': {
            const { projectName } = args as { projectName?: string };
            const containers = await this.dockerClient.listContainers(projectName);
            return {
              content: [{ type: 'text', text: JSON.stringify(containers, null, 2) }],
            };
          }
          
          case 'create_container': {
            const { 
              name: containerName, 
              image, 
              projectName,
              env,
              ports,
              volumes,
              cmd,
              networkMode,
              restart
            } = args as { 
              name: string; 
              image: string; 
              projectName?: string;
              env?: string[];
              ports?: Array<{ container: number; host: number }>;
              volumes?: Array<{ source: string; target: string }>;
              cmd?: string[];
              networkMode?: string;
              restart?: string;
            };
            
            // Prepare port bindings
            const exposedPorts: Record<string, {}> = {};
            const portBindings: Record<string, Array<{HostPort: string}>> = {};
            
            if (ports && ports.length > 0) {
              ports.forEach(port => {
                const containerPort = `${port.container}/tcp`;
                exposedPorts[containerPort] = {};
                portBindings[containerPort] = [{ HostPort: port.host.toString() }];
              });
            }
            
            // Prepare volume bindings
            const binds: string[] = [];
            
            if (volumes && volumes.length > 0) {
              volumes.forEach(volume => {
                binds.push(`${volume.source}:${volume.target}`);
              });
            }
            
            // Prepare restart policy
            const restartPolicy = restart ? {
              Name: restart,
              MaximumRetryCount: restart === 'on-failure' ? 5 : undefined
            } : undefined;
            
            const options = {
              name: containerName,
              Image: image,
              Env: env,
              Cmd: cmd,
              ExposedPorts: Object.keys(exposedPorts).length > 0 ? exposedPorts : undefined,
              HostConfig: {
                PortBindings: Object.keys(portBindings).length > 0 ? portBindings : undefined,
                Binds: binds.length > 0 ? binds : undefined,
                NetworkMode: networkMode,
                RestartPolicy: restartPolicy
              }
            };
            
            const result = await this.dockerClient.createContainer(options, projectName);
            return {
              content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
          }
          
          case 'run_container': {
            const { 
              name: containerName, 
              image, 
              projectName,
              env,
              ports,
              volumes,
              cmd,
              networkMode,
              restart
            } = args as { 
              name: string; 
              image: string; 
              projectName?: string;
              env?: string[];
              ports?: Array<{ container: number; host: number }>;
              volumes?: Array<{ source: string; target: string }>;
              cmd?: string[];
              networkMode?: string;
              restart?: string;
            };
            
            // Prepare port bindings
            const exposedPorts: Record<string, {}> = {};
            const portBindings: Record<string, Array<{HostPort: string}>> = {};
            
            if (ports && ports.length > 0) {
              ports.forEach(port => {
                const containerPort = `${port.container}/tcp`;
                exposedPorts[containerPort] = {};
                portBindings[containerPort] = [{ HostPort: port.host.toString() }];
              });
            }
            
            // Prepare volume bindings
            const binds: string[] = [];
            
            if (volumes && volumes.length > 0) {
              volumes.forEach(volume => {
                binds.push(`${volume.source}:${volume.target}`);
              });
            }
            
            // Prepare restart policy
            const restartPolicy = restart ? {
              Name: restart,
              MaximumRetryCount: restart === 'on-failure' ? 5 : undefined
            } : undefined;
            
            const options = {
              name: containerName,
              Image: image,
              Env: env,
              Cmd: cmd,
              ExposedPorts: Object.keys(exposedPorts).length > 0 ? exposedPorts : undefined,
              HostConfig: {
                PortBindings: Object.keys(portBindings).length > 0 ? portBindings : undefined,
                Binds: binds.length > 0 ? binds : undefined,
                NetworkMode: networkMode,
                RestartPolicy: restartPolicy
              }
            };
            
            const result = await this.dockerClient.runContainer(options, projectName);
            return {
              content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
          }
          
          case 'recreate_container': {
            const { containerId, image, env, cmd } = args as { 
              containerId: string; 
              image?: string;
              env?: string[];
              cmd?: string[];
            };
            
            let options;
            if (image || env || cmd) {
              options = {
                name: '', // Will be overridden by the recreate method
                Image: image || '',
                Env: env || [],
                Cmd: cmd || []
              };
            }
            
            const result = await this.dockerClient.recreateContainer(containerId, options);
            return {
              content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
          }
          
          case 'start_container': {
            const { containerId } = args as { containerId: string };
            await this.dockerClient.startContainer(containerId);
            return {
              content: [{ type: 'text', text: `Container ${containerId} started successfully` }],
            };
          }
          
          case 'fetch_container_logs': {
            const { containerId, tail } = args as { containerId: string; tail?: number };
            const logs = await this.dockerClient.getContainerLogs(containerId, tail);
            return {
              content: [{ type: 'text', text: logs }],
            };
          }
          
          case 'stop_container': {
            const { containerId } = args as { containerId: string };
            await this.dockerClient.stopContainer(containerId);
            return {
              content: [{ type: 'text', text: `Container ${containerId} stopped successfully` }],
            };
          }
          
          case 'remove_container': {
            const { containerId, force } = args as { containerId: string; force?: boolean };
            await this.dockerClient.removeContainer(containerId, force);
            return {
              content: [{ type: 'text', text: `Container ${containerId} removed successfully` }],
            };
          }
          
          // Image operations
          case 'list_images': {
            const images = await this.dockerClient.listImages();
            return {
              content: [{ type: 'text', text: JSON.stringify(images, null, 2) }],
            };
          }
          
          case 'pull_image': {
            const { imageName } = args as { imageName: string };
            await this.dockerClient.pullImage(imageName);
            return {
              content: [{ type: 'text', text: `Image ${imageName} pulled successfully` }],
            };
          }
          
          case 'push_image': {
            const { imageName } = args as { imageName: string };
            await this.dockerClient.pushImage(imageName);
            return {
              content: [{ type: 'text', text: `Image ${imageName} pushed successfully` }],
            };
          }
          
          case 'build_image': {
            const { tarContext, tag, dockerfile } = args as { 
              tarContext: string; 
              tag: string;
              dockerfile?: string;
            };
            
            const options = {
              t: tag,
              dockerfile
            };
            
            await this.dockerClient.buildImage(tarContext, options);
            return {
              content: [{ type: 'text', text: `Image ${tag} built successfully` }],
            };
          }
          
          case 'remove_image': {
            const { imageId, force } = args as { imageId: string; force?: boolean };
            await this.dockerClient.removeImage(imageId, force);
            return {
              content: [{ type: 'text', text: `Image ${imageId} removed successfully` }],
            };
          }
          
          // Network operations
          case 'list_networks': {
            const networks = await this.dockerClient.listNetworks();
            return {
              content: [{ type: 'text', text: JSON.stringify(networks, null, 2) }],
            };
          }
          
          case 'create_network': {
            const { name, driver, internal } = args as { 
              name: string; 
              driver?: string;
              internal?: boolean;
            };
            
            const result = await this.dockerClient.createNetwork(name, {
              Driver: driver,
              Internal: internal
            });
            
            return {
              content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
          }
          
          case 'remove_network': {
            const { networkId } = args as { networkId: string };
            await this.dockerClient.removeNetwork(networkId);
            return {
              content: [{ type: 'text', text: `Network ${networkId} removed successfully` }],
            };
          }
          
          // Volume operations
          case 'list_volumes': {
            const volumes = await this.dockerClient.listVolumes();
            return {
              content: [{ type: 'text', text: JSON.stringify(volumes, null, 2) }],
            };
          }
          
          case 'create_volume': {
            const { name, driver, labels } = args as { 
              name: string; 
              driver?: string;
              labels?: Record<string, string>;
            };
            
            const result = await this.dockerClient.createVolume(name, {
              Driver: driver,
              Labels: labels
            });
            
            return {
              content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
            };
          }
          
          case 'remove_volume': {
            const { name, force } = args as { name: string; force?: boolean };
            await this.dockerClient.removeVolume(name, force);
            return {
              content: [{ type: 'text', text: `Volume ${name} removed successfully` }],
            };
          }
          
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) throw error;
        throw new McpError(
          ErrorCode.InternalError,
          error instanceof Error ? error.message : 'Unknown error occurred'
        );
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Docker MCP server running on stdio');
  }
}

const server = new DockerServer();
server.run().catch(console.error);
