# Docker Setup Guide for JobVite Crowler

This guide explains how to run the JobVite Crowler using Docker and Docker Compose.

## Quick Start

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure your settings in `.env`:**
   ```bash
   FTP_HOST=your-ftp-server.com
   FTP_USERNAME=your-username
   FTP_PASSWORD=your-password
   FTP_DIRECTORY=/target/path
   HOURS_DELAY=24
   BUILD_TARGET=production
   ```

3. **Build and run:**
   ```bash
   docker-compose up -d
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f crowler
   ```

## Configuration

All configuration is managed through the `.env` file in the root directory:

### Build Target
- `production` (default): Runs the crawler as a background service with scheduled job synchronization
- `development`: Keeps the container running for manual testing

### FTP Settings
- `FTP_HOST`: Your FTP server address
- `FTP_USERNAME`: FTP login username
- `FTP_PASSWORD`: FTP login password
- `FTP_DIRECTORY`: Target directory on FTP server (e.g., `/public_html/jobs`)

### Scheduler
- `HOURS_DELAY`: Interval between job synchronization runs (in hours)
  - `24` = once per day
  - `6` = every 6 hours
  - `1` = every hour

### Service (Windows only)
- `SERVICE_NAME`: Name for Windows service installation
- `SERVICE_DESCRIPTION`: Description for Windows service

## Directory Structure

The Docker setup creates and manages these directories:

```
./Crowler/
├── jobs/              # Output directory for scraped job data (mounted in container)
│   ├── jobs.json      # Main jobs data file
│   └── [job-id].html  # Individual job descriptions
└── logs/              # Container logs (if enabled)
```

These directories are created automatically and mounted from your local machine, so data persists between container restarts.

## Commands

### Start the service
```bash
docker-compose up -d
```

### Stop the service
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f crowler
```

### View specific number of log lines
```bash
docker-compose logs --tail=100 crowler
```

### Rebuild the image
```bash
docker-compose build --no-cache
```

### Run a one-time job sync (production mode)
```bash
docker-compose exec crowler python crowler.py
```

### Run in development mode (interactive)
```bash
# Update .env: BUILD_TARGET=development
docker-compose up -d
docker-compose exec crowler /bin/bash
# Inside container, run commands like:
# python crowler.py
# python -c "import os; print(os.getenv('FTP_HOST'))"
```

## Production Deployment

### Environment File Security
Create a `.env` file (not `.env.example`) with your actual credentials:

```bash
cp .env.example .env
# Edit .env with your real FTP credentials
chmod 600 .env  # Restrict file permissions (Linux/macOS)
```

### Running as a Service

On Linux systems with systemd, create a service file:

**`/etc/systemd/system/jobvite-crowler.service`**
```ini
[Unit]
Description=JobVite Crowler Service
Requires=docker.service
After=docker.service

[Service]
Type=simple
WorkingDirectory=/path/to/JobViteCrowler
ExecStart=/usr/bin/docker-compose up
ExecStop=/usr/bin/docker-compose down
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable jobvite-crowler
sudo systemctl start jobvite-crowler
sudo systemctl status jobvite-crowler
```

### Monitoring

Check container health:
```bash
docker ps
docker-compose ps
```

View resource usage:
```bash
docker stats jobvite-crowler
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs crowler
```
Check for environment variable errors or missing FTP credentials.

### Jobs not being scraped
1. Verify FTP credentials in `.env`
2. Check internet connectivity
3. Verify Jobvite page structure hasn't changed
4. Check container logs: `docker-compose logs -f crowler`

### FTP upload failing
- Verify `FTP_HOST`, `FTP_USERNAME`, `FTP_PASSWORD` are correct
- Check that `FTP_DIRECTORY` exists on the FTP server
- Verify FTP server allows your IP address

### Container using too much memory
Adjust Docker resources in `docker-compose.yml`:
```yaml
crowler:
  # ... other settings ...
  deploy:
    resources:
      limits:
        memory: 512m
      reservations:
        memory: 256m
```

## Development Workflow

For development and testing:

1. Set `BUILD_TARGET=development` in `.env`
2. Start container: `docker-compose up -d`
3. Enter shell: `docker-compose exec crowler /bin/bash`
4. Run commands:
   ```bash
   python crowler.py              # Test scraping
   echo $FTP_HOST                 # Verify env vars
   ls -la /app/jobs               # Check output
   ```

## Volumes

The following directories are mounted between your machine and the container:

| Local Path | Container Path | Purpose |
|-----------|---------------|---------|
| `./Crowler/jobs` | `/app/jobs` | Scraped job data output |
| `./Crowler/logs` | `/app/logs` | Application logs |

Data in these directories persists between container restarts.

## Docker Image Details

The Docker image is built from `Crowler/Dockerfile` with the following characteristics:

- **Base Image**: Python 3.11-slim
- **System Dependencies**: Chromium, ChromeDriver, curl
- **Python Dependencies**: Installed from `pyproject.toml` (Selenium, python-dotenv)
- **Size**: Approximately 500-600MB (production), includes browser automation

### Image Stages

- **base**: Contains Python runtime and all dependencies
- **production**: Runs `python main.py` (background scheduler)
- **development**: Keeps container running for interactive use

## Security Notes

1. **Never commit `.env` file** - use `.env.example` as template
2. **FTP credentials** - use strong passwords, consider environment-specific credentials
3. **Docker socket** - don't expose docker socket unless necessary
4. **Logs** - may contain sensitive data, review log retention policy

## Performance Optimization

For high-frequency scraping or large job databases:

1. Increase `HOURS_DELAY` to avoid overwhelming FTP server
2. Monitor container resource usage: `docker stats`
3. Enable log rotation (already configured in docker-compose.yml)
4. Consider separating job scraping from FTP upload

## See Also

- [Main README](./README.md) - Project overview
- `Crowler/.env.example` - Backend-specific configuration
- `docker-compose.yml` - Docker Compose configuration
