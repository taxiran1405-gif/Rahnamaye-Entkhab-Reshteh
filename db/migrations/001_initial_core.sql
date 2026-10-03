create extension if not exists pgcrypto;

create table source (
  source_id text primary key,
  name_fa text not null,
  url text,
  authority_level text not null check (authority_level in ('A','B','C','D')),
  active boolean not null default true
);

create table source_snapshot (
  snapshot_id uuid primary key default gen_random_uuid(),
  source_id text not null references source(source_id),
  retrieved_at timestamptz not null,
  content_hash text not null,
  content_type text,
  locator text,
  status text not null check (status in ('ok','error','changed','unchanged')),
  error_message text
);

create table province (
  province_id text primary key, name_fa text not null unique, capital_city_fa text not null
);

create table city (
  city_id text primary key, province_id text not null references province(province_id),
  name_fa text not null, is_province_capital boolean not null default false,
  unique(province_id,name_fa)
);

create table university (
  university_id text primary key, name_fa text not null,
  province_id text not null references province(province_id),
  seat_city_id text references city(city_id), governance text,
  scope text not null check (scope in ('provincial_capital_public','regional_major_center')),
  verification_status text not null default 'needs_official_verification'
    check (verification_status in ('verified','provisional','needs_official_verification','conflicting'))
);

create table campus (
  campus_id text primary key, university_id text not null references university(university_id),
  city_id text references city(city_id), name_fa text,
  verification_status text not null default 'needs_official_verification'
    check (verification_status in ('verified','provisional','needs_official_verification','conflicting'))
);

create table program_family (
  program_id text primary key, name_fa text not null, group_name text not null
);

create table course_type (
  course_type_id text primary key, name_fa text not null unique
);

create table admission_observation (
  admission_id uuid primary key default gen_random_uuid(),
  data_year integer not null, academic_year integer, group_name text not null,
  program_id text not null references program_family(program_id),
  university_id text not null references university(university_id), campus_id text references campus(campus_id),
  course_type_id text not null references course_type(course_type_id), quota_type text not null, region text not null,
  cutoff_rank numeric not null check (cutoff_rank > 0),
  data_kind text not null check (data_kind in ('official','reported_last_rank','approx_range','sample_card','aggregate')),
  sample_size integer,
  confidence text not null check (confidence in ('C4','C3','C2','C1','CX')),
  conflict_status text not null default 'none' check (conflict_status in ('none','conflicting','needs_review','resolved')),
  created_at timestamptz not null default now()
);

create table admission_evidence (
  admission_id uuid not null references admission_observation(admission_id) on delete cascade,
  source_id text not null references source(source_id), snapshot_id uuid references source_snapshot(snapshot_id),
  evidence_locator text, primary key(admission_id,source_id)
);

create table university_metric (
  metric_id uuid primary key default gen_random_uuid(),
  university_id text not null references university(university_id), source_id text not null references source(source_id),
  edition integer, metric_name text not null,
  metric_scope text not null check (metric_scope in ('overall','subject','research','teaching','industry','international')),
  value_text text not null, retrieved_at timestamptz not null,
  confidence text not null check (confidence in ('C4','C3','C2','C1','CX'))
);

create table evidence_record (
  evidence_id uuid primary key default gen_random_uuid(), source_id text not null references source(source_id),
  snapshot_id uuid references source_snapshot(snapshot_id), entity_type text not null, entity_id text not null,
  field_name text not null, value_json jsonb not null, data_year integer not null, academic_year integer,
  authority_level text not null check (authority_level in ('A','B','C','D')),
  confidence text not null check (confidence in ('C4','C3','C2','C1','CX')),
  conflict_status text not null default 'none' check (conflict_status in ('none','conflicting','needs_review','resolved')),
  created_at timestamptz not null default now()
);

create table student_profile (
  profile_id uuid primary key default gen_random_uuid(), target_year integer not null, group_name text not null,
  national_rank integer not null, quota_rank integer, quota_type text not null, region text not null,
  preferences_json jsonb not null default '{}'::jsonb, created_at timestamptz not null default now()
);

create table recommendation_run (
  run_id uuid primary key default gen_random_uuid(), profile_id uuid not null references student_profile(profile_id),
  started_at timestamptz not null default now(), model_version text not null, rule_version text not null,
  weights_version text not null, candidate_set_hash text,
  status text not null check (status in ('draft','verified','published','rejected'))
);

create table recommendation_cell (
  cell_id uuid primary key default gen_random_uuid(), run_id uuid not null references recommendation_run(run_id) on delete cascade,
  display_order integer not null, created_at timestamptz not null default now()
);

create table recommendation_option (
  option_id uuid primary key default gen_random_uuid(), cell_id uuid not null references recommendation_cell(cell_id) on delete cascade,
  program_id text not null references program_family(program_id), university_id text not null references university(university_id),
  campus_id text references campus(campus_id), course_type_id text not null references course_type(course_type_id),
  row_role text not null check (row_role in ('primary','parallel','cover')),
  admission_lower numeric, admission_upper numeric, admission_midpoint numeric, utility_score numeric,
  risk_class text not null, confidence text not null check (confidence in ('C4','C3','C2','C1','CX')),
  reason_codes jsonb not null default '[]'::jsonb, evidence_ids jsonb not null default '[]'::jsonb
);

create table verification_event (
  verification_id uuid primary key default gen_random_uuid(), run_id uuid references recommendation_run(run_id) on delete cascade,
  stage text not null, status text not null check (status in ('PASS','FAIL','REVIEW')),
  details_json jsonb not null default '{}'::jsonb, created_at timestamptz not null default now()
);

create table model_outcome (
  outcome_id uuid primary key default gen_random_uuid(), run_id uuid not null references recommendation_run(run_id),
  option_id uuid references recommendation_option(option_id), outcome_status text, accepted_program_text text,
  observed_rank integer, observed_at timestamptz, notes text
);

create index idx_admission_lookup on admission_observation(program_id,university_id,course_type_id,quota_type,region,data_year);
create index idx_evidence_entity on evidence_record(entity_type,entity_id,field_name,data_year);