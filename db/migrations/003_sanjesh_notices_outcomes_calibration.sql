-- Sanjesh notice ledger, executable rule extraction, outcome data, and calibration registry.

create table if not exists sanjesh_notice (
  notice_id uuid primary key default gen_random_uuid(),
  source_id text not null references source(source_id),
  publication_date date,
  admission_year integer,
  notice_type text not null check (notice_type in (
    'policy','registration','score_report','quota_correction',
    'selection_booklet','selection_extension','ranking_method',
    'virtual_advisor','final_result','post_result_report',
    'academic_record','other'
  )),
  title_fa text not null,
  official_url text,
  access_url text,
  content_hash text,
  retrieved_at timestamptz not null default now(),
  status text not null default 'reviewed' check (status in (
    'reviewed','provisional','conflicting','superseded','stale'
  )),
  created_at timestamptz not null default now()
);

create table if not exists sanjesh_rule (
  rule_id text primary key,
  notice_id uuid references sanjesh_notice(notice_id) on delete set null,
  admission_year integer,
  rule_domain text not null check (rule_domain in (
    'eligibility','quota','region','native_selection','course_type',
    'scoring','selection_form','correction','results','academic_record',
    'special_condition'
  )),
  rule_text_fa text not null,
  required_inputs jsonb not null default '[]'::jsonb,
  engine_effect text not null,
  effective_from date,
  effective_to date,
  confidence text not null check (confidence in ('C4','C3','C2','C1','CX')),
  source_status text not null default 'provisional' check (source_status in (
    'official','official_mirror','secondary','conflicting'
  )),
  created_at timestamptz not null default now()
);

create table if not exists admission_outcome (
  outcome_id uuid primary key default gen_random_uuid(),
  run_id uuid references recommendation_run(run_id) on delete set null,
  option_id uuid references recommendation_option(option_id) on delete set null,
  admission_year integer not null,
  candidate_anonymous_id text not null,
  actual_quota_type text,
  actual_region text,
  actual_quota_rank integer,
  actual_national_rank integer,
  selected_choice_order integer,
  accepted boolean not null,
  accepted_program_id text references program_family(program_id),
  accepted_university_id text references university(university_id),
  accepted_course_type_id text references course_type(course_type_id),
  result_source_id text references source(source_id),
  result_evidence_locator text,
  observed_at timestamptz,
  notes text,
  created_at timestamptz not null default now()
);

create index if not exists idx_admission_outcome_calibration
  on admission_outcome(admission_year, actual_quota_type, actual_region, accepted);

create table if not exists calibration_run (
  calibration_id uuid primary key default gen_random_uuid(),
  model_version text not null,
  data_snapshot_hash text not null,
  outcome_snapshot_hash text not null,
  evaluation_scope jsonb not null,
  method text not null,
  metric_json jsonb not null,
  leakage_check text not null check (leakage_check in ('PASS','FAIL','REVIEW')),
  status text not null check (status in ('draft','verified','published','rejected')),
  created_at timestamptz not null default now()
);

comment on table sanjesh_rule is 'Executable rule extracted from a Sanjesh notice; rule changes are versioned.';
comment on table admission_outcome is 'Outcome-linked evidence for real calibration; anonymous identifier only.';
comment on table calibration_run is 'Reproducible calibration evaluation with leakage guard and immutable data snapshot references.';
