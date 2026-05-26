
---

And this is the OpenCode prompt I’d use to generate issues progressively.

:::writing{variant="standard" id="48172"}
You are helping build a Docker-first Dungeons & Dragons campaign manager application.

Project requirements:

- Keep files under 100 lines whenever possible
- Keep code modular and readable
- One feature per issue
- One responsibility per file
- Avoid giant utility files
- Prefer composition over complexity

Tech stack:
- React + Vite frontend
- FastAPI or Express backend
- PostgreSQL database
- Docker Compose for development
- JWT authentication

Main features:
- User login/register
- Dungeon Master admin role
- Campaign creation/joining
- Character creation
- DM dashboard
- Monster management
- Session tracking

Architecture goals:
- Separate frontend/backend cleanly
- Organize by feature domain
- Keep APIs RESTful
- Write beginner-readable code
- Add comments only when useful

Your task:
1. Generate GitHub issues one at a time
2. Each issue should contain:
   - Title
   - Description
   - Goals
   - Acceptance criteria
   - Suggested file structure
3. Start with foundational infrastructure first
4. Do NOT skip steps
5. Prefer incremental progress over large implementations

Development order:
1. Docker setup
2. Backend bootstrap
3. Frontend bootstrap
4. Database setup
5. Auth system
6. Campaign system
7. Character system
8. DM tools
9. Monster system

When generating code:
- Keep files small
- Split logic into focused modules
- Avoid overengineering
- Prefer explicit code over abstraction
- Explain WHY files are created
:::

Your first GitHub issues should probably look like this:

1. Docker Compose Setup
2. Backend FastAPI/Express Bootstrap
3. Frontend React/Vite Bootstrap
4. PostgreSQL Container Setup
5. Healthcheck API Route
6. Frontend API Connection Test
7. User Model
8. Registration Endpoint
9. Login Endpoint
10. JWT Middleware

I also think you should structure the repo like this early:

```text
dnd-manager/
├── docker/
├── backend/
├── frontend/
├── database/
├── docs/
├── .github/
│   └── ISSUE_TEMPLATE/
└── docker-compose.yml
