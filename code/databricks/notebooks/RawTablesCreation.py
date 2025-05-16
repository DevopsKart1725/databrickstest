# Databricks notebook source
# MAGIC %run ./RawTables-DDL

# COMMAND ----------

# %run ./EDL_RawTablesCreation

# COMMAND ----------

import datetime
from pyspark.sql.functions import col,lit

catalogue_env = dbutils.widgets.get("adb_catalogue_env")
work_schema=catalogue_env+".synhdq_work"
# catalogue_env="iep_dev"
# work_schema="iep_dev"+".synhdq_work"


# COMMAND ----------

# Get today's date
today = datetime.date.today()
# Format date as dd-mm-yyyy
date_str = today.strftime("%d-%m-%Y")
# Print the date
print(date_str)
# date_str="21-05-2024"




# COMMAND ----------

# Get the list of folders inside the directory
folders_df = dbutils.fs.ls("/Volumes/"+catalogue_env+"/synhdq_raw/synhdq_raw/raw_data/"+date_str)
# Sort the list of folders by their modification time in descending order
sorted_folders = sorted(folders_df, key=lambda x: x.modificationTime, reverse=True)
# Get the latest folder
latest_folder = sorted_folders[0]
# Extract the path of the latest folder
latest_folder_path = latest_folder.path
# Print the path of the latest folder
print(latest_folder_path)

# COMMAND ----------


#specify columns and datatypes for rawtables
edh_exceptions_dtype_dict={"entity_name":"STRING","flag_id":"bigint","exception":"STRING","exception_reason":"STRING","network_id":"STRING","flagged_date":"Date","other_reason":"STRING","is_approved":"STRING"}
edh_score_dtype_dict={"entity_name":"STRING","key1":"STRING","Key2":"STRING","key4":"STRING","failed_count":"bigint","pass_count":"bigint","extract_date":"Date"}
edh_query_details_dtype_dict={"entity_name":"STRING","flex1":"STRING","key1":"STRING","key2":"STRING","subject_area":"STRING","generic_query_text":"STRING","extract_date":"Date","flex2":"STRING","flex3":"STRING","flex4":"STRING","flex5":"STRING","flex6":"STRING","target_field":"STRING","key3":"STRING","flex7":"STRING","flex8":"STRING","flex9":"STRING","key4":"STRING","system_site_status":"STRING","country_startup_specialist":"STRING","flex10":"STRING",#"project_status":"STRING",
                              "dli_refresh_time":"Date","flex11":"STRING","region":"STRING"}
edh_rules_dtype_dict={"entity_name":"STRING","key4":"STRING","priority":"Int","rule_type":"STRING","function":"STRING","key2":"STRING","activated_date":"Date","decommissioned_date":"Date","role":"STRING"}
edh_flag_reactivation_dtype_dict={"entity_name":"STRING","flag_id":"bigint","network_id":"STRING","reactivate_date":"Date"}
iep_edh_score_detail_dtype_dict={"entity_name":"STRING","project_code":"STRING","check_no":"string","failed_count":"bigint","pass_count":"bigint","source_system":"STRING","extract_date":"date","site_id":"string","int_site_id":"string"}
edh_rules_attributes_dtype_dict={"entity_name":"STRING","transaction_id":"string","rule_no":"string","type":"string","value":"string","subtype":"string"}
edh_rule_disabled_records_dtype_dict={"entity_name":"string","key4":"string","generic_query_text":"string","master_project_code":"string","key2":"string","status":"string","sponsor":"string","disable_reason":"string","other_reason":"string","user_id":"string","disabled_type":"string"}


edh_exceptions_cols=["flag_id","exception","exception_reason","network_id","flagged_date","other_reason","is_approved"]
edh_score_cols=["key1","key2","key4","failed_count","pass_count","extract_date"]
edh_query_details_cols=["flex1","key1","key2","subject_area","generic_query_text","extract_date","flex2","flex3","flex4","flex5","flex6","target_field","key3","flex7","flex8","flex9","key4","system_site_status","country_startup_specialist","flex10",#"project_status",
                        "dli_refresh_time","flex11","region"]
edh_rules_cols=["key4","priority","rule_type","function","key2","activated_date","decommissioned_date","role"]
edh_flag_reactivation_cols=["flag_id","network_id","reactivate_date"]
edh_rule_disabled_records_cols=["key4", "generic_query_text", "master_project_code", "key2", "status", "sponsor", "disable_reason", "other_reason", "user_id","disabled_type"]


iep_edh_score_detail_cols=["project_code","check_no","failed_count","pass_count","source_system","extract_date","site_id","int_site_id"]
edh_rules_attributes_cols=["transaction_id","rule_no","type","value","subtype"]

# COMMAND ----------

def cast_columns(df, column_dict,colmn):
    df = df.select(lit("project").alias("entity_name"),*colmn)
    for column in df.columns:
        if column in column_dict:
            # print(column_dict[column]+"   "+column)
            df = df.withColumn(column, df[column].cast(column_dict[column]))
    return df

# COMMAND ----------

tables_df = dbutils.fs.ls(latest_folder_path)
print(tables_df)

