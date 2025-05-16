# Databricks notebook source
dbutils.widgets.text("adb_catalogue_env","")
dbutils.widgets.text("edl_catalogue_env","")

# COMMAND ----------

iep_ct_env=dbutils.widgets.get("adb_catalogue_env")
edl_ct_env= dbutils.widgets.get("edl_catalogue_env")

# COMMAND ----------

# Connect to source query for query_detail
spark.sql(f"USE CATALOG {iep_ct_env}")
df_query_detail=spark.sql("""select distinct qd.entity_name,qd.query_id,qd.key1 as project_code,qd.key2 as source_system,qd.key3,qd.key4 as rule_id,qd.date_opened,qd.closed_date,qd.days_open,qd.status,qd.exception_flag,qd.flag_priority,qd.subject_area,qd.generic_query_text,qd.extract_date,qd.target_field,qd.system_site_status,qd.country_startup_specialist,qd.dli_refresh_time,qd.region,CURRENT_TIMESTAMP() as last_processed_date from synhdq_encur.snap_edq_query_details qd inner join synhdq_work.edh_rules_attributes rules on qd.key4=rules.rule_no where upper(rules.value)='IEP'""")

# COMMAND ----------

# Connect to source query for dashboard_filter
df_dashboard_filter=spark.sql(f"""select distinct project_code,study_status1,Award_date,FSP_FSO,contract_attribute,study_phase,therapeutic_area,indication,primary_sub_indication,rescue_project,owning_business_unit,sponsor_name,CURRENT_TIMESTAMP() as last_processed_date from {edl_ct_env}.prc_presentation.sync_global_index""")

# COMMAND ----------

# Connect to source query for work schema iep_edh_score_detail
spark.sql(f"USE CATALOG {iep_ct_env}")
df_edq_score_detail=spark.sql("select distinct sc.project_code,sc.check_no,sc.failed_count,sc.pass_count,sc.source_system,sc.extract_date,sc.site_id,sc.int_site_id,CURRENT_TIMESTAMP() as last_processed_date from synhdq_work.iep_edh_score_detail sc inner join synhdq_encur.iep_rule_model_mapping rmdl on rmdl.Rule = substr(sc.check_no, 2,3)")

# COMMAND ----------

# Load data into tgt tables
spark.sql(f"USE CATALOG {iep_ct_env}")
spark.sql("use schema synhdq_encur")

# DDL query_detail table
spark.sql("drop table if exists iep_edq_query_details")
df_query_detail.write.mode("overwrite").saveAsTable("iep_edq_query_details")

# DDL Dashboard_filter table
spark.sql("drop table if exists iep_edq_dashboard_filters")
df_dashboard_filter.write.mode("overwrite").saveAsTable("iep_edq_dashboard_filters")

# DDL score_detail table
spark.sql("drop table if exists iep_edq_score_detail")
df_edq_score_detail.write.mode("overwrite").saveAsTable("iep_edq_score_detail")

# COMMAND ----------

spark.sql(f"USE CATALOG {iep_ct_env}")
spark.sql("use schema synhdq_encur")
# Create the table iep_edq_score_summary if it does not exist
#spark.sql("drop table IF EXISTS iep_edq_score_summary")
spark.sql("""CREATE TABLE IF NOT EXISTS iep_edq_score_summary (
    extract_date DATE,
    award_date DATE,
    project_code STRING,
    check_no STRING,
    pass_count BIGINT,
    failed_count BIGINT,
    insert_date TIMESTAMP
)
USING delta
PARTITIONED BY (extract_date)
""")

# COMMAND ----------

spark.sql(f"USE CATALOG {iep_ct_env}")
spark.sql("use schema synhdq_encur")
df_iep_edq_score_summary=spark.sql("""select sdet.extract_date,to_date(dbf.award_date, 'yyyy-mm-dd') award_date,sdet.project_code,substr(sdet.check_no, 2, 3) check_no,sum(ifnull(sdet.pass_count,0)) pass_count,sum(ifnull(sdet.failed_count,0)) failed_count, current_timestamp() as insert_date from iep_edq_score_detail sdet inner join iep_edq_dashboard_filters dbf ON sdet.project_code = dbf.project_code group by sdet.extract_date,to_date(dbf.award_date, 'yyyy-mm-dd'),sdet.project_code,substr(sdet.check_no, 2, 3) order by 1,2,3,4""")
print(df_iep_edq_score_summary.count())

# COMMAND ----------

from datetime import timedelta

spark.sql(f"USE CATALOG {iep_ct_env}")
spark.sql("use schema synhdq_encur")
# Get the maximum extract_date from the DataFrame
max_extract_date = df_iep_edq_score_summary.agg({"extract_date": "max"}).collect()[0][0]
old_extract_date = max_extract_date - timedelta(days=183)
print(max_extract_date)
print(old_extract_date)

# Delete records from the Summary table where extract_date is same as source extract_date and 6 months older records
spark.sql(f"DELETE FROM iep_edq_score_summary WHERE extract_date = '{max_extract_date}' or extract_date < '{old_extract_date}'")

# COMMAND ----------

spark.sql(f"USE CATALOG {iep_ct_env}")
spark.sql("use schema synhdq_encur")
#spark.sql("drop table if exists iep_edq_score_summary")
df_iep_edq_score_summary.write.insertInto("iep_edq_score_summary", overwrite=False)
