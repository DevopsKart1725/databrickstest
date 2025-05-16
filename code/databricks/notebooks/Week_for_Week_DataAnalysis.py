# Databricks notebook source
# MAGIC %run ./PreviousPastTables-DDL

# COMMAND ----------

# catalogue_env="iep_dev"

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p5_week_flags select * from {catalogue_env}.synhdq_encur.snap_p4_week_flags""")

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p4_week_flags select * from {catalogue_env}.synhdq_encur.snap_p3_week_flags""")

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p3_week_flags select * from {catalogue_env}.synhdq_encur.snap_p2_week_flags""")

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p2_week_flags select * from {catalogue_env}.synhdq_encur.snap_p1_week_flags""")

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p1_week_flags 
select pd.business_unit
,pd.contract_category
,pd.parent_sponsor
,pd.sponsor_name
,pd.project_status
,pd.project_sub_status
,pd.master_project_code
,pd.project_manager
,pd.project_director
,pd.segment_lead
,tgt.key2
,er.role
,er.rule_type
,er.`function`
,tgt.Key4
,tgt.query_id
,tgt.date_opened
,tgt.closed_date
,tgt.days_open
,tgt.status
,sc.dq_score
,concat_ws('-',YEAR(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date)),date_format(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date), 'MMM')
,case when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date)) < 7 then 'WK-1'
      when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date)) < 14 then 'WK-2'
      when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date)) < 21 then 'WK-3'
      when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date)) < 28 then 'WK-4'
ELSE 'WK-5' END) AS week_details
from {catalogue_env}.synhdq_encur.snap_edq_query_details tgt
left outer join {catalogue_env}.synhdq_encur.snap_edq_project_details pd on tgt.Key1=pd.project_code and tgt.key2=pd.child_source
left outer join {catalogue_env}.synhdq_work.edh_rules er on tgt.Key4=er.Key4
left outer join {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score sc on tgt.key1= sc.key1 and tgt.key2=sc.key2 and tgt.key4=sc.key4
--where tgt.date_opened between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) + INTERVAL 6 DAY) as date) OR tgt.closed_date between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 7 DAYS) + INTERVAL 6 DAY) as date)
""") .display()

# COMMAND ----------

# spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p2_week_flags 
# select pd.business_unit
# ,pd.contract_category
# ,pd.parent_sponsor
# ,pd.sponsor_name
# ,pd.project_status
# ,pd.project_sub_status
# ,pd.master_project_code
# ,pd.project_manager
# ,pd.project_director
# ,pd.segment_lead
# ,tgt.key2
# ,er.role
# ,er.rule_type
# ,er.`function`
# ,tgt.Key4
# ,tgt.query_id
# ,tgt.date_opened
# ,tgt.closed_date
# ,tgt.days_open
# ,tgt.status
# ,sc.dq_score
# ,concat_ws('-',YEAR(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) as date)),date_format(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) as date), 'MMM')
# ,case when day(cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)) < 7 then 'WK-5'
#       when day(cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)) < 14 then 'WK-4'
#       when day(cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)) < 21 then 'WK-3'
#       when day(cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)) < 28 then 'WK-2'
# ELSE 'WK-1' END) AS week_details
# from {catalogue_env}.synhdq_encur.snap_edq_query_details tgt
# left outer join {catalogue_env}.synhdq_encur.snap_edq_project_details pd on tgt.Key1=pd.project_code and tgt.key2=pd.child_source
# left outer join {catalogue_env}.synhdq_work.edh_rules er on tgt.Key4=er.Key4  and tgt.key2=er.key2
# left outer join {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score sc on tgt.key1= sc.key1 and tgt.key2=sc.key2 and tgt.key4=sc.key4
# where tgt.date_opened between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)
# OR tgt.closed_date between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 14 DAYS) + INTERVAL 6 DAY) as date)""");

# COMMAND ----------

# spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p3_week_flags 
# select pd.business_unit
# ,pd.contract_category
# ,pd.parent_sponsor
# ,pd.sponsor_name
# ,pd.project_status
# ,pd.project_sub_status
# ,pd.master_project_code
# ,pd.project_manager
# ,pd.project_director
# ,pd.segment_lead
# ,tgt.key2
# ,er.role
# ,er.rule_type
# ,er.`function`
# ,tgt.Key4
# ,tgt.query_id
# ,tgt.date_opened
# ,tgt.closed_date
# ,tgt.days_open
# ,tgt.status
# ,sc.dq_score
# ,concat_ws('-',YEAR(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date)),date_format(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date), 'MMM')
# ,case when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date)) < 7 then 'WK-1'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date)) < 14 then 'WK-2'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date)) < 21 then 'WK-3'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date)) < 28 then 'WK-4'
# ELSE 'WK-5' END) AS week_details
# from {catalogue_env}.synhdq_encur.snap_edq_query_details tgt
# left outer join {catalogue_env}.synhdq_encur.snap_edq_project_details pd on tgt.Key1=pd.project_code and tgt.key2=pd.child_source
# left outer join {catalogue_env}.synhdq_work.edh_rules er on tgt.Key4=er.Key4
# left outer join {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score sc on tgt.key1= sc.key1 and tgt.key2=sc.key2 and tgt.key4=sc.key4
# where tgt.date_opened between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) + INTERVAL 6 DAY) as date)
# OR tgt.closed_date between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 21 DAYS) + INTERVAL 6 DAY) as date)""");

# COMMAND ----------

# spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p4_week_flags 
# select pd.business_unit
# ,pd.contract_category
# ,pd.parent_sponsor
# ,pd.sponsor_name
# ,pd.project_status
# ,pd.project_sub_status
# ,pd.master_project_code
# ,pd.project_manager
# ,pd.project_director
# ,pd.segment_lead
# ,tgt.key2
# ,er.role
# ,er.rule_type
# ,er.`function`
# ,tgt.Key4
# ,tgt.query_id
# ,tgt.date_opened
# ,tgt.closed_date
# ,tgt.days_open
# ,tgt.status
# ,sc.dq_score
# ,concat_ws('-',YEAR(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date)),date_format(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date), 'MMM')
# ,case when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date)) < 7 then 'WK-1'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date)) < 14 then 'WK-2'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date)) < 21 then 'WK-3'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date)) < 28 then 'WK-4'
# ELSE 'WK-5' END) AS week_details
# from {catalogue_env}.synhdq_encur.snap_edq_query_details tgt
# left outer join {catalogue_env}.synhdq_encur.snap_edq_project_details pd on tgt.Key1=pd.project_code and tgt.key2=pd.child_source
# left outer join {catalogue_env}.synhdq_work.edh_rules er on tgt.Key4=er.Key4
# left outer join {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score sc on tgt.key1= sc.key1 and tgt.key2=sc.key2 and tgt.key4=sc.key4
# where tgt.date_opened between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) + INTERVAL 6 DAY) as date)
# OR tgt.closed_date between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 28 DAYS) + INTERVAL 6 DAY) as date)""");

# COMMAND ----------

# spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_p5_week_flags 
# select pd.business_unit
# ,pd.contract_category
# ,pd.parent_sponsor
# ,pd.sponsor_name
# ,pd.project_status
# ,pd.project_sub_status
# ,pd.master_project_code
# ,pd.project_manager
# ,pd.project_director
# ,pd.segment_lead
# ,tgt.key2
# ,er.role
# ,er.rule_type
# ,er.`function`
# ,tgt.Key4
# ,tgt.query_id
# ,tgt.date_opened
# ,tgt.closed_date
# ,tgt.days_open
# ,tgt.status
# ,sc.dq_score
# ,concat_ws('-',YEAR(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date)),date_format(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date), 'MMM')
# ,case when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date)) < 7 then 'WK-1'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date)) < 14 then 'WK-2'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date)) < 21 then 'WK-3'
#       when day(cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date)) < 28 then 'WK-4'
# ELSE 'WK-5' END) AS week_details
# from {catalogue_env}.synhdq_encur.snap_edq_query_details tgt
# left outer join {catalogue_env}.synhdq_encur.snap_edq_project_details pd on tgt.Key1=pd.project_code and tgt.key2=pd.child_source
# left outer join {catalogue_env}.synhdq_work.edh_rules er on tgt.Key4=er.Key4
# left outer join {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score sc on tgt.key1= sc.key1 and tgt.key2=sc.key2 and tgt.key4=sc.key4
# where tgt.date_opened between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) + INTERVAL 6 DAY) as date)
# OR tgt.closed_date between cast(DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) as date) and cast((DATE_TRUNC('week', CURRENT_DATE - INTERVAL 35 DAYS) + INTERVAL 6 DAY) as date)""");
