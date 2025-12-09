import Docker, { DockerOptions } from 'dockerode';
import { getConfig } from './config.js';
import type {
  DockerContainer,
  DockerImage,
  DockerVolume,
  DockerNetworkInfo,
  ContainerStats,
  CreateContainerOptions
} from './types.js';

export class DockerClient {
  private docker: Docker;
  private projectPrefix: string;

  constructor() {
    const config = getConfig();
    this.projectPrefix = config.projectPrefix || 'mcp-';
    
    // Initialize Docker client with configuration
    this.docker = new Docker(config as DockerOptions);
  }

  // Helper to format container names with project prefix
  private formatName(name: string, projectName?: string): string {
    if (name.startsWith('/')) {
      name = name.substring(1);
    }
    
    if (projectName && !name.includes(projectName)) {
      return `${this.projectPrefix}${projectName}-${name}`;
    }
    
    return name;
  }

  // Helper to parse container names
  private parseContainerName(name: string): string {
    if (name.startsWith('/')) {
      return name.substring(1);
    }
    return name;
  }

  // Helper to format bytes to human-readable format
  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    
    return `${parseFloat((bytes / Math.pow(1024, i)).toFixed(2))} ${sizes[i]}`;
  }

  // Container operations
  async listContainers(projectName?: string): Promise<DockerContainer[]> {
    const containers = await this.docker.listContainers({ all: true }) as DockerContainer[];
    
    if (projectName) {
      const prefix = `${this.projectPrefix}${projectName}-`;
      return containers.filter(container => 
        container.Names.some(name => this.parseContainerName(name).startsWith(prefix))
      );
    }
    
    return containers;
  }

  async createContainer(options: CreateContainerOptions, projectName?: string): Promise<{ id: string; name: string }> {
    if (projectName) {
      options.name = this.formatName(options.name, projectName);
      
      // Add project label
      options.Labels = {
        ...options.Labels,
        'mcp.project': projectName
      };
    }
    
    const container = await this.docker.createContainer(options);
    return { 
      id: container.id, 
      name: options.name 
    };
  }

  async runContainer(options: CreateContainerOptions, projectName?: string): Promise<{ id: string; name: string }> {
    const { id, name } = await this.createContainer(options, projectName);
    const container = this.docker.getContainer(id);
    await container.start();
    return { id, name };
  }

  async recreateContainer(containerId: string, options?: CreateContainerOptions): Promise<{ id: string; name: string }> {
    const container = this.docker.getContainer(containerId);
    const info = await container.inspect();
    
    // Stop and remove the container
    if (info.State.Running) {
      await container.stop();
    }
    await container.remove();
    
    // Create new container with same or updated options
    const newOptions: CreateContainerOptions = options || {
      name: this.parseContainerName(info.Name),
      Image: info.Config.Image,
      Env: info.Config.Env,
      Cmd: info.Config.Cmd,
      ExposedPorts: info.Config.ExposedPorts,
      HostConfig: info.HostConfig,
      Labels: info.Config.Labels
    };
    
    const newContainer = await this.docker.createContainer(newOptions);
    await newContainer.start();
    
    return { 
      id: newContainer.id, 
      name: newOptions.name 
    };
  }

  async startContainer(containerId: string): Promise<void> {
    const container = this.docker.getContainer(containerId);
    await container.start();
  }

  async stopContainer(containerId: string): Promise<void> {
    const container = this.docker.getContainer(containerId);
    await container.stop();
  }

  async removeContainer(containerId: string, force: boolean = false): Promise<void> {
    const container = this.docker.getContainer(containerId);
    await container.remove({ force });
  }

  async getContainerLogs(containerId: string, tail: number = 100): Promise<string> {
    const container = this.docker.getContainer(containerId);
    const logs = await container.logs({
      stdout: true,
      stderr: true,
      tail,
      follow: false
    });
    
    return logs.toString();
  }

  async getContainerStats(containerId: string): Promise<ContainerStats> {
    const container = this.docker.getContainer(containerId);
    const stats = await container.stats({ stream: false });
    
    // Calculate CPU usage percentage
    const cpuDelta = stats.cpu_stats.cpu_usage.total_usage - stats.precpu_stats.cpu_usage.total_usage;
    const systemCpuDelta = stats.cpu_stats.system_cpu_usage - stats.precpu_stats.system_cpu_usage;
    const cpuCount = stats.cpu_stats.online_cpus || 1;
    const cpuPercentage = (cpuDelta / systemCpuDelta) * cpuCount * 100;
    
    // Calculate memory usage
    const memoryUsage = stats.memory_stats.usage;
    const memoryLimit = stats.memory_stats.limit;
    const memoryPercentage = (memoryUsage / memoryLimit) * 100;
    
    // Network stats
    const networkStats = stats.networks ? Object.values(stats.networks).reduce(
      (acc: any, net: any) => {
        acc.rx_bytes += net.rx_bytes || 0;
        acc.tx_bytes += net.tx_bytes || 0;
        return acc;
      },
      { rx_bytes: 0, tx_bytes: 0 }
    ) : { rx_bytes: 0, tx_bytes: 0 };
    
    // Block I/O stats
    const ioStats = stats.blkio_stats?.io_service_bytes_recursive || [];
    const readBytes = ioStats.find((s: any) => s.op === 'Read')?.value || 0;
    const writeBytes = ioStats.find((s: any) => s.op === 'Write')?.value || 0;
    
    return {
      cpu_percentage: parseFloat(cpuPercentage.toFixed(2)),
      memory_usage: this.formatBytes(memoryUsage),
      memory_limit: this.formatBytes(memoryLimit),
      memory_percentage: parseFloat(memoryPercentage.toFixed(2)),
      network_rx: this.formatBytes(networkStats.rx_bytes),
      network_tx: this.formatBytes(networkStats.tx_bytes),
      block_read: this.formatBytes(readBytes),
      block_write: this.formatBytes(writeBytes)
    };
  }

  // Image operations
  async listImages(): Promise<DockerImage[]> {
    return this.docker.listImages() as Promise<DockerImage[]>;
  }

  async pullImage(imageName: string): Promise<void> {
    const stream = await this.docker.pull(imageName);
    
    await new Promise<void>((resolve, reject) => {
      this.docker.modem.followProgress(stream, (err: Error | null, output: any[]) => {
        if (err) return reject(err);
        resolve();
      });
    });
  }

  async pushImage(imageName: string): Promise<void> {
    const image = this.docker.getImage(imageName);
    const stream = await image.push({});
    
    await new Promise<void>((resolve, reject) => {
      this.docker.modem.followProgress(stream, (err: Error | null, output: any[]) => {
        if (err) return reject(err);
        resolve();
      });
    });
  }

  async buildImage(tarContext: string, options: { t: string, dockerfile?: string }): Promise<void> {
    const stream = await this.docker.buildImage(tarContext, options);
    
    await new Promise<void>((resolve, reject) => {
      this.docker.modem.followProgress(stream, (err: Error | null, output: any[]) => {
        if (err) return reject(err);
        resolve();
      });
    });
  }

  async removeImage(imageId: string, force: boolean = false): Promise<void> {
    const image = this.docker.getImage(imageId);
    await image.remove({ force });
  }

  // Network operations
  async listNetworks(): Promise<DockerNetworkInfo[]> {
    return this.docker.listNetworks() as Promise<DockerNetworkInfo[]>;
  }

  async createNetwork(name: string, options: { Driver?: string, Internal?: boolean } = {}): Promise<{ id: string; name: string }> {
    const network = await this.docker.createNetwork({
      Name: name,
      Driver: options.Driver || 'bridge',
      Internal: options.Internal || false
    });
    
    return { 
      id: network.id, 
      name 
    };
  }

  async removeNetwork(networkId: string): Promise<void> {
    const network = this.docker.getNetwork(networkId);
    await network.remove();
  }

  // Volume operations
  async listVolumes(): Promise<DockerVolume[]> {
    const volumes = await this.docker.listVolumes();
    return volumes.Volumes as DockerVolume[];
  }

  async createVolume(name: string, options: { Driver?: string, Labels?: Record<string, string> } = {}): Promise<{ name: string }> {
    const volume = await this.docker.createVolume({
      Name: name,
      Driver: options.Driver || 'local',
      Labels: options.Labels || {}
    });
    
    return { name: volume.Name };
  }

  async removeVolume(name: string, force: boolean = false): Promise<void> {
    const volume = this.docker.getVolume(name);
    await volume.remove({ force });
  }
}
