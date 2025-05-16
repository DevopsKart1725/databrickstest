# Databricks notebook source
# catalogue_env = "iep_dev"
catalogue_env = dbutils.widgets.get("adb_catalogue_env")

# COMMAND ----------

spark.sql(f"""create  table if not exists {catalogue_env}.synhdq_encur.snap_p1_week_flags
( business_unit          STRING
,contract_category      STRING
,parent_sponsor         STRING
,sponsor_name           STRING
,project_status         STRING
,project_sub_status     STRING
,master_project_code    STRING
,project_manager        STRING
,project_director       STRING
,segment_lead           STRING
,key2                   STRING
,role                   STRING
,rule_type              STRING
,`function`             STRING
,key4                   STRING
,query_id               STRING
,date_opened            date
,closed_date            date
,days_open              BIGINT
,status                 STRING
,dq_score               DOUBLE
,week_details           STRING
)""")

# COMMAND ----------

spark.sql(f"""create  table if not exists {catalogue_env}.synhdq_encur.snap_p2_week_flags
( business_unit          STRING
,contract_category      STRING
,parent_sponsor         STRING
,sponsor_name           STRING
,project_status         STRING
,project_sub_status     STRING
,master_project_code    STRING
,project_manager        STRING
,project_director       STRING
,segment_lead           STRING
,key2                   STRING
,role                   STRING
,rule_type              STRING
,`function`             STRING
,key4                   STRING
,query_id               STRING
,date_opened            date
,closed_date            date
,days_open              bigint
,status                 STRING
,dq_score               DOUBLE
,week_details           STRING
)""")

# COMMAND ----------

spark.sql(f"""create  table if not exists {catalogue_env}.synhdq_encur.snap_p3_week_flags
( business_unit          STRING
,contract_category      STRING
,parent_sponsor         STRING
,sponsor_name           STRING
,project_status         STRING
,project_sub_status     STRING
,master_project_code    STRING
,project_manager        STRING
,project_director       STRING
,segment_lead           STRING
,key2                   STRING
,role                   STRING
,rule_type              STRING
,`function`             STRING
,key4                   STRING
,query_id               STRING
,date_opened            date
,closed_date            date
,days_open              bigint
,status                 STRING
,dq_score               DOUBLE
,week_details           STRING
)""")

# COMMAND ----------

spark.sql(f"""create  table if not exists {catalogue_env}.synhdq_encur.snap_p4_week_flags
( business_unit          STRING
,contract_category      STRING
,parent_sponsor         STRING
,sponsor_name           STRING
,project_status         STRING
,project_sub_status     STRING
,master_project_code    STRING
,project_manager        STRING
,project_director       STRING
,segment_lead           STRING
,key2                   STRING
,role                   STRING
,rule_type              STRING
,`function`             STRING
,key4                   STRING
,query_id               STRING
,date_opened            date
,closed_date            date
,days_open              bigint
,status                 STRING
,dq_score               DOUBLE
,week_details           STRING
)""")

# COMMAND ----------

spark.sql(f"""create  table if not exists {catalogue_env}.synhdq_encur.snap_p5_week_flags
( business_unit          STRING
,contract_category      STRING
,parent_sponsor         STRING
,sponsor_name           STRING
,project_status         STRING
,project_sub_status     STRING
,master_project_code    STRING
,project_manager        STRING
,project_director       STRING
,segment_lead           STRING
,key2                   STRING
,role                   STRING
,rule_type              STRING
,`function`             STRING
,key4                   STRING
,query_id               STRING
,date_opened            date
,closed_date            date
,days_open              bigint
,status                 STRING
,dq_score               DOUBLE
,week_details           STRING
)""")
