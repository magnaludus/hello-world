-- LoadLab migration 001: initial schema
-- Source: PRD §7.1. Every table is RLS-enforced on user_id.
-- Run locally: `supabase db reset` (destructive) or `supabase migration up`.

set check_function_bodies = off;

-- Extensions ------------------------------------------------------------------

create extension if not exists "pgcrypto";

-- Enums / helper types --------------------------------------------------------

do $$
begin
  if not exists (select 1 from pg_type where typname = 'component_type') then
    create type component_type as enum ('brass', 'powder', 'primer', 'bullet');
  end if;
  if not exists (select 1 from pg_type where typname = 'load_dev_method') then
    create type load_dev_method as enum (
      'satterlee',
      'ocw',
      'audette',
      'modified_audette',
      'seating_depth',
      'stat_velocity_ladder',
      'component_compare',
      'matrix'
    );
  end if;
  if not exists (select 1 from pg_type where typname = 'confidence_tier') then
    create type confidence_tier as enum ('high', 'moderate', 'low', 'insufficient');
  end if;
end
$$;

-- Tables ----------------------------------------------------------------------

create table if not exists public.rifle (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  name text not null,
  cartridge text not null,
  barrel_length_in numeric,
  twist_rate text,
  gas_system text,
  round_count_baseline int not null default 0,
  created_at timestamptz not null default now()
);
create index if not exists rifle_user_id_idx on public.rifle (user_id);

create table if not exists public.component (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  type component_type not null,
  brand text not null,
  model text,
  lot_number text,
  weight_gr numeric,
  bc_g1 numeric,
  bc_g7 numeric,
  notes text
);
create index if not exists component_user_id_idx on public.component (user_id);
create index if not exists component_type_idx on public.component (type);

create table if not exists public.session (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  rifle_id uuid not null references public.rifle (id) on delete restrict,
  method load_dev_method not null,
  date timestamptz not null,
  location text,
  temp_f numeric,
  pressure_inhg numeric,
  humidity_pct numeric check (humidity_pct is null or (humidity_pct between 0 and 100)),
  density_altitude_ft numeric,
  chronograph_type text,
  chrono_distance_ft numeric,
  target_distance_yd numeric,
  round_count_at_session int,
  notes text
);
create index if not exists session_user_id_idx on public.session (user_id);
create index if not exists session_rifle_id_idx on public.session (rifle_id);

create table if not exists public.load_recipe (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.session (id) on delete cascade,
  brass_id uuid references public.component (id),
  powder_id uuid references public.component (id),
  primer_id uuid references public.component (id),
  bullet_id uuid references public.component (id),
  cbto_in numeric,
  neck_tension_in numeric,
  notes text
);
create index if not exists load_recipe_session_id_idx on public.load_recipe (session_id);

create table if not exists public.charge_string (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.session (id) on delete cascade,
  recipe_id uuid not null references public.load_recipe (id) on delete cascade,
  charge_gr numeric not null,
  sequence_order int
);
create index if not exists charge_string_session_id_idx on public.charge_string (session_id);

create table if not exists public.shot (
  id uuid primary key default gen_random_uuid(),
  charge_string_id uuid not null references public.charge_string (id) on delete cascade,
  shot_number int not null,
  velocity_fps numeric,
  poi_x_in numeric,
  poi_y_in numeric,
  flagged boolean not null default false,
  flag_reason text,
  notes text
);
create index if not exists shot_charge_string_id_idx on public.shot (charge_string_id);

create table if not exists public.analysis_result (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.session (id) on delete cascade,
  method load_dev_method not null,
  result_json jsonb not null,
  confidence_tier confidence_tier,
  candidate_nodes jsonb,
  warnings text[],
  created_at timestamptz not null default now()
);
create index if not exists analysis_result_session_id_idx on public.analysis_result (session_id);

-- Row Level Security ----------------------------------------------------------

alter table public.rifle enable row level security;
alter table public.component enable row level security;
alter table public.session enable row level security;
alter table public.load_recipe enable row level security;
alter table public.charge_string enable row level security;
alter table public.shot enable row level security;
alter table public.analysis_result enable row level security;

-- Owner-only policies for top-level tables.
create policy rifle_owner on public.rifle
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy component_owner on public.component
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

create policy session_owner on public.session
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- Child tables inherit ownership via the parent session.
create policy load_recipe_owner on public.load_recipe
  for all using (
    exists (
      select 1 from public.session s
      where s.id = load_recipe.session_id and s.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.session s
      where s.id = load_recipe.session_id and s.user_id = auth.uid()
    )
  );

create policy charge_string_owner on public.charge_string
  for all using (
    exists (
      select 1 from public.session s
      where s.id = charge_string.session_id and s.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.session s
      where s.id = charge_string.session_id and s.user_id = auth.uid()
    )
  );

create policy shot_owner on public.shot
  for all using (
    exists (
      select 1
      from public.charge_string cs
      join public.session s on s.id = cs.session_id
      where cs.id = shot.charge_string_id and s.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1
      from public.charge_string cs
      join public.session s on s.id = cs.session_id
      where cs.id = shot.charge_string_id and s.user_id = auth.uid()
    )
  );

create policy analysis_result_owner on public.analysis_result
  for all using (
    exists (
      select 1 from public.session s
      where s.id = analysis_result.session_id and s.user_id = auth.uid()
    )
  ) with check (
    exists (
      select 1 from public.session s
      where s.id = analysis_result.session_id and s.user_id = auth.uid()
    )
  );
