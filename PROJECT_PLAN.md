# OKC Thunder Technical Project - Complete Implementation Plan

## Project Overview
Full-stack basketball statistics application with Django backend, Angular frontend, and PostgreSQL database.

---

## ✅ COMPLETED TASKS

### Backend - Database & API
- [x] **Database Schema Design**
  - Created 6 normalized tables: Teams, Games, Players, Shots, Passes, Turnovers
  - Implemented foreign key relationships

- [x] **Django Models** (`backend/app/dbmodels/models.py`)
  - Team, Game, Player, Shot, Pass, Turnover models

- [x] **Database Migrations**
  - `python manage.py makemigrations` ✓
  - `python manage.py migrate` ✓

- [x] **Data Loading Script** (`backend/scripts/load_data.py`)
  - Idempotent (can run multiple times)
  - Loads 10 teams, 39 games, 10 players, 192 shots, 165 passes, 14 turnovers

- [x] **Database Architecture Documentation** (`written_responses/database_architecture.md`)
  - 248 words describing normalized schema

- [x] **API Implementation** (`backend/app/helpers/players.py`)
  - `get_player_summary_stats()` - queries database and returns player stats
  - `get_ranks()` - calculates rankings across all players

---

## 🔄 IN PROGRESS / PENDING TASKS

### 1. Database Export (MANUAL STEP REQUIRED)
**Status:** Needs manual execution
**Location:** `backend/scripts/dbexport.pgsql`

**Command to run:**
```bash
cd backend/scripts
pg_dump -U okcapplicant okc > dbexport.pgsql
```
**Password:** `thunder`

**Why manual:** Command requires interactive password input

---

### 2. Backend API Testing
**Status:** Ready to test
**API Endpoint:** `GET /api/v1/playerSummary/{playerID}`

**Test URLs:**
- http://localhost:8000/api/v1/playerSummary/0 (Michael Jordan)
- http://localhost:8000/api/v1/playerSummary/1 (Pound)
- http://localhost:8000/api/v1/playerSummary/2 (Buddy)

**Expected Response Structure:**
```json
{
  "name": "Player Name",
  "playerID": 0,
  "totalShotAttempts": 20,
  "totalPoints": 23,
  "totalPasses": 19,
  "totalPotentialAssists": 5,
  "totalTurnovers": 1,
  "totalPassingTurnovers": 1,
  "pickAndRollCount": 31,
  "isolationCount": 4,
  "postUpCount": 0,
  "offBallScreenCount": 4,
  "totalShotAttemptsRank": 3,
  "totalPointsRank": 2,
  ...
  "pickAndRoll": { /* detailed stats */ },
  "isolation": { /* detailed stats */ },
  "postUp": { /* detailed stats */ },
  "offBallScreen": { /* detailed stats */ }
}
```

---

### 3. Frontend - TypeScript Interface
**Status:** Not started
**Location:** `frontend/src/app/player-summary/`

**Task:** Create TypeScript interface that matches API response

**File to create:** `frontend/src/app/player-summary/player-summary.interface.ts`

**Implementation:**
```typescript
export interface PlayerSummary {
  name: string;
  playerID: number;
  totalShotAttempts: number;
  totalPoints: number;
  totalPasses: number;
  totalPotentialAssists: number;
  totalTurnovers: number;
  totalPassingTurnovers: number;
  pickAndRollCount: number;
  isolationCount: number;
  postUpCount: number;
  offBallScreenCount: number;

  // Rankings
  totalShotAttemptsRank: number;
  totalPointsRank: number;
  totalPassesRank: number;
  totalPotentialAssistsRank: number;
  totalTurnoversRank: number;
  totalPassingTurnoversRank: number;
  pickAndRollCountRank: number;
  isolationCountRank: number;
  postUpCountRank: number;
  offBallScreenCountRank: number;

  // Action breakdowns
  pickAndRoll: ActionStats;
  isolation: ActionStats;
  postUp: ActionStats;
  offBallScreen: ActionStats;
}

export interface ActionStats {
  totalShotAttempts: number;
  totalPoints: number;
  totalPasses: number;
  totalPotentialAssists: number;
  totalTurnovers: number;
  totalPassingTurnovers: number;
  shots: Shot[];
  passes: Pass[];
  turnovers: Turnover[];
}

export interface Shot {
  loc: [number, number];  // [x, y] coordinates in feet
  points: number;
}

export interface Pass {
  startLoc: [number, number];
  endLoc: [number, number];
  isCompleted: boolean;
  isPotentialAssist: boolean;
  isTurnover: boolean;
}

export interface Turnover {
  loc: [number, number];
}
```

