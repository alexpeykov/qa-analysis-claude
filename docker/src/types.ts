export interface DockerContainer {
  Id: string;
  Names: string[];
  Image: string;
  ImageID: string;
  Command: string;
  Created: number;
  State: string;
  Status: string;
  Ports: DockerPort[];
  Labels: Record<string, string>;
  NetworkSettings: {
    Networks: Record<string, DockerNetwork>;
  };
  Mounts: DockerMount[];
}

export interface DockerPort {
  IP?: string;
  PrivatePort?: number;
  PublicPort?: number;
  Type: string;
}

export interface DockerNetwork {
  IPAddress: string;
  Gateway: string;
  IPPrefixLen: number;
  MacAddress: string;
}

export interface DockerMount {
  Type: string;
  Source: string;
  Destination: string;
  Mode: string;
  RW: boolean;
  Propagation: string;
}

export interface DockerImage {
  Id: string;
  RepoTags: string[];
  RepoDigests: string[];
  Created: number;
  Size: number;
  VirtualSize: number;
  SharedSize: number;
  Labels: Record<string, string>;
  Containers: number;
}

export interface DockerVolume {
  Name: string;
  Driver: string;
  Mountpoint: string;
  CreatedAt: string;
  Status: Record<string, string>;
  Labels: Record<string, string>;
  Scope: string;
  Options: Record<string, string>;
}

export interface DockerNetworkInfo {
  Name: string;
  Id: string;
  Created: string;
  Scope: string;
  Driver: string;
  EnableIPv6: boolean;
  IPAM: {
    Driver: string;
    Options: Record<string, string>;
    Config: Array<{
      Subnet: string;
      Gateway: string;
    }>;
  };
  Internal: boolean;
  Attachable: boolean;
  Ingress: boolean;
  ConfigFrom: {
    Network: string;
  };
  ConfigOnly: boolean;
  Containers: Record<string, {
    Name: string;
    EndpointID: string;
    MacAddress: string;
    IPv4Address: string;
    IPv6Address: string;
  }>;
  Options: Record<string, string>;
  Labels: Record<string, string>;
}

export interface ContainerStats {
  cpu_percentage: number;
  memory_usage: string;
  memory_limit: string;
  memory_percentage: number;
  network_rx: string;
  network_tx: string;
  block_read: string;
  block_write: string;
}

export interface CreateContainerOptions {
  name: string;
  Image: string;
  Env?: string[];
  Cmd?: string[];
  ExposedPorts?: Record<string, {}>;
  HostConfig?: {
    PortBindings?: Record<string, Array<{HostPort: string}>>;
    Binds?: string[];
    NetworkMode?: string;
    RestartPolicy?: {
      Name: string;
      MaximumRetryCount?: number;
    };
  };
  Labels?: Record<string, string>;
}