# COMMAND ----------

#get table folders list
tables_df = dbutils.fs.ls(latest_folder_path)

for table in tables_df:
    pth = table.path.replace("dbfs:","")

    tbl = pth.split("/")[-2].split(".")[-1].replace("EDQ","EDH").replace("_RAW","")
    print(tbl)

    formt="parquet"

    df = spark.read.format(formt).load(pth)
    print(pth)
    # df.printSchema()
    
    # df.display()
    #df.write.mode("overwrite").format("parquet").insertInto(Synhdq_raw."pth.split("/")[-2]")
    #load dataframe in work tables
    if(tbl=="EDH_RULES"):
        dct = edh_rules_dtype_dict
        cols = edh_rules_cols
        final_df = cast_columns(df,dct,cols)
        # final_df.write.mode("overwrite").format("delta").saveAsTable(work_schema+"."+tbl)
    elif(tbl=="EDH_FLAG_REACTIVATION"):
        dct = edh_flag_reactivation_dtype_dict
        cols = edh_flag_reactivation_cols
        final_df = cast_columns(df,dct,cols)
        final_df = final_df.dropDuplicates(["flag_id"])
    elif(tbl=="EDH_EXCEPTIONS"):
        dct = edh_exceptions_dtype_dict
        cols = edh_exceptions_cols
        final_df = cast_columns(df,dct,cols)
        final_df = final_df.dropDuplicates(["flag_id"])
    elif(tbl=="EDH_SCORE"):
        dct = edh_score_dtype_dict
        cols = edh_score_cols
        final_df = cast_columns(df,dct,cols)
        # final_df.write.mode("overwrite").format("delta").saveAsTable(work_schema+"."+tbl)
    elif(tbl=="EDH_QUERY_DETAILS"):
        dct = edh_query_details_dtype_dict
        cols = edh_query_details_cols
        final_df = cast_columns(df,dct,cols)
        final_df = final_df.dropDuplicates(["key1","key2","key3","key4"])
        # display(final_df)
        # final_df.write.mode("overwrite").format("delta").saveAsTable(work_schema+"."+tbl)
    elif(tbl=="IEP_EDH_SCORE_DETAIL"):
        dct = iep_edh_score_detail_dtype_dict
        cols = iep_edh_score_detail_cols
        final_df = cast_columns(df,dct,cols)
    elif(tbl=="EDH_RULES_ATTRIBUTES"):
        dct = edh_rules_attributes_dtype_dict
        cols = edh_rules_attributes_cols
        final_df = cast_columns(df,dct,cols)
    elif(tbl=="EDH_RULE_DISABLED_RECORDS"):
        dct = edh_rule_disabled_records_dtype_dict
        cols = edh_rule_disabled_records_cols
        final_df = cast_columns(df,dct,cols)
        
    final_df.printSchema()
    print(final_df.count())
    # final_df = final_df.dropDuplicates()
    # print(final_df.count())


    final_df.write.mode("overwrite").format("delta").saveAsTable(work_schema+"."+tbl)


# COMMAND ----------

from pyspark.sql import DataFrame

def vacuum_table(table_name: str, retain_days: int) -> DataFrame:
    return spark.sql(f"VACUUM {catalogue_env}.{table_name} RETAIN {retain_days} HOURS")

tables_to_vacuum = ["synhdq_work.EDH_RULES", "synhdq_work.EDH_FLAG_REACTIVATION", "synhdq_work.EDH_EXCEPTIONS", "synhdq_work.EDH_SCORE", "synhdq_work.EDH_QUERY_DETAILS","synhdq_work.IEP_EDH_SCORE_DETAIL","synhdq_work.EDH_RULES_ATTRIBUTES"]

for table in tables_to_vacuum:
    vacuum_table(table, 50 * 24)  # Convert days to hours

# COMMAND ----------

# # Convert python variable to shell variable
# shell_variable = f"export MY_VARIABLE={catalogue_env}"

# COMMAND ----------

# %sh
# find /Volumes/$shell_variable/synhdq_raw/synhdq_raw/raw_data/ -iname "*.parquet" -mtime +50 -exec rm -rf {} \;

# COMMAND ----------

# MAGIC %md
# MAGIC checking latest data is coming from EDQ or not in score and query details

# COMMAND ----------

# import datetime
today = datetime.date.today()
is_backdate_process=dbutils.widgets.get("is_backdate_process")

extrct_date_qd = spark.sql(f"select extract_date from {work_schema}.edh_query_details order by extract_date desc").collect()[0][0]
extrct_date_sc = spark.sql(f"select extract_date from {work_schema}.edh_score order by extract_date desc").collect()[0][0]

if (is_backdate_process == "no"):
    datestr = today.strftime("%Y-%m-%d")
    if ((datestr == str(extrct_date_qd)) and (datestr == str(extrct_date_sc))):
        exit(0)
    else:
        print("today: "+datestr)
        print("extrct_date_query_details: "+str(extrct_date_qd))
        print("extrct_date_score: "+str(extrct_date_sc))
        raise Exception("The dates do not match. It seems like EDQ tables are not refreshed at OCI end. Please check with EDQ  team")
