# Docker Deployment Guide - AI Service

This guide explains how to build and deploy the AI Service using Docker.

## Quick Start

### Build the Image

```bash
cd incident-response-orchestrator
docker build -f Dockerfile -t ai-service:latest .
```

### Run with Docker Compose (Recommended)

```bash
# With Redis cache
docker-compose -f docker-compose.ai.yml up -d

# Check logs
docker-compose -f docker-compose.ai.yml logs -f ai-service
```

### Run Standalone

```bash
docker run -p 5000:5000 \
  -e GROQ_API_KEY=your_key_here \
  -e FLASK_ENV=production \
  ai-service:latest
```

---

## Docker Build Details

### Multi-Stage Build

The Dockerfile uses a two-stage build process for optimization:

**Stage 1: Builder**
- Installs build dependencies
- Creates Python wheels for all requirements
- Result: ~500MB intermediate image

**Stage 2: Runtime**
- Starts from clean python:3.9-slim image
- Installs only wheels (no compilation needed)
- Adds non-root user for security
- Final size: ~800MB-1GB (depending on dependencies)

### Build Optimization

- Uses `.dockerignore` to exclude unnecessary files
- Wheel caching for faster rebuilds
- Minimal runtime dependencies
- Non-root user execution (security best practice)

---

## Environment Variables

Required when running container:

```bash
GROQ_API_KEY=gsk_your_api_key_here
FLASK_ENV=production
FLASK_PORT=5000
REDIS_HOST=redis
REDIS_PORT=6379
```

### Create .env file

```bash
cat > .env.docker << EOF
cat > .env.docker << EOF
# IMPORTANT: Replace the placeholder below with your GROQ API key.
# Do NOT commit real secrets into source control.
GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE
FLASK_ENV=production
FLASK_PORT=5000
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
EOF
```

### Pass to docker-compose

```bash
docker-compose -f docker-compose.ai.yml --env-file .env.docker up -d
```

---

## Docker Compose Configuration

### ai-service container

- **Image**: Built from local Dockerfile
- **Port**: 5000 (mapped to host 5000)
- **Depends on**: Redis
- **Health Check**: HTTP GET /health every 30s
- **Volumes**: Persists ChromaDB data
- **Networks**: ai-network bridge network
- **Restart**: Always (unless explicitly stopped)

### redis container

- **Image**: redis:7-alpine (minimal Redis image)
- **Port**: 6379 (mapped to host 6379)
- **Volumes**: Persists data to redis-data volume
- **Health Check**: redis-cli ping every 10s
- **Restart**: Always

---

## Usage Examples

### Check Service Health

```bash
docker-compose -f docker-compose.ai.yml ps

# Expected output shows both services as "Up"
```

### View Logs

```bash
# All services
docker-compose -f docker-compose.ai.yml logs

# Only AI service
docker-compose -f docker-compose.ai.yml logs ai-service

# Follow logs in real-time
docker-compose -f docker-compose.ai.yml logs -f ai-service
```

### Test Endpoint

```bash
curl -X POST http://localhost:5000/api/describe \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Incident",
    "incident_type": "ransomware",
    "severity": "high",
    "description": "Test attack detection"
  }'
```

### Stop Services

```bash
docker-compose -f docker-compose.ai.yml down

# Stop and remove volumes
docker-compose -f docker-compose.ai.yml down -v
```

### Restart Services

```bash
docker-compose -f docker-compose.ai.yml restart
```

---

## Production Deployment

### Using Gunicorn Workers

The default CMD in Dockerfile uses Gunicorn with:
- **Workers**: 4 (adjust based on CPU cores: `4 * CPU_count`)
- **Timeout**: 60 seconds (adjust for long-running requests)
- **Max Requests**: 1000 (restart workers periodically for memory cleanup)
- **Worker Class**: sync (change to gevent for async if needed)

### Kubernetes Deployment

Example Kubernetes deployment YAML:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-service
  template:
    metadata:
      labels:
        app: ai-service
    spec:
      containers:
      - name: ai-service
        image: ai-service:latest
        ports:
        - containerPort: 5000
        env:
        - name: GROQ_API_KEY
          valueFrom:
            secretKeyRef:
              name: groq-secrets
              key: api-key
        - name: FLASK_ENV
          value: "production"
        - name: REDIS_HOST
          value: "redis-service"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 40
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
```

### Environment-Specific Configuration

**Development**:
```bash
docker-compose -f docker-compose.ai.yml up -d
```

**Staging**:
```bash
docker build -t ai-service:staging .
docker run -e FLASK_ENV=staging -p 5000:5000 ai-service:staging
```

**Production**:
```bash
docker build -t ai-service:1.0.0 .
docker run \
  -e FLASK_ENV=production \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  -p 5000:5000 \
  --restart always \
  ai-service:1.0.0
