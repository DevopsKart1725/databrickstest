# Databricks notebook source
from pyspark.sql.functions import expr,date_sub,row_number,col,lit, broadcast,when,desc,rank,max
from pyspark.sql.window import WindowSpec,Window

# COMMAND ----------

catalogue_env = dbutils.widgets.get("adb_catalogue_env")
# catalogue_env="iep_dev"

# COMMAND ----------

from datetime import datetime, date
today = date.today()
# Format date as dd-mm-yyyy
date_str = today.strftime("%d-%m-%Y")
# Print the date
print(date_str)
# date_str="01-07-2024"

# COMMAND ----------

# Get the list of folders inside the directory
folders_df = dbutils.fs.ls("/Volumes/"+catalogue_env+"/synhdq_raw/synhdq_raw/hist_data/"+str(date_str))
# Sort the list of folders by their modification time in descending order
sorted_folders = sorted(folders_df, key=lambda x: x.modificationTime, reverse=True)
# Get the latest folder
latest_folder = sorted_folders[0]
# Extract the path of the latest folder
latest_folder_path = latest_folder.path
# Print the path of the latest folder
print(latest_folder_path)

# COMMAND ----------

df_hist = spark.read.format("parquet").load(f"{latest_folder_path}/EDQ.SBI_EDQ_QUERY_DETAILS/")

# COMMAND ----------

df_exc=spark.read.format("parquet").load(f"{latest_folder_path}/EDHDB.EDH_EXCEPTIONS/")
df_excpt_qid=df_exc.toDF(*[col.lower() for col in df_exc.columns]).select(col("flag_id").cast("long"))

# df_excpt_qid=spark.table("iep_dev.synhdq_work.edh_exceptions").select("flag_id").distinct().collect()


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

from pyspark.sql.functions import regexp_replace, col, when

# Define the condition using regular expression
condition = (col("key4").rlike(r"^\d{4}$") & ~col("key4").rlike(r"\."))

# Replace 4-digit rule id with the same id followed by .00
df_hist = df_hist.withColumn("key4", when(condition, regexp_replace("key4", r"(\b\d{4}\b)", "$1.00")).otherwise(col("key4")))

# COMMAND ----------

# df_hist.write.mode("overwrite").saveAsTable("iep_dev.synhdq_encur.snap_edq_query_details_test")

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

# if(catalogue_env!="iep_prd"):
spark.sql(f"DROP TABLE IF EXISTS {catalogue_env}.synhdq_encur.snap_edq_query_details_bkp")

# COMMAND ----------

# if(catalogue_env!="iep_prd"):
spark.sql(f"create table if not exists {catalogue_env}.synhdq_encur.snap_edq_query_details_bkp as select * from {catalogue_env}.synhdq_encur.snap_edq_query_details")

# COMMAND ----------

# if(catalogue_env!="iep_prd"):
spark.sql(f"delete from {catalogue_env}.synhdq_encur.snap_edq_query_details")

# COMMAND ----------

window_spec = Window.partitionBy("key1","key2","key3","key4").orderBy(desc("date_opened"))
df = df_hist.withColumn("rank",row_number().over(window_spec)).filter(col("rank")==1).drop("rank")

# insert overwrite table iep_dev.synhdq_encur.snap_edq_query_details_test SELECT *
# FROM iep_dev.synhdq_encur.snap_edq_query_details_test
# qualify row_number() over (partition by key1,key2,key3,key4 order by date_opened desc)=1;
 

# COMMAND ----------

df = df.withColumn("status", when((col("status").isNull() | (col("status") == '')) & (col("exception_flag") == "Y"), "E").otherwise(df["status"]))


# WHEN status is null and exception_flag ='Y'THEN change status to E

# COMMAND ----------

df = df.join(broadcast(df_excpt_qid), df["query_id"] == df_excpt_qid["flag_id"], "left").withColumn("case_result", 
                   when((col("status") == 'C') & (col("exception_flag") == 'N'),lit('A'))
                   .when((col("status") == 'A') & (col("exception_flag") == 'N'),lit('A'))
                   .when((col("status") == 'E') & (col("exception_flag") == 'Y'), when( col("query_id") == col("flag_id"),lit('A')).otherwise(lit('NA')))
                   .otherwise(lit('NA'))).filter(col("case_result")=="A").drop("case_result").drop("flag_id")
                   

# COMMAND ----------

# df = spark.read.table("iep_dev.synhdq_encur.snap_edq_query_details_test")

df_query_details_hist_2y = df.selectExpr("*") \
    .where(
        expr("""
            CASE 
                WHEN status = 'C' AND exception_flag = 'N' THEN 
                    CASE 
                        WHEN date_opened <= CURRENT_DATE AND date_opened >= "2023-01-01" THEN 'A'
                        ELSE 'NA' 
                    END
                WHEN status = 'A' AND exception_flag = 'N' THEN 'A'
                WHEN status = "E" AND exception_flag = 'Y' THEN 'A'
                ELSE 'NA2' 
            END == 'A'
        """)
    )
