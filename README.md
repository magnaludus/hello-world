# LoadLab

Precision rifle load development platform. Statistically honest node detection, component context, and multi-session confirmation workflow. See the PRD for the full spec (§1-18).

## Repo layout

```
loadlab/
├── apps/
│   ├── web/              Next.js 14 + Tailwind + shadcn/ui
│   ├── stats-service/    Python FastAPI statistics engine
│   └── cli/              loadlab CLI (import, analyze, export, power)
├── packages/
│   ├── shared/           Zod schemas + TS types
│   ├── chrono-parsers/   Garmin, LabRadar, MagnetoSpeed, ...
│   └── db/               Supabase types + generated database.types.ts
└── supabase/
    ├── config.toml
    └── migrations/       SQL migrations (001: initial schema)
```

## Prereqs

- Node 20 LTS, pnpm 9+
- Python 3.11
- Supabase CLI
- Docker (for local Supabase + stats-service)

## Bootstrap

```bash
pnpm install
cp apps/web/.env.example apps/web/.env.local   # fill in Supabase keys

# Stats service
cd apps/stats-service
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cd ../..

# Local Supabase
supabase start
supabase db reset                              # applies migrations/
```

## Turbo tasks

```bash
pnpm dev           # parallel dev for all apps that define dev
pnpm build
pnpm lint
pnpm typecheck
pnpm test
```

## What's in this commit

Phase 1 scaffold only, per PRD §13:

- Monorepo (Turborepo + pnpm workspaces), TS strict mode, ESLint strict, Prettier, Vitest
- `apps/web` Next.js 14 App Router, Tailwind + shadcn/ui, dark theme, semantic confidence-tier tokens from PRD §6.10
- `apps/stats-service` FastAPI skeleton with module layout matching PRD §6 (methods, detection, power, bayesian, validation)
- `apps/cli` Commander skeleton with stubs for `power`, `import`, `analyze`
- `packages/shared` Zod schemas mirroring the Postgres enums in §7.1
- `packages/chrono-parsers`, `packages/db` placeholders
- `supabase/migrations/20260422000001_init.sql` full schema from §7.1 with RLS

Next: follow the "First Claude Code Prompt" protocol and proceed phase by phase per §13.
