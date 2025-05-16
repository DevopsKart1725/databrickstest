# Databricks notebook source
# catalogue_env = "iep_dev"
catalogue_env = dbutils.widgets.get("adb_catalogue_env")

# COMMAND ----------

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_exceptions (entity_name string,
flag_id bigint,
exception string,
exception_reason string,
network_id string,
flagged_date date,
other_reason string,
is_approved string)""")


spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_query_details (entity_name string,
flex1 string,
key1 string,
Key2 string,
subject_area string,
generic_query_text string,
extract_date date,
flex2 string,
flex3 string,
flex4 string,
flex5 string,
flex6 string,
target_field string,
key3 string,
flex7 string,
flex8 string,
flex9 string,
key4 string,
system_site_status string,
country_startup_specialist string,
flex10 string,
dli_refresh_time date,
flex11 string,
region string)""")


spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_rules(
entity_name string,
key4 string,
priority int,
rule_type string,
function string,
key2 string,
activated_date date,
decommissioned_date date,
role string)""")

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_flag_reactivation
(entity_name string,
flag_id bigint,
network_id string,
reactivate_date date)""")

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_score
(entity_name string,
key1 string,
key2 string,
key4 string,
failed_count bigint,
pass_count bigint,
extract_date date)""")


spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_score
(entity_name string,
key1 string,
key2 string,
key4 string,
generic_query_text string,
disable_reason string)""")


# New table for IEP
spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.iep_edh_score_detail
(entity_name string,
project_code string,
check_no string,
failed_count bigint,
pass_count bigint,
source_system string,
extract_date date,
site_id string,
int_site_id string)""")

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.edh_rules_attributes
(entity_name string,
transaction_id string,
rule_no string,
type string,
value string,
subtype string)""")


# COMMAND ----------

spark.sql(f"""CREATE TABLE if not exists iep_dev.synhdq_work.edh_rule_disabled_records
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

spark.sql(f"drop table if exists {catalogue_env}.synhdq_work.child_source_mapping")

# COMMAND ----------

spark.sql(f"""create table if not exists {catalogue_env}.synhdq_work.child_source_mapping  
(  
child_source string,
derived_child_source string
)
""");

# COMMAND ----------

spark.sql(f"""
insert into {catalogue_env}.synhdq_work.child_source_mapping
select 'ICE' as child_source ,'Syneos Pricing Tool' as derived_child_source union
select 'VC' as child_source ,'Vault Clinical' as derived_child_source union
select 'QB' as child_source ,'QuickBase' as derived_child_source union
select 'VV' as child_source ,'Veeva TMF' as derived_child_source union
select 'RAVE' as child_source ,'RAVE EDC' as derived_child_source union
select 'EBS' as child_source ,'Oracle EBS RBB' as derived_child_source union
select 'IMS_PIT' as child_source ,'IMS Funds Setup' as derived_child_source union
select 'IMS_CM' as child_source ,'IMS Case Manager' as derived_child_source union
select 'PRISM' as child_source ,'PRISM' as derived_child_source union
select 'FT' as child_source ,'Forecast' as derived_child_source union
select 'SH' as child_source ,'Proj Deliv Ctr' as derived_child_source union
select 'SF' as child_source ,'Salesforce' as derived_child_source union
select 'GB' as child_source ,'Activate' as derived_child_source union
select 'MC' as child_source ,'CTMS' as derived_child_source union
select 'GRM' as child_source ,'GRM' as derived_child_source""")