df_query_details_hist_more_than_2y = df.selectExpr("*") \
    .where(
        expr("""
            CASE 
                WHEN status = 'C' AND exception_flag = 'N' THEN 
                    CASE 
                        WHEN date_opened <= CURRENT_DATE AND date_opened > "2022-12-31" THEN 'A'
                        ELSE 'NA' 
                    END
                ELSE 'NA2' 
            END == 'NA'
        """)
    )


# COMMAND ----------

windowSpec = Window.orderBy(lit('A'))  # Using a constant value because we just need a sequential number
df_query_details_hist_more_than_2y = df_query_details_hist_more_than_2y.withColumn("query_id", row_number().over(windowSpec)).withColumn("query_id", col("query_id").cast("long"))


# COMMAND ----------

max_query_id = df_query_details_hist_more_than_2y.agg({"query_id": "max"}).collect()[0][0]
print(max_query_id)

# COMMAND ----------

windowSpec = Window.orderBy(lit('A'))
df_query_details_hist_2y = df_query_details_hist_2y.withColumn("ref_query_id", df_query_details_hist_2y["query_id"]).withColumn("query_id", max_query_id + row_number().over(windowSpec)).withColumn("query_id", col("query_id").cast("long"))
# display(df_query_details_hist_2y)
# df_query_details_hist_2y.count()                                                              

# COMMAND ----------

# MAGIC %md
# MAGIC saving tables

# COMMAND ----------

spark.sql(f"drop table if exists {catalogue_env}.synhdq_encur.snap_edq_query_details_archive")

# COMMAND ----------

spark.sql(f"""CREATE table if not exists {catalogue_env}.synhdq_encur.snap_edq_query_details_archive(
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

edq_query_details_tbl_name = f"{catalogue_env}.synhdq_encur.snap_edq_query_details"
edq_query_details_tbl_name_stg = f"{edq_query_details_tbl_name}_stg"
spark.sql(f"drop table if exists {edq_query_details_tbl_name_stg}")
df_query_details_hist_2y_df=df_query_details_hist_2y.withColumn("entity_name",lit("project"))
df_query_details_hist_2y_df.write.mode("overwrite").saveAsTable(edq_query_details_tbl_name_stg)

df_query_details_hist_more_than_2y_df=df_query_details_hist_more_than_2y.select(lit("project").alias("entity_name"),"*")
df_query_details_hist_more_than_2y_df.write.mode("overwrite").saveAsTable(f"{edq_query_details_tbl_name}_archive") 

# COMMAND ----------

# MAGIC %md
# MAGIC updating exceptions flag_id in the exception table and populating to OCI
# MAGIC

# COMMAND ----------

df_query_details_hist_2y_tbl = spark.sql(f"select * from {edq_query_details_tbl_name_stg}")

# COMMAND ----------

df_query_details_hist_2y_excptn = df_query_details_hist_2y_tbl.filter("status = 'E' AND exception_flag = 'Y'")
df_query_details_hist_2y_excptn.count()
# df_query_details_hist_2y_excptn.select("query_id","ref_query_id").display()

# COMMAND ----------

df_exc=df_exc.withColumn("flag_id", col("flag_id").cast("long"))

# COMMAND ----------

# MAGIC %md
# MAGIC require only the rows present in df_query_details_hist_2y_excptn to be present in df_exc removing the rest- inner join

# COMMAND ----------

spark.sql(f"drop table if exists {catalogue_env}.synhdq_encur.edh_exceptions")

# COMMAND ----------

spark.sql(f"""
CREATE TABLE if not exists {catalogue_env}.synhdq_encur.edh_exceptions (
  FLAG_ID STRING,
  EXCEPTION STRING,
  EXCEPTION_REASON STRING,
  NETWORK_ID STRING,
  FLAGGED_DATE TIMESTAMP,
  OTHER_REASON STRING,
  CREATED_TS TIMESTAMP,
  CREATED_BY STRING,
  UPDATED_TS TIMESTAMP,
  UPDATED_BY STRING,
  IS_APPROVED STRING,
  TYPE STRING,
  REACTIVATION_DATE TIMESTAMP)""")

# COMMAND ----------

from pyspark.sql.functions import col,lit,regexp_extract
cols=df_exc.columns
df_excptn_updated = df_exc.join(df_query_details_hist_2y_excptn, df_exc["flag_id"] == df_query_details_hist_2y_excptn["ref_query_id"], "right")

df_excptn_updated=df_excptn_updated.drop("flag_id").withColumnRenamed("query_id","flag_id").withColumn("flag_id", col("flag_id").cast("string")).select(*[cols]).withColumn("EXCEPTION", lit("Y")).withColumn("starts_with_a_and_number", regexp_extract(col("NETWORK_ID"), "^a[0-9]+$", 0) != "")

df_excptn_updated=df_excptn_updated.withColumn("NETWORK_ID",when((df_excptn_updated["starts_with_a_and_number"] == "true"), df_excptn_updated["NETWORK_ID"]).otherwise(lit("a033905"))).drop("starts_with_a_and_number")
print(df_excptn_updated.count())
df_excptn_updated.write.mode("overwrite").saveAsTable(f"{catalogue_env}.synhdq_encur.edh_exceptions")

# COMMAND ----------

df_query_details_hist_2y_tbl.drop("ref_query_id").write.mode("overwrite").format("delta").saveAsTable(edq_query_details_tbl_name)