```

---

## Troubleshooting

### Service Fails to Start

```bash
# Check logs
docker-compose -f docker-compose.ai.yml logs ai-service

# Common issue: Missing GROQ_API_KEY
# Solution: Set environment variable before running
export GROQ_API_KEY=your_key_here
docker-compose -f docker-compose.ai.yml up -d
```

### Redis Connection Error

```
ERROR: error during connect: this error may indicate that 
the docker daemon is not running
```

**Solution**: Ensure Docker daemon is running
```bash
docker version  # Test if Docker is running
```

### Out of Memory

```bash
# Increase Docker memory allocation
docker update --memory 4g ai-service
```

### Health Check Failing

```bash
# Check if service is responding
docker exec ai-service curl -f http://localhost:5000/health

# Check service logs for errors
docker-compose -f docker-compose.ai.yml logs ai-service
```

---

## Performance Optimization

### CPU & Memory

```bash
# Set resource limits
docker run \
  -m 2g \
  --cpus 2 \
  ai-service:latest
```

### Scaling

Use Docker Swarm or Kubernetes:

```bash
# Docker Swarm
docker service create \
  --replicas 3 \
  --limit-memory 2g \
  ai-service:latest

# Kubernetes (see YAML above)
kubectl apply -f ai-service-deployment.yaml
```

### Volume Optimization

Use named volumes for better performance:

```bash
docker volume create ai-service-data
docker run -v ai-service-data:/app/chroma_data ai-service:latest
```

---

## Security Best Practices

### Implemented in Dockerfile

✅ Non-root user (appuser:1000)  
✅ Minimal base image (python:3.9-slim)  
✅ No sudo required  
✅ Read-only root filesystem (can be enabled)  

### Additional Recommendations

```bash
# Run with read-only root filesystem
docker run --read-only -v /tmp ai-service:latest

# Run without CAP_NET_RAW
docker run --cap-drop=NET_RAW ai-service:latest

# Use secrets manager for credentials
docker secret create groq_key <(echo $GROQ_API_KEY)
```

### Network Security

```bash
# Use custom network instead of host
docker network create ai-network
docker run --network ai-network ai-service:latest

# Restrict port exposure
docker run -p 127.0.0.1:5000:5000 ai-service:latest  # Local only
```

---

## Image Registry

### Docker Hub

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag ai-service:latest username/ai-service:latest
docker tag ai-service:latest username/ai-service:1.0.0

# Push to registry
docker push username/ai-service:latest
docker push username/ai-service:1.0.0
```

### Private Registry

```bash
# Tag for private registry
docker tag ai-service:latest registry.company.com/ai-service:latest

# Push to private registry
docker push registry.company.com/ai-service:latest
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t ai-service:${{ github.sha }} .
      
      - name: Push to registry
        run: |
          docker tag ai-service:${{ github.sha }} \
            registry.com/ai-service:latest
          docker push registry.com/ai-service:latest
```

---

## Monitoring & Logging

### Docker Logs

```bash
# View logs
docker logs ai-service

# Follow logs in real-time
docker logs -f ai-service

# Last 100 lines
docker logs --tail 100 ai-service

# With timestamps
docker logs -t ai-service
```

### Health Monitoring

```bash
# Check health status
docker inspect --format='{{json .State.Health}}' ai-service | jq

# Expected output when healthy:
# {"Status":"healthy","FailingStreak":0,"Runs":[...]}
```

### Log Aggregation

```bash
# Send logs to CloudWatch
docker run \
  --log-driver awslogs \
  --log-opt awslogs-group=/ecs/ai-service \
  ai-service:latest

# Send logs to ELK Stack
docker run \
  --log-driver splunk \
  --log-opt splunk-token=token \
  ai-service:latest
```

---

## Maintenance

### Prune Unused Images

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a
```

### Update Base Image

```bash
# Update to newer Python version
# Edit Dockerfile: FROM python:3.10-slim
docker build -t ai-service:latest .
```

### Rebuild from Cache

```bash
# Fast rebuild (uses cache)
docker build -t ai-service:latest .

# Fresh build (ignores cache)
docker build --no-cache -t ai-service:latest .
```

---

## Support & References

- **Docker Docs**: https://docs.docker.com/
- **Gunicorn Docs**: https://gunicorn.org/
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Redis Documentation**: https://redis.io/documentation

For issues or questions, refer to [README.md](./ai-service/README.md) or [DRY_RUN_REPORT.md](./ai-service/DRY_RUN_REPORT.md).