---

### 4. Frontend - UI Design & Implementation
**Status:** Not started
**Files to modify:**
- `frontend/src/app/player-summary/player-summary.component.ts`
- `frontend/src/app/player-summary/player-summary.component.html`
- `frontend/src/app/player-summary/player-summary.component.scss`

**Requirements:**
1. Display player name and overall statistics
2. Show rankings for each stat
3. Visualize shots, passes, and turnovers on a court diagram
4. Break down stats by action type (Pick & Roll, Isolation, Post-up, Off-Ball Screen)
5. Allow input of different player IDs
6. Responsive design

**Suggested Features:**
- Court visualization using SVG or Canvas
- Color-coded shots (made vs missed)
- Pass visualization with arrows
- Stats table with rankings
- Action type selector/tabs
- Shot chart heat map

**Component Updates:**
```typescript
// player-summary.component.ts
import { PlayerSummary } from './player-summary.interface';

export class PlayerSummaryComponent implements OnInit {
  playerSummary: PlayerSummary | null = null;
  playerID: number = 0;
  loading: boolean = false;
  error: string | null = null;

  ngOnInit(): void {
    this.loadPlayerData(this.playerID);
  }

  loadPlayerData(playerID: number): void {
    this.loading = true;
    this.playersService.getPlayerSummary(playerID)
      .pipe(untilDestroyed(this))
      .subscribe({
        next: (data) => {
          this.playerSummary = data.apiResponse;
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to load player data';
          this.loading = false;
        }
      });
  }
}
```

---

### 5. Frontend - Start Development Server
**Status:** Not started
**Command:**
```bash
cd frontend
npm start
```
**Access:** http://localhost:4200/player-summary

---

### 6. Local Testing
**Status:** Not started

**Checklist:**
- [ ] Backend running on http://localhost:8000/
- [ ] Frontend running on http://localhost:4200/
- [ ] API returns correct data for all players (IDs 0-9)
- [ ] Frontend displays player stats correctly
- [ ] Court visualization works
- [ ] Player ID input works
- [ ] Rankings display correctly
- [ ] All action types show correct breakdowns

---

### 7. Deployment to Railway
**Status:** Not started

#### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
```

#### Step 2: Login to Railway
```bash
railway login
```

#### Step 3: Initialize Railway Project
```bash
railway init
```
**Project name:** `{githubusername}-thunder-2025`

#### Step 4: Add PostgreSQL Database
```bash
railway add --database postgres --service database
```
Wait for deployment to complete.

#### Step 5: Add Backend Service
```bash
railway add \
  --service backend \
  --variables 'DATABASE_URL=${{Postgres.DATABASE_URL}}' \
  --variables 'PGDATABASE=${{Postgres.PGDATABASE}}' \
  --variables 'PGHOST=${{Postgres.PGHOST}}' \
  --variables 'PGPASSWORD=${{Postgres.PGPASSWORD}}' \
  --variables 'PGPORT=${{Postgres.PGPORT}}' \
  --variables 'PGUSER=${{Postgres.PGUSER}}' \
  --variables 'DJANGO_SETTINGS_MODULE=app.settings'
```

#### Step 6: Configure Backend Service
In Railway web interface:
1. Click "backend" service
2. Settings → Source → Connect Repo → Select your GitHub repo
3. Settings → Source → Root Directory → `backend`
4. Networking → Generate Domain
5. Copy the generated domain (e.g., `https://backend-xyz.railway.app`)

#### Step 7: Update Frontend Environment
Edit `frontend/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  BACKEND_PUBLIC_DOMAIN: 'https://backend-xyz.railway.app'  // Your backend domain
};
```
**Commit and push this change!**

#### Step 8: Add Frontend Service
```bash
railway add --service frontend
```

#### Step 9: Configure Frontend Service
In Railway web interface:
1. Click "frontend" service
2. Settings → Source → Connect Repo → Select your GitHub repo
3. Settings → Source → Root Directory → `frontend`
4. Networking → Generate Domain
5. Copy the generated domain (e.g., `https://frontend-xyz.railway.app`)

