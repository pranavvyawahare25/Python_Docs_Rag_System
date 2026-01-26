# Docker Deployment Guide

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The app will be available at `http://localhost:8501`

### Using Docker CLI

```bash
# Build the image
docker build -t python-docs-rag .

# Run the container
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --name python-docs-rag-app \
  python-docs-rag

# View logs
docker logs -f python-docs-rag-app

# Stop and remove
docker stop python-docs-rag-app
docker rm python-docs-rag-app
```

## Features

✅ **Self-contained** - All dependencies included  
✅ **Auto-download** - Vector store downloads automatically on first run  
✅ **Persistent data** - Vector store cached in mounted volume  
✅ **Health checks** - Automatic container health monitoring  
✅ **Easy deployment** - One command to start

## Configuration

### Environment Variables

You can customize the deployment with environment variables:

```bash
docker run -d \
  -p 8501:8501 \
  -e STREAMLIT_SERVER_PORT=8501 \
  -e STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
  python-docs-rag
```

### Custom Port

To run on a different port (e.g., 8080):

```bash
docker run -d -p 8080:8501 python-docs-rag
```

Then access at `http://localhost:8080`

## Production Deployment

### With Vector Store Pre-loaded

If you want to include the vector store in the image:

1. **Uncomment in Dockerfile**:
   ```dockerfile
   # Copy pre-built vector store (optional)
   COPY data/vector_store /app/data/vector_store
   ```

2. **Rebuild**:
   ```bash
   docker build -t python-docs-rag .
   ```

### Deploy to Cloud

#### Docker Hub

```bash
# Tag the image
docker tag python-docs-rag your-username/python-docs-rag:latest

# Push to Docker Hub
docker push your-username/python-docs-rag:latest

# Run from anywhere
docker run -d -p 8501:8501 your-username/python-docs-rag:latest
```

#### AWS ECS / Google Cloud Run / Azure Container Instances

Upload your image to the respective container registry and deploy using their web console or CLI.

## Troubleshooting

### Container won't start

Check logs:
```bash
docker logs python-docs-rag-app
```

### Port already in use

Change the host port:
```bash
docker run -d -p 8502:8501 python-docs-rag
```

### Vector store not downloading

- Check internet connectivity inside container
- Verify GitHub release URL in `app.py`
- Check container logs for error messages

### Out of memory

Increase Docker memory limit:
- Docker Desktop → Settings → Resources → Memory
- Increase to at least 2GB

## Development

### Rebuild after changes

```bash
# With docker-compose
docker-compose up --build

# With docker
docker build -t python-docs-rag . && docker run -p 8501:8501 python-docs-rag
```

### Interactive shell

```bash
docker run -it python-docs-rag /bin/bash
```

## Image Size

Expected size: ~2.5 GB
- Base Python image: ~1.5 GB
- Dependencies: ~1 GB
- Application code: ~5 MB

To reduce size, use `python:3.8-alpine` (builds may be slower).
