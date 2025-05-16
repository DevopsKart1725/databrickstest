# Databricks notebook source
df_hist = spark.read.format("parquet").load("/Volumes/iep_dev/synhdq_raw/synhdq_raw/hist_data/21-06-2024/112714/EDQ.SBI_EDQ_QUERY_DETAILS/")

# COMMAND ----------

df1=spark.read.table("iep_dev.synhdq_encur.snap_edq_query_details")

# COMMAND ----------

col_name_dict={"query_id":"query_id","project_code":"key1","source_system":"key2","query_text":"key3","rule_id":"key4","date_opened":"date_opened","closed_date":"closed_date","days_open":"days_open","status":"status","exception_flag":"exception_flag","flag_priority":"flag_priority","customer":"flex1","subject_area":"subject_area","generic_query_text":"generic_query_text","extract_date":"extract_date","country_cd":"flex2","country_name":"flex3","site_number":"flex4","pi_name":"flex5","subject_number":"flex6","target_field":"target_field","int_facilityid":"flex7","facility":"flex8","monitor":"flex9","system_site_status":"system_site_status","country_startup_specialist":"country_startup_specialist","flag_owner":"flex10","dli_refresh_time":"dli_refresh_time","contract_co":"flex11","region":"region"}

col_type_dict={"entity_name":"string","query_id":"long","key1":"string","key2":"string","key3":"string","key4":"string","date_opened":"date","closed_date":"date","days_open":"long","status":"string","exception_flag":"string","flag_priority":"integer","flex1":"string","subject_area":"string","generic_query_text":"string","extract_date":"date","flex2":"string","flex3":"string","flex4":"string","flex5":"string","flex6":"string","target_field":"string","flex7":"string","flex8":"string","flex9":"string","system_site_status":"string","country_startup_specialist":"string","flex10":"string","dli_refresh_time":"timestamp","flex11":"string","region":"string"}

hist_col_list=["query_id","project_code","source_system","query_text","rule_id","date_opened","closed_date","days_open","status","exception_flag","flag_priority","customer","subject_area","generic_query_text","extract_date","country_cd","country_name","site_number","pi_name","subject_number","target_field","int_facilityid","facility","monitor","system_site_status","country_startup_specialist","flag_owner","dli_refresh_time","contract_co","region"]

col_list=["query_id","key1","key2","key3","key4","date_opened","closed_date","days_open","status","exception_flag","flag_priority","flex1","subject_area","generic_query_text","extract_date","flex2","flex3","flex4","flex5","flex6","target_field","flex7","flex8","flex9","system_site_status","country_startup_specialist","flex10","dli_refresh_time","flex11","region"]

# COMMAND ----------

for i in hist_col_list:
    df_hist = df_hist.withColumnRenamed(i,col_name_dict[i])

# COMMAND ----------

for i in col_list:
    df_hist = df_hist.withColumn(i,df_hist[i].cast(col_type_dict[i])).select(col_list)

# COMMAND ----------

df_hist.write.mode("overwrite").saveAsTable("iep_dev.synhdq_encur.snap_edq_query_details_test")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from iep_dev.synhdq_encur.snap_edq_query_details_test

# COMMAND ----------