#### Step 10: Load Data to Railway Database
```bash
cd backend/scripts
railway connect Postgres
```
In the psql shell:
```sql
\i dbexport.pgsql
```

#### Step 11: Note Frontend URL
Save the frontend URL - this goes in `SUBMISSION.md`

---

### 8. Screenshots & Screen Captures
**Status:** Not started
**Location:** Create folder `screenshots/` or include in root

**Required screenshots:**
1. Full player summary page
2. Court visualization with shots/passes
3. Stats table with rankings
4. Different player views (at least 2-3 players)
5. Action type breakdowns
6. Responsive design (desktop & mobile if applicable)

**Formats accepted:** PNG, JPG, GIF, MP4 (screen recording)

---

### 9. Fill Out SUBMISSION.md
**Status:** Not started
**File:** `SUBMISSION.md`

**Required information:**
```markdown
# Submission Information

Applicant Name: [Your Full Name]

Applicant Email Address: [your.email@example.com]

Deployed Project URL: [https://frontend-xyz.railway.app]
```

---

### 10. AI Prompts Documentation (If Using AI)
**Status:** Not started
**Location:** `prompts/` directory

**Format:** Text file with ordered list
**Include:**
1. Each prompt used
2. AI model used (e.g., "Claude Sonnet 4.5", "ChatGPT 5")

**Example:**
```
prompts/ai_prompts.txt
---
1. [Claude Sonnet 4.5] "Help me design a normalized database schema for basketball statistics"
2. [Claude Sonnet 4.5] "Write a Django model for storing player shots with coordinates"
3. [Claude Sonnet 4.5] "Create an idempotent data loading script"
```

---

## 📋 FINAL CHECKLIST

### Backend ✅
- [x] Database schema designed
- [x] Django models created
- [x] Migrations run
- [x] Data loading script created and tested
- [x] Database architecture description written
- [x] API functions implemented
- [ ] Database exported (manual step)

### Frontend 🔄
- [ ] TypeScript interface created
- [ ] UI designed and implemented
- [ ] Court visualization added
- [ ] Stats display working
- [ ] Player ID input functional
- [ ] Frontend server tested locally

### Deployment 🔄
- [ ] Railway CLI installed
- [ ] Project initialized on Railway
- [ ] PostgreSQL added
- [ ] Backend service deployed
- [ ] Frontend service deployed
- [ ] Environment variables configured
- [ ] Database loaded to Railway
- [ ] Public URLs working

### Documentation 🔄
- [x] Database architecture description (<250 words)
- [ ] Screenshots/screen captures taken
- [ ] SUBMISSION.md filled out
- [ ] AI prompts documented (if applicable)

---

## 🚀 QUICK START COMMANDS

### Backend
```bash
# Start backend server
cd backend
source okc/Scripts/activate  # Windows: okc\Scripts\activate
python manage.py runserver

# Load data (already done)
python scripts/load_data.py

# Export database (needs manual password entry)
cd scripts
pg_dump -U okcapplicant okc > dbexport.pgsql
```

### Frontend
```bash
# Start frontend server
cd frontend
npm start
```

### Both servers must be running simultaneously for the app to work!

---

## 📊 CURRENT STATUS

**Completion:** ~60% done

**Time Estimate for Remaining Tasks:**
- Database export: 2 minutes (manual)
- Frontend interface: 30 minutes
- Frontend UI design: 2-4 hours
- Testing: 30 minutes
- Deployment: 1-2 hours
- Screenshots & documentation: 30 minutes

**Total remaining:** ~5-7 hours

---

## 🎯 PRIORITY ORDER

1. **Export database** (2 min) - Required for submission
2. **Test API** (10 min) - Verify backend works
3. **Create TypeScript interface** (30 min) - Foundation for frontend
4. **Design & implement UI** (3-4 hours) - Main frontend work
5. **Test locally** (30 min) - Ensure everything works
6. **Deploy to Railway** (1-2 hours) - Make it accessible
7. **Screenshots & docs** (30 min) - Final submission materials

---

## 📞 SUPPORT

**Questions?** Email: datasolutions@okcthunder.com

**Deadline:** Check your GitHub Classroom assignment for due date
