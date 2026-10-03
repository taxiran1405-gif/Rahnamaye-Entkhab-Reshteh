-- Annual choice-offering catalog.
create table if not exists choice_offering (
  offering_id uuid primary key default gen_random_uuid(),
  admission_year integer not null,
  group_name text not null,
  choice_code text not null,
  program_id text not null references program_family(program_id),
  university_id text not null references university(university_id),
  campus_id text references campus(campus_id),
  course_type_id text not null references course_type(course_type_id),
  selection_method text not null,
  city_id text references city(city_id),
  province_id text references province(province_id),
  quota_eligible boolean,
  capacity integer check (capacity is null or capacity >= 0),
  gender_restriction text,
  native_selection_type text,
  tuition_text text,
  source_id text not null references source(source_id),
  source_snapshot_hash text,
  status text not null default 'provisional'
    check (status in ('verified','provisional','conflicting','needs-review','superseded')),
  notes text,
  unique(admission_year,group_name,choice_code)
);

create table if not exists choice_offering_evidence (
  offering_id uuid not null references choice_offering(offering_id) on delete cascade,
  source_id text not null references source(source_id),
  snapshot_id uuid references source_snapshot(snapshot_id),
  evidence_locator text,
  primary key(offering_id,source_id)
);

create index if not exists idx_choice_offering_lookup
  on choice_offering(admission_year,group_name,program_id,university_id,course_type_id);

create index if not exists idx_choice_offering_city
  on choice_offering(admission_year,province_id,city_id);

comment on table choice_offering is 'Annual published choice catalog, separate from cutoff/outcome data.';
