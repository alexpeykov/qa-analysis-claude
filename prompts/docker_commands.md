# Docker Commands Prompts

This file contains useful prompts for working with Docker in the QA Analysis project.

## Container Management

### List All Containers
```
Show me all Docker containers (running and stopped)
```

### List Running Containers Only
```
Show me only the running Docker containers
```

### Start a Container
```
Start the Docker container named [container_name]
```

### Stop a Container
```
Stop the Docker container named [container_name]
```

### Restart a Container
```
Restart the Docker container named [container_name]
```

### Remove a Container
```
Remove the Docker container named [container_name] (force if running)
```

### View Container Logs
```
Show me the logs from container [container_name] (last 100 lines)
```

### Follow Container Logs (Real-time)
```
Show me real-time logs from container [container_name]
```

### Execute Command in Container
```
Execute the command [command] in the running container [container_name]
```

### Get Shell Access to Container
```
Open a bash shell in the running container [container_name]
```

### Inspect Container Details
```
Show me detailed information about container [container_name]
```

### View Container Resource Usage
```
Show me CPU and memory usage for all running containers
```

## Image Management

### List All Images
```
Show me all Docker images on this system
```

### Pull an Image
```
Pull the Docker image [image_name:tag] from the registry
```

### Remove an Image
```
Remove the Docker image [image_name:tag]
```

### Build an Image
```
Build a Docker image from [Dockerfile_path] with tag [image_name:tag]
```

### Inspect Image Details
```
Show me detailed information about the image [image_name:tag]
```

### View Image Layers
```
Show me the layers and history of image [image_name:tag]
```

### Remove Unused Images
```
Remove all dangling/unused Docker images
```

## Network Management

### List Networks
```
Show me all Docker networks
```

### Create a Network
```
Create a Docker network named [network_name]
```

### Inspect Network
```
Show me details about the Docker network [network_name]
```

### Connect Container to Network
```
Connect container [container_name] to network [network_name]
```

### Disconnect Container from Network
```
Disconnect container [container_name] from network [network_name]
```

## Volume Management

### List Volumes
```
Show me all Docker volumes
```

### Create a Volume
```
Create a Docker volume named [volume_name]
```

### Inspect Volume
```
Show me details about the Docker volume [volume_name]
```

### Remove a Volume
```
Remove the Docker volume [volume_name]
```

### Remove Unused Volumes
```
Remove all unused Docker volumes
```

## Docker Compose

### Start Services
```
Start all services defined in docker-compose.yml
```

### Start Specific Service
```
Start the [service_name] service from docker-compose.yml
```

### Stop Services
```
Stop all services defined in docker-compose.yml
```

### View Compose Logs
```
Show me logs from all docker-compose services
```

### Rebuild and Start Services
```
Rebuild and restart all services in docker-compose.yml
```

### Scale a Service
```
Scale the [service_name] service to [number] instances
```

### Remove Compose Services
```
Stop and remove all containers, networks, and volumes created by docker-compose
```

## System Management

### View System-wide Information
```
Show me Docker system information
```

### View Disk Usage
```
Show me Docker disk usage for images, containers, and volumes
```

### Clean Up System
```
Remove all stopped containers, unused networks, dangling images, and build cache
```

### Prune Everything
```
Remove all unused Docker resources (containers, networks, images, volumes)
```

## Project-Specific Prompts

### MySQL Container Management
```
Start the MySQL container for the QA analysis database
```

```
Show me the MySQL container logs for the last 50 lines
```

```
Connect to the MySQL container and open a MySQL shell
```

```
Execute the MySQL command [SQL_QUERY] in the database container
```

### Application Container Management
```
Start the QA analysis application container
```

```
Show me the application container logs in real-time
```

```
Restart the application container and show logs
```

```
Open a shell in the application container to debug
```

### Development Workflow
```
Stop all containers, rebuild the application image, and restart everything
```

```
Show me the status of all QA analysis project containers
```

```
Clean up all stopped containers and unused images for this project
```

```
Show me the environment variables in the [container_name] container
```

## Troubleshooting Prompts

### Container Not Starting
```
Help me troubleshoot why container [container_name] won't start - show me the logs and inspect configuration
```

### Port Conflicts
```
Check if port [port_number] is already in use and show me which process is using it
```

### Network Connectivity Issues
```
Help me debug network connectivity between containers [container1] and [container2]
```

### Permission Issues
```
Check and fix permission issues with Docker volumes for container [container_name]
```

### Database Connection Issues
```
Help me troubleshoot MySQL connection issues from the application container
```

## Advanced Use Cases

### Create Development Environment
```
Set up a complete development environment with MySQL, the application, and any necessary services using Docker
```

### Backup Database Container
```
Create a backup of the MySQL database from the container to a local file
```

### Restore Database Container
```
Restore the MySQL database in the container from backup file [backup_file]
```

### Monitor Container Health
```
Set up health checks and monitoring for all running containers
```

### Copy Files To/From Container
```
Copy the file [source_path] from my local machine to [destination_path] in container [container_name]
```

```
Copy the file [source_path] from container [container_name] to [destination_path] on my local machine
```

## Docker Build Optimization

### Analyze Image Size
```
Analyze the size of Docker image [image_name:tag] and suggest optimizations
```

### Multi-stage Build
```
Help me create a multi-stage Dockerfile to optimize the image size for [application_type]
```

### Build Cache Management
```
Clear Docker build cache and rebuild image [image_name:tag]
```

## Security and Best Practices

### Scan Image for Vulnerabilities
```
Scan the Docker image [image_name:tag] for security vulnerabilities
```

### Check Container Security
```
Review the security configuration of container [container_name] and suggest improvements
```

### Update Base Images
```
Check if the base images in my Dockerfiles have updates available
```

## Integration with CI/CD

### Build for Production
```
Build a production-ready Docker image with optimizations for deployment
```

### Tag and Push Image
```
Tag the image [image_name] as [new_tag] and push it to registry [registry_url]
```

### Run Tests in Container
```
Run the test suite inside a Docker container to ensure consistency
```
