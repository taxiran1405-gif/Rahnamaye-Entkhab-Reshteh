-- Quota-aware rank context
-- Do not replace the original migration; this migration is additive and versioned.
alter table admission_observation
  add column if not exists rank_basis text,
  add column if not exists quota_population_size integer;

alter table admission_observation
  add constraint admission_observation_rank_basis_chk
  check (rank_basis is null or rank_basis in (
    'national_rank','quota_rank','final_quota_rank','regional_rank','special_quota_rank'
  ));

create table if not exists student_quota_rank (
  quota_rank_id uuid primary key default gen_random_uuid(),
  profile_id uuid not null references student_profile(profile_id) on delete cascade,
  quota_type text not null,
  region text,
  rank_value integer not null check (rank_value > 0),
  is_final boolean not null default false,
  verification_status text not null default 'provisional'
    check (verification_status in ('verified','provisional','conflicting','needs-review')),
  source_id text references source(source_id),
  snapshot_id uuid references source_snapshot(snapshot_id),
  evidence_locator text,
  created_at timestamptz not null default now()
);

create index if not exists idx_student_quota_rank_lookup
  on student_quota_rank(profile_id, quota_type, region, is_final);

create index if not exists idx_admission_quota_basis
  on admission_observation(program_id, university_id, course_type_id, quota_type, region, rank_basis, data_year);

comment on column admission_observation.rank_basis is
  'Semantic basis of cutoff_rank; direct comparisons require matching candidate rank semantics.';
comment on column admission_observation.quota_population_size is
  'Optional size of the relevant quota cohort when officially or reliably known.';
