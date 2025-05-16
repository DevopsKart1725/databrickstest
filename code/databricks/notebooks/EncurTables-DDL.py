# Databricks notebook source
catalogue_env = dbutils.widgets.get("adb_catalogue_env")
edl_catalog_env = dbutils.widgets.get("edl_catalogue_env")
# catalogue_env= "iep_dev"

# COMMAND ----------

# spark.sql(f"""create table if not exists {catalogue_env}.synhdq_encur.snap_edq_sync_user_access(
#     NETWORK_USER string, 
#     ACCESS_BASIS string, 
#     PROJECT_CODE string, 
#     GRM_ROLE string, 
#     REFRESH_DATE TIMESTAMP 
# )""")
# catalogue_env= "iep_dev"
spark.sql(f"""CREATE TABLE IF NOT EXISTS {catalogue_env}.synhdq_encur.snap_edq_user_access (
  network_user STRING,
  access_basis STRING,
  project_code STRING,
  grm_role STRING,
  ebs_role STRING)
""")

# COMMAND ----------

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_encur.snap_edq_source_refresh(
    SOURCE_SYSTEM           string,  
    REFRESH_START           TIMESTAMP,      
    STATUS                  string,  
    PROCESSED_TIMESTAMP     TIMESTAMP,      
    LAST_SUCCESSFUL_REFRESH TIMESTAMP,      
    REFRESH_ACTIVE          string
)""")

# COMMAND ----------

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_encur.snap_edq_project_details(
  entity_name  string,
  business_unit STRING,
  contract_category STRING,
  parent_sponsor STRING,
  sponsor_name STRING,
  project_status STRING,
  project_sub_status STRING,
  project_code STRING,
  master_project_code STRING,
  child_source STRING,
  project_manager STRING,
  project_director STRING,
  segment_lead STRING
)""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE if not exists iep_dev.synhdq_encur.snap_edq_rule_disabled_records
( entity_name string,
  key4 STRING,
  generic_query_text String,
  master_project_code STRING,
  key2 STRING,
  status string,
  sponsor string,
  disable_reason string,
  other_reason string,
  user_id string,
  disabled_type string
  )""")

# COMMAND ----------

spark.sql(f"""CREATE table if not exists {catalogue_env}.synhdq_encur.snap_edq_query_details(
  entity_name STRING,
  query_id bigint,
  key1 STRING,
  key2 STRING,
  key3 STRING,
  key4 STRING,
  date_opened date,
  closed_date date,
  days_open bigint,
  status string,
  exception_flag string,
  flag_priority int,
  flex1 STRING,
  subject_area STRING,
  generic_query_text STRING,
  extract_date date,
  flex2 STRING,
  flex3 STRING,
  flex4 STRING,
  flex5 STRING,
  flex6 STRING,
  target_field STRING,
  flex7 STRING,
  flex8 STRING,
  flex9 STRING,
  system_site_status STRING,
  country_startup_specialist STRING,
  flex10 STRING,
  dli_refresh_time TIMESTAMP,
  flex11 STRING,
  region STRING
)""")

# COMMAND ----------

spark.sql(f"""CREATE TABLE if not exists {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score(
  entity_name STRING,
  key1 STRING,
  key2 STRING,
  key4 STRING,
  failed_count BIGINT,
  pass_count BIGINT,
  extract_date date,
  no_of_evaluations INT,
  master_project_code STRING,
  no_of_open_flags BIGINT,
  subject_area STRING,
  exception_count BIGINT,
  dq_score DOUBLE)""")
