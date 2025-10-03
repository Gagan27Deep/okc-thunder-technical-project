# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an OKC Thunder technical internship project featuring a full-stack basketball player statistics application with an Angular frontend, Django REST backend, and PostgreSQL database.

## Development Environment Setup

### PostgreSQL Database Setup
```bash
# Connect to PostgreSQL and set up database
psql -U postgres
create schema app;
alter user okcapplicant with password 'thunder';
grant all on schema app to okcapplicant;
```

Database connection configured in `backend/app/settings.py`:
- Database: `okc`
- User: `okcapplicant`
- Password: `thunder`
- Schema: `app` (search path: `app,public`)

### Backend (Django)

**Start backend server:**
```bash
cd backend
source okc/Scripts/activate  # Windows: okc\Scripts\activate
python manage.py runserver
```
Backend runs on http://localhost:8000/

**Run migrations:**
```bash
cd backend
source okc/Scripts/activate
python manage.py makemigrations
python manage.py migrate
```

**Database export (for submission):**
```bash
pg_dump -U okcapplicant okc > backend/scripts/dbexport.pgsql
```

### Frontend (Angular)

**Start frontend server:**
```bash
cd frontend
npm start
```
Frontend runs on http://localhost:4200/

**Note:** Project uses Angular 12.1.0 and Node 16.x, but may work with newer versions using `--force` flag.

## Architecture

### Backend Structure

**API Endpoint:**
- `GET /api/v1/playerSummary/{playerID}` - Returns player summary statistics and rankings
- Defined in `backend/app/urls.py`
- Handled by `PlayerSummary` view in `backend/app/views/players.py`

**Key Backend Files:**
- `backend/app/helpers/players.py` - Contains two main functions to implement:
  - `get_player_summary_stats(player_id)` - Query database and return player summary matching structure in `sample_summary_data.json`
  - `get_ranks(player_id, player_summary)` - Calculate stat rankings across all players
- `backend/app/dbmodels/models.py` - Define Django ORM models for database tables
- `backend/app/settings.py` - Django configuration, database settings
- `backend/raw_data/` - Source JSON data files:
  - `players.json` - Player information and detailed game statistics
  - `games.json` - Game metadata
  - `teams.json` - Team information

**Data Structure:**
The API response must include:
- Player totals: `totalShotAttempts`, `totalPoints`, `totalPasses`, `totalPotentialAssists`, `totalTurnovers`, `totalPassingTurnovers`
- Action counts: `pickAndRollCount`, `isolationCount`, `postUpCount`, `offBallScreenCount`
- Per-action breakdowns with individual shots/passes/turnovers (coordinates in feet from basket center)
- Rankings for all stats (suffix `Rank`)

### Frontend Structure

**Key Frontend Files:**
- `frontend/src/app/player-summary/` - Main component for displaying player data
  - `player-summary.component.ts` - Component logic
  - `player-summary.component.html` - Template
  - `player-summary.component.scss` - Styles
- `frontend/src/app/_services/players.service.ts` - API communication service
- `frontend/src/environments/environment.prod.ts` - Production backend URL (for Railway deployment)

**Court Coordinates:**
- Shots, passes, and turnovers have x/y coordinates in feet
- Coordinates relative to center of offensive basket (see `court_diagram.jpg`)

**Halfcourt Actions:**
- Pick & Roll
- Isolation
- Post-up
- Off-Ball Screen

## Project Deliverables

### Backend Tasks:
1. Design normalized PostgreSQL database schema for `backend/raw_data` files
2. Write database architecture description (<250 words) in `written_responses/`
3. Create data loading script in `backend/scripts/` that handles repeated runs without duplicates
4. Export database: `pg_dump -U okcapplicant okc > backend/scripts/dbexport.pgsql`
5. Implement `get_player_summary_stats()` in `backend/app/helpers/players.py`
6. Implement `get_ranks()` in `backend/app/helpers/players.py` (optional but recommended)

### Frontend Tasks:
1. Create TypeScript interface for API response in `frontend/src/app/player-summary/`
2. Design player summary UI
3. Deploy project and capture screenshots

### Deployment:
- Platform: Railway
- Must set `BACKEND_PUBLIC_DOMAIN` in `frontend/src/environments/environment.prod.ts`
- Add deployed URL to `SUBMISSION.md`

## Important Notes

- Database models use Django ORM and must be in `backend/app/dbmodels/models.py`
- All models use schema `app` (configured in settings)
- Data loading script must be idempotent (safe to run multiple times)
- Sample API response structure in `backend/app/helpers/sample_summary_data/sample_summary_data.json`
- Update `backend/requirements.txt` if adding Python dependencies
- Update `frontend/package.json` if adding npm dependencies
- Track AI prompts in `prompts/` directory if using AI assistance
