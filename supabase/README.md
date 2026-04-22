# Supabase

Local Supabase project config and migrations for LoadLab.

## Layout

- `config.toml` - local dev config (auth, ports, storage)
- `migrations/` - ordered SQL migrations

## Commands

```bash
# One-time
supabase login
supabase link --project-ref <project-ref>

# Apply migrations to remote
supabase db push

# Generate TS types into packages/db
supabase gen types typescript --linked > ../packages/db/src/database.types.ts
```

## Migration 001

Creates the full schema from PRD §7.1, including:

- `rifle`, `component` - user-owned inventory
- `session`, `load_recipe`, `charge_string`, `shot` - session flow tables
- `analysis_result` - stats engine output persisted alongside the session
- RLS policies on every table, owner-only via `auth.uid() = user_id`
- Child tables (`load_recipe`, `charge_string`, `shot`, `analysis_result`) gate access through their parent `session`
