# DND Campaign Manager

A self-hosted Dungeons & Dragons campaign manager built with Docker.

The goal of this project is to provide:
- User accounts
- Dungeon Master administration
- Campaign management
- Character creation
- Session management
- DM tools
- Lightweight and readable code
- Small files (preferably under 100 lines)

---

# Project Goals

## Core Features

### Authentication
- User registration
- Login/logout
- JWT or session auth
- Role system
  - Player
  - Dungeon Master (Admin)

### Campaign System
- Create campaign
- Join campaign
- Campaign invite codes
- Active campaign sessions

### Character Creation
- Create characters
- Edit stats
- Inventory
- Spell tracking
- Notes/backstory

### Dungeon Master Tools
- Campaign dashboard
- Monster management
- Encounter builder
- Hidden notes
- Initiative tracker

### Monster Database
- Public lore entries
- DM-only stat blocks
- Search/filter monsters

---

# Tech Stack

## Frontend
- React
- Vite
- TypeScript

## Backend
- FastAPI or Express
- REST API
- JWT authentication

## Database
- PostgreSQL

## Dev Environment
- Docker
- Docker Compose

---

# Design Rules

## File Size
Try to keep files under 100 lines whenever possible.

## Structure
Keep features modular and separated by domain.

Example:

backend/
  auth/
  campaigns/
  characters/
  monsters/

frontend/
  pages/
  components/
  api/

## Git Workflow
- One issue per feature
- One branch per issue
- Small pull requests

---

# Initial Development Plan

## Phase 1
- Docker setup
- Backend API
- Frontend setup
- Database connection

## Phase 2
- User authentication
- Roles
- Login system

## Phase 3
- Campaign creation
- Join campaign flow

## Phase 4
- Character creation

## Phase 5
- DM dashboard

## Phase 6
- Monster system

---

# Running the Project

```bash
docker compose up --build
