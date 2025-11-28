# JobVite Crowler

An automated job aggregation platform that crawls Lean Tech's Jobvite careers page and presents job listings through a modern web interface with built-in admin controls.

## Overview

JobVite Crowler is a full-stack application that:
- **Automatically crawls** job listings from Jobvite using Selenium web automation
- **Collects and stores** job data with detailed descriptions
- **Deploys** both frontend and data via FTP to a web server
- **Provides** a React-based web interface for browsing jobs
- **Includes** an admin panel for triggering manual job synchronization
- **Integrates** WhatsApp for direct job applications

## Features

### Backend (Python Crawler)
- Headless browser automation with Selenium to scrape Jobvite careers page
- Automatic job discovery and detailed description extraction
- Scheduled background synchronization with configurable intervals
- FTP deployment for both job data and website files
- Windows/Linux service management capabilities
- Environment-based configuration for security and flexibility

### Frontend (React Web Interface)
- Responsive job listing page with grid layout
- Detailed job view with full descriptions
- Job metadata (sector, work mode, country) display
- Admin panel for manual job synchronization
- WhatsApp integration for quick job applications
- Error boundaries and graceful error handling

## Project Structure

```
JobViteCrowler/
├── Crowler/              # Python backend crawler & service
│   ├── crowler.py        # Web scraper using Selenium
│   ├── main.py           # Service entry point with scheduling
│   ├── ftptransfer.py    # FTP upload for job data
│   ├── deploy.py         # FTP deployment for website files
│   ├── service_manager.py # Windows/Linux service management
│   ├── pyproject.toml    # Python dependencies
│   └── .env.example      # Environment variables template
│
└── Site/                 # React + TypeScript frontend
    ├── src/
    │   ├── Pages/        # Main pages (Jobs, Detail, Admin)
    │   ├── components/   # Shared React components
    │   ├── services/     # API client and data fetching
    │   └── assets/       # Static assets
    ├── vite.config.ts    # Vite build configuration
    ├── tsconfig.json     # TypeScript configuration
    └── package.json      # Node dependencies
```

## Technology Stack

### Backend
- **Python 3.11+** - Runtime environment
- **Selenium 4.35.0** - Web scraping and browser automation
- **python-dotenv** - Environment variable management
- **FTP** - File transfer protocol for deployment

### Frontend
- **React 19.1.1** - UI framework
- **TypeScript 5.8** - Type safety
- **Vite 7.1** - Build tool and dev server
- **React Router 7.9** - Client-side routing
- **Axios 1.12** - HTTP client

## Getting Started

### Prerequisites
- Python 3.11 or higher
- Node.js 18+ and npm/yarn
- FTP credentials (for deployment)
- Chrome/Chromium browser and ChromeDriver

### Backend Setup

1. Navigate to the Crowler directory:
   ```bash
   cd Crowler
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or with uv
   uv sync
   ```

3. Create environment file from template:
   ```bash
   cp .env.example .env
   ```

4. Configure environment variables in `.env`:
   ```
   FTP_HOST=your-ftp-host.com
   FTP_USERNAME=your-username
   FTP_PASSWORD=your-password
   FTP_DIRECTORY=/path/on/ftp/server
   CHROME_DRIVER_PATH=/path/to/chromedriver
   HOURS_DELAY=24
   SERVICE_NAME=JobViteCrowler
   ```

5. Run the crawler:
   ```bash
   python crowler.py          # Single run
   python main.py             # Continuous background service
   ```

### Frontend Setup

1. Navigate to the Site directory:
   ```bash
   cd Site
   ```

