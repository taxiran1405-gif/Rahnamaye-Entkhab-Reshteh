-- Raw program titles remain lossless until canonical mapping is reviewed.
create table if not exists program_title_raw (
  raw_program_id uuid primary key default gen_random_uuid(),
  admission_year integer not null,
  group_name text not null,
  raw_title_fa text not null,
  canonical_program_id text references program_family(program_id),
  mapping_status text not null default 'needs-review'
    check (mapping_status in ('mapped','needs-review','conflicting','rejected')),
  source_id text not null references source(source_id),
  source_locator text,
  unique(admission_year,group_name,raw_title_fa)
);

create index if not exists idx_program_raw_mapping
  on program_title_raw(admission_year,group_name,mapping_status);
