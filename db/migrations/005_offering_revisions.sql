-- Event-sourced revisions for annual choice offerings.
create table if not exists choice_offering_revision (
  revision_id uuid primary key default gen_random_uuid(),
  admission_year integer not null,
  group_name text not null,
  choice_code text not null,
  operation text not null check (operation in ('ADD','CHANGE','DELETE')),
  fields_before jsonb,
  fields_after jsonb,
  notice_id uuid references sanjesh_notice(notice_id) on delete set null,
  source_id text not null references source(source_id),
  source_locator text,
  source_snapshot_hash text,
  effective_date date,
  status text not null default 'provisional'
    check (status in ('verified','provisional','conflicting','superseded','needs-review')),
  created_at timestamptz not null default now()
);

create index if not exists idx_offering_revision_apply
  on choice_offering_revision(admission_year,group_name,choice_code,effective_date);

create table if not exists offering_snapshot (
  snapshot_id uuid primary key default gen_random_uuid(),
  admission_year integer not null,
  group_name text not null,
  base_source_hash text not null,
  applied_revision_hash text not null,
  row_count integer not null default 0,
  status text not null check (status in ('draft','verified','published')),
  created_at timestamptz not null default now()
);