2. Install dependencies:
   ```bash
   npm install
   # or with yarn
   yarn install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Build for production:
   ```bash
   npm run build
   ```

## Usage

### Running the Crawler

**Single job sync:**
```bash
python Crowler/crowler.py
```
This will scrape the Jobvite page and save results to `jobs.json` with individual descriptions in the `jobs/` directory.

**Continuous background service:**
```bash
python Crowler/main.py
```
Runs as a background service, synchronizing jobs at intervals specified by `HOURS_DELAY`.

### Installing as System Service (Windows)

```bash
python Crowler/service_manager.py install
python Crowler/service_manager.py start
```

### Deploying to FTP

Deploy all files (frontend + job data):
```bash
python Crowler/deploy.py
```

Upload only job data:
```bash
python Crowler/ftptransfer.py
```

### Web Interface

Once the frontend is running:
- **Jobs Page:** Browse all available job listings
- **Detail Page:** View complete job description and metadata
- **Admin Panel:** Trigger manual job synchronization
- **WhatsApp Apply:** Direct messaging integration for job applications

## API Endpoints

The backend exposes the following endpoints:

- `GET /jobs` - Retrieve all jobs with last updated timestamp
- `GET /jobs/{id}` - Get specific job details
- `POST /sync` - Trigger job synchronization (called by admin panel)

API base URL is configured in `Site/src/services/api.ts` (default: `http://localhost:8000`)

## Configuration

### Environment Variables

All sensitive configuration is stored in `.env`:

| Variable | Description | Example |
|----------|-------------|---------|
| `FTP_HOST` | FTP server hostname | `ftp.example.com` |
| `FTP_USERNAME` | FTP login username | `user` |
| `FTP_PASSWORD` | FTP login password | `password` |
| `FTP_DIRECTORY` | Target directory on FTP | `/public_html/jobs` |
| `CHROME_DRIVER_PATH` | Path to ChromeDriver | `/usr/local/bin/chromedriver` |
| `HOURS_DELAY` | Hours between syncs | `24` |
| `SERVICE_NAME` | Windows service name | `JobViteCrowler` |

## Data Structure

Jobs are stored in `jobs.json` with the following structure:

```json
{
  "jobs": [
    {
      "jobviteId": "unique-id",
      "jobTitle": "Position Title",
      "jobDescription": "HTML description (optional)",
      "sector": "Technology",
      "workMode": "Remote",
      "country": "United States"
    }
  ],
  "lastUpdated": "2025-11-24T10:30:00Z"
}
```

Individual job descriptions are stored as HTML files in the `jobs/` directory.

## Development

### Frontend Development

Start the Vite dev server for hot module reloading:
```bash
cd Site
npm run dev
```

The dev server runs on `http://localhost:5173` by default.

### Backend Development

Run the crawler script directly to test changes:
```bash
cd Crowler
python crowler.py
```

Watch the output for any errors or warnings.

### Linting & Type Checking

Frontend:
```bash
cd Site
npm run lint
```

## Deployment

### Production Build

1. Build the frontend:
   ```bash
   cd Site
   npm run build
   ```

2. Configure FTP credentials in `.env`

3. Deploy everything:
   ```bash
   cd Crowler
   python deploy.py
   ```

This will upload:
- Built React frontend from `Site/dist/`
- Job data and descriptions from Crowler

## Troubleshooting

### Jobs not being scraped
- Verify ChromeDriver path in `.env`
- Check Jobvite page structure hasn't changed
- Review crawler logs for errors

### FTP upload failures
- Verify FTP credentials and server accessibility
- Check directory permissions on FTP server
- Ensure `FTP_DIRECTORY` exists

### Frontend not loading job data
- Verify backend API is running and accessible
- Check API endpoint in `Site/src/services/api.ts`
- Review browser console for network errors

### Service won't start
- Check Windows Event Viewer for service errors
- Verify all environment variables are set correctly
- Ensure Python executable is in PATH

## Contributing

When making changes:
1. Test crawler output with `python crowler.py`
2. Build and test frontend with `npm run build`
3. Verify FTP deployment with test credentials
4. Update this README if adding features or changing configuration

## Recent Changes

- Included hidden/missing jobs in crawler
- Added description validation before upload
- Implemented FTP file transfer for descriptions
- Optimized JSON structure for performance
- Added Chrome driver path configuration

## License

[Add license information if applicable]

## Support

For issues or questions, please check:
1. Environment variables are correctly configured
2. ChromeDriver is compatible with your Chrome version
3. FTP server is accessible from your network
4. Required dependencies are installed (`pip install -r requirements.txt` for backend, `npm install` for frontend)
