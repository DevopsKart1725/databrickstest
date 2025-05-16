# Databricks notebook source
# MAGIC %run ./EncurTables-DDL

# COMMAND ----------

# catalogue_env= "iep_dev"
# edl_catalog_env="edl_dev"

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, desc, row_number,lit,length,expr,coalesce,when,cast,current_date, date_diff,min,max,when,datediff
from pyspark.sql import functions as F

# COMMAND ----------

from pyspark.sql import DataFrame

# Load the first part of the union into a DataFrame
df1: DataFrame = spark.table(f"{edl_catalog_env}.prc_presentation.sync_access").select(
    "network_user", "access_basis", "project_code", "grm_role", lit(None).cast("string").alias("ebs_role")
)

# Load the data for the second part of the union into a DataFrame
df2_source: DataFrame = spark.table(f"{edl_catalog_env}.prc_presentation.prc_study_roles").where(
    (F.col("proj_role").like("%PFA%")) | (F.col("proj_role").like("%SEG%"))
)

# Transform the second DataFrame
df2: DataFrame = df2_source.select(
    F.concat(F.lit("a"), "employee_id").alias("network_user"),
    F.concat(F.lit("project "), "project_code").alias("access_basis"),
    "project_code",
    lit(None).cast("string").alias("grm_role"),
    F.col("proj_role").alias("ebs_role")
)

# Union the two DataFrames
df_union: DataFrame = df1.union(df2)

# Write the result to a table
df_union.write.mode("overwrite").saveAsTable(f"{catalogue_env}.synhdq_encur.snap_edq_user_access")

# COMMAND ----------

spark.sql(f"""insert overwrite table {catalogue_env}.synhdq_encur.snap_edq_source_refresh
select * from {edl_catalog_env}.prc_presentation.source_refresh""")

# COMMAND ----------

# # Load data
# pm = spark.table(f"{catalogue_env}.synhdq_work.cdm_project_mapping")
# csm = spark.table(f"{catalogue_env}.synhdq_work.child_source_mapping")


# # Perform necessary transformations
# window_spec = Window.partitionBy(pm["child_project_code"], csm["derived_child_source"]) \
#                    .orderBy(desc("last_processed_date"))

# cdm = pm.join(csm, pm["child_source"] == csm["child_source"], "left") \
#         .withColumn("row_num", row_number().over(window_spec)) \
#         .filter(col("row_num") == 1) \
#         .select(pm["child_project_code"],
#                 pm["master_project_code"],
#                 csm["derived_child_source"].alias("child_source"))
                
# sgi = spark.table(f"{edl_catalog_env}.prc_presentation.sync_global_index") \
#           .selectExpr("owning_business_unit as business_unit", 
#                   "contract_attribute as contract_category", 
#                   "sponsor_parent_company_name as parent_sponsor", 
#                   "sponsor_name", 
#                   "study_status1 as project_status", 
#                   "study_sub_status1 as project_sub_status", 
#                   "project_code", 
#                   "project_lead as project_manager", 
#                   "pd_name as project_director") \
#           .distinct()

# sr = spark.table(f"{edl_catalog_env}.prc_presentation.prc_study_roles") \
#          .where(col("proj_role") == "SEGLEAD") \
#          .selectExpr("project_code", "employee_name as segment_lead") \
#          .distinct()
         
# result = cdm.join(sgi.alias("sgi"), cdm["master_project_code"] == sgi["project_code"], "right") \
#             .join(sr, sgi["project_code"] == sr["project_code"], "left") \
#             .selectExpr("'project' as entity_name",
#                         "business_unit",
#                         "contract_category",
#                         "parent_sponsor",
#                         "sponsor_name",
#                         "project_status",
#                         "project_sub_status",
#                         "child_project_code as project_code", #key1
#                         "master_project_code",
#                         "child_source", #key2 ask shilpa to change as well
#                         "project_manager",
#                         "project_director",
#                         "segment_lead")

# COMMAND ----------

# Load the data from the relevant tables
cdm_project_mapping = spark.table(f"{catalogue_env}.synhdq_work.cdm_project_mapping")
sbi_child_source_mapping = spark.table(f"{catalogue_env}.synhdq_work.child_source_mapping")
sync_global_index = spark.table(f"{edl_catalog_env}.prc_presentation.sync_global_index")
prc_study_roles = spark.table(f"{edl_catalog_env}.prc_presentation.prc_study_roles")
pm_project_system = spark.table(f"{edl_catalog_env}.prc_presentation.pm_project_system")

# Define a window specification
windowSpec = Window.partitionBy("child_project_code", "derived_child_source").orderBy(col("last_processed_date").desc())

# Process the cdm_project_mapping and sbi_child_source_mapping with window function
cdm_filtered = cdm_project_mapping \
    .join(sbi_child_source_mapping, cdm_project_mapping.child_source == sbi_child_source_mapping.child_source, "left") \
    .withColumn("row_num", row_number().over(windowSpec)) \
    .filter(col("row_num") == 1) \
    .select(col("child_project_code"), col("master_project_code"), col("derived_child_source").alias("child_source")) \
    .distinct()

# Process sync_global_index
sgi_filtered = sync_global_index \
    .select(
        col("owning_business_unit").alias("business_unit"),
        col("contract_attribute").alias("contract_category"),
        col("sponsor_parent_company_name").alias("parent_sponsor"),
        col("sponsor_name"),
        col("study_status1").alias("project_status"),
        col("study_sub_status1").alias("project_sub_status"),
        col("sync_global_index.project_code"),
    ) \
    .distinct()

# Process prc_study_roles for segment leads
sr_filtered = prc_study_roles \
    .filter(col("proj_role") == "SEGLEAD") \
    .select(
        col("prc_study_roles.project_code"),
        col("employee_name").alias("segment_lead")
    ) \
    .distinct()
	
# DPDRoles logic
dpd_window = Window.partitionBy("project_code").orderBy(
    col("proj_role"), col("lead_indicator"), col("role_start")
)
dpd_roles = prc_study_roles \
    .filter(col("proj_role") == "XPD") \
    .withColumn("rn", row_number().over(dpd_window)) \
    .filter(col("rn") == 1) \
    .select(
        col("project_code").alias("dpd_project_code"),
        col("employee_name").alias("dpd_employee_name"),
        col("rn")
    )

# LeadRoles logic
lead_window = Window.partitionBy("project_code").orderBy(
    when(col("proj_role") == "PRJMGR", 1)
    .when(col("proj_role") == "PL", 2)
    .otherwise(11),
    col("lead_indicator"),
    col("role_start")
)
lead_roles = prc_study_roles \
    .withColumn("rn", row_number().over(lead_window)) \
    .filter(col("rn") == 1) \
    .select(
        col("project_code"),
        col("proj_role"),
        col("proj_role_label"),
        col("employee_name").alias("lead_employee_name"),
        col("rn")
    )

# Extract Project_Lead and DPD roles
roles_combined = lead_roles.alias("lr") \
    .join(
        dpd_roles.alias("dr"),
        (col("lr.project_code") == col("dr.dpd_project_code")) & (col("dr.rn") == 1),
        "left"
    ) \
    .join(
        pm_project_system
        .select("project_code").distinct().alias("pps"),
        col("lr.project_code") == col("pps.project_code"),
        "inner"
    ) \
    .select(
        col("lr.project_code"),
        when((col("lr.proj_role").isin("PL", "PRJMGR")) & (col("lr.proj_role_label") == "PRJMGR"), col("lr.lead_employee_name"))
        .otherwise(lit(None)).alias("project_lead"),
        when(col("dr.rn") == 1, col("dr.dpd_employee_name"))
        .otherwise(lit(None)).alias("DPD")
    )

# COMMAND ----------

# Join all parts together
result = cdm_filtered \
    .join(sgi_filtered.alias("sgi"), cdm_filtered["master_project_code"] == sgi_filtered["project_code"], "right") \
    .join(roles_combined.alias("roles"), col("sgi.project_code") == col("roles.project_code"), "left") \
    .join(sr_filtered.alias("sr"), col("sgi.project_code") == col("sr.project_code"), "left") \
    .selectExpr(
        "'project' as entity_name",
        "business_unit",
        "contract_category",
        "parent_sponsor",
        "sponsor_name",
        "project_status",
        "project_sub_status",
        "child_project_code as project_code",  # Key1
        "master_project_code",
        "child_source",  # Key2
        "project_lead as project_manager",
        "DPD as project_director",
        "segment_lead"
    )


# COMMAND ----------

tbl= f"{catalogue_env}.synhdq_encur.snap_edq_project_details"
result.write.mode("overwrite").saveAsTable(tbl)

# COMMAND ----------

spark.sql(f"""drop table if exists {catalogue_env}.synhdq_work.dev_temp_edh_query_details""")

# COMMAND ----------

raw = spark.table(f"{catalogue_env}.synhdq_work.edh_query_details").alias("raw")
tgt = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_query_details").alias("tgt")

joined_df1 = raw.join(tgt, (raw["key1"] == tgt["key1"]) &
                          (raw["key2"] == tgt["key2"]) &
                          (raw["key3"] == tgt["key3"]) &
                          (raw["key4"] == tgt["key4"]), "inner") \
                .selectExpr("tgt.query_id", "raw.*")

mq = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_query_details") \
         .agg(F.max(F.col("query_id")).alias("max_query_id")) \
         .selectExpr("coalesce(max_query_id, 0) as max_query_id")

joined_df2 = raw.join(tgt, (raw["key1"] == tgt["key1"]) &
                          (raw["key2"] == tgt["key2"]) &
                          (raw["key3"] == tgt["key3"]) &
                          (raw["key4"] == tgt["key4"]), "leftanti") \
                .crossJoin(mq) \
                .withColumn("query_id", mq["max_query_id"] + row_number().over(Window.orderBy("raw.extract_date"))) \
                .selectExpr("query_id", "raw.*")

final_df = joined_df1.union(joined_df2)
# display(joined_df2.select(max("query_id")))
# display(final_df.orderBy("query_id").count())




# COMMAND ----------

# Write final_df to a new table
final_df.write.mode("overwrite").saveAsTable(f"{catalogue_env}.synhdq_work.dev_temp_edh_query_details")

# COMMAND ----------

spark.sql(f"""drop table if exists {catalogue_env}.synhdq_work.edh_query_details_final_stg""")

# COMMAND ----------

rm = spark.table(f"{catalogue_env}.synhdq_work.dev_temp_edh_query_details").alias("rm")
fr = spark.table(f"{catalogue_env}.synhdq_work.edh_flag_reactivation").alias("fr")
e = spark.table(f"{catalogue_env}.synhdq_work.edh_exceptions").alias("e")
qd = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_query_details").alias("qd")

joined_temp_excptn = rm.join(e, rm["query_id"] == e["flag_id"], "full_outer")\
    .join(fr, rm["query_id"] == fr["flag_id"], "left")\
    .withColumn("exception_reactivation_status_temp",
                when((col("rm.query_id").isNotNull()) & (col("e.flag_id").isNotNull()) & (col("fr.flag_id").isNull()), "OPEN_EXCEPTIONS")
                .when((col("rm.query_id").isNull()) & (col("e.flag_id").isNotNull()) & (col("fr.flag_id").isNull()), "CLOSE_EXCEPTIONS")
                .when((col("rm.query_id").isNotNull()) & (col("e.flag_id").isNull()) & (col("fr.flag_id").isNotNull()), "OPEN_REACTIVATIONS")
                )\
    .select(coalesce(col("rm.query_id"), col("e.flag_id")).alias("query_id").cast("bigint"),
            col("exception_reactivation_status_temp"),
            coalesce(col("rm.entity_name"), col("e.entity_name")).alias("entity_name"),
            col("rm.flex1"),
            col("rm.key1"),
            col("rm.key2"),
            col("rm.subject_area"),
            col("rm.generic_query_text"),
            col("rm.extract_date"),
            col("rm.flex2"),
            col("rm.flex3"),
            col("rm.flex4"),
            col("rm.flex5"),
            col("rm.flex6"),
            col("rm.target_field"),
            col("rm.key3"),
            col("rm.flex7"),
            col("rm.flex8"),
            col("rm.flex9"),
            col("rm.key4"),
            col("rm.system_site_status"),
            col("rm.country_startup_specialist"),
            col("rm.flex10"),
            col("rm.dli_refresh_time"),
            col("rm.flex11"),
            col("rm.region"),
            col("e.exception")
            )

joined_temp_tgt = joined_temp_excptn.alias("joined_temp_excptn").join(qd, qd["query_id"] == joined_temp_excptn["query_id"], "full_outer")\
    .withColumn("exception_reactivation_status", 
                when((col("exception").like("%Y%")) & (~col("status").like("C")), 'OPEN_EXCEPTIONS')
                .otherwise(joined_temp_excptn["exception_reactivation_status_temp"])).drop("joined_temp_excptn.exception_reactivation_status_temp")\
    .withColumn("derived_date_opened",
                when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNull()), joined_temp_excptn["extract_date"])
                .when((joined_temp_excptn["query_id"].isNull()) & (qd["query_id"].isNotNull()), qd["date_opened"])
                .when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNotNull()),
                      when(((qd["status"].like('%C%')) & (qd["exception_flag"].like('%N%')) & (col("exception_reactivation_status").isNull())), joined_temp_excptn["extract_date"]).otherwise(qd["date_opened"])
                  )
                )\
      .withColumn("derived_exception_flag", 
                when(col("exception_reactivation_status").isin('OPEN_EXCEPTIONS', 'CLOSE_EXCEPTIONS'), 'Y')
                .otherwise('N'))\
      .withColumn("derived_closed_date",
                when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNull()), lit(None))
                .when((joined_temp_excptn["query_id"].isNull()) & (qd["query_id"].isNotNull()),
                      when(qd["status"].isin('A', 'E','A ', 'E ',' A', ' E'), current_date()).otherwise(qd["closed_date"]))
                .when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNotNull()),
                      when((qd["status"].isin('A', 'C','A ', 'C ',' A', ' C')) & (col("exception_flag").like('%N%')), lit(None))
                      .when(col("exception_reactivation_status").isin('OPEN_EXCEPTIONS', 'OPEN_REACTIVATIONS'), lit(None))
                      .when((col("exception_reactivation_status") == "CLOSE_EXCEPTIONS"),coalesce(qd["closed_date"], current_date()))
                      .otherwise(qd["closed_date"])))\
      .withColumn("status", 
                when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNull()), 'A')
                .when((joined_temp_excptn["query_id"].isNull()) & (qd["query_id"].isNotNull()), 'C')
                .when((joined_temp_excptn["query_id"].isNotNull()) & (qd["query_id"].isNotNull()),
                      when(col("exception_reactivation_status") == 'OPEN_EXCEPTIONS', 'E')
                      .when(col("exception_reactivation_status") == 'CLOSE_EXCEPTIONS', 'C')
                      .otherwise('A'))
                )\
      .withColumn("derived_days_open",
                when(col("derived_closed_date").isNull(), datediff(current_date(), col("derived_date_opened")))
                .otherwise(datediff(col("derived_closed_date"), col("derived_date_opened")))
                )\
      .withColumn("flag_priority", lit(None).cast("int"))\
.select(coalesce(joined_temp_excptn.entity_name, qd.entity_name).alias("entity_name"),
        coalesce(joined_temp_excptn.query_id, qd.query_id).alias("query_id"),
        coalesce(joined_temp_excptn.key1, qd.key1).alias("key1"),
        coalesce(joined_temp_excptn.key2, qd.key2).alias("key2"),
        coalesce(joined_temp_excptn.key3, qd.key3).alias("key3"),
        coalesce(joined_temp_excptn.key4, qd.key4).alias("key4"),
        col("derived_date_opened").alias("date_opened"),
        col("derived_closed_date").alias("closed_date"),
        col("derived_days_open").alias("days_open").cast("bigint"),
        col("status"),
        col("derived_exception_flag").alias("exception_flag"),
        col("flag_priority"),
        coalesce(joined_temp_excptn.flex1, qd.flex1).alias("flex1"),
        coalesce(joined_temp_excptn.subject_area, qd.subject_area).alias("subject_area"),
        coalesce(joined_temp_excptn.generic_query_text, qd.generic_query_text).alias("generic_query_text"),
        coalesce(joined_temp_excptn.extract_date, qd.extract_date).alias("extract_date"),
        coalesce(joined_temp_excptn.flex2, qd.flex2).alias("flex2"),
        coalesce(joined_temp_excptn.flex3, qd.flex3).alias("flex3"),
        coalesce(joined_temp_excptn.flex4, qd.flex4).alias("flex4"),
        coalesce(joined_temp_excptn.flex5, qd.flex5).alias("flex5"),
        coalesce(joined_temp_excptn.flex6, qd.flex6).alias("flex6"),
        coalesce(joined_temp_excptn.target_field, qd.target_field).alias("target_field"),
        coalesce(joined_temp_excptn.flex7, qd.flex7).alias("flex7"),
        coalesce(joined_temp_excptn.flex8, qd.flex8).alias("flex8"),
        coalesce(joined_temp_excptn.flex9, qd.flex9).alias("flex9"),
        coalesce(joined_temp_excptn.system_site_status, qd.system_site_status).alias("system_site_status"),
        coalesce(joined_temp_excptn.country_startup_specialist, qd.country_startup_specialist).alias("country_startup_specialist"),
        coalesce(joined_temp_excptn.flex10, qd.flex10).alias("flex10"),
        coalesce(joined_temp_excptn.dli_refresh_time, qd.dli_refresh_time).alias("dli_refresh_time"),
        coalesce(joined_temp_excptn.flex11, qd.flex11).alias("flex11"),
        coalesce(joined_temp_excptn.region, qd.region).alias("region"))

joined_temp_tgt=joined_temp_tgt.filter(col("date_opened").isNotNull())

# COMMAND ----------

# joined_temp_tgt.where("date_opened is null").display()
# joined_temp_tgt.select("status","exception_flag").distinct().display()

# COMMAND ----------

stg_table=f"{catalogue_env}.synhdq_work.edh_query_details_final_stg"
joined_temp_tgt.write.mode("overwrite").saveAsTable(stg_table)

# COMMAND ----------

pd_df = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_project_details")
edq_df = spark.table(f"{catalogue_env}.synhdq_work.edh_query_details_final_stg")
rules_df = spark.table(f"{catalogue_env}.synhdq_work.edh_rules")
rule_disabled_records_df = spark.table(f"{catalogue_env}.synhdq_work.edh_rule_disabled_records")

# COMMAND ----------

filtered_rule_disabled_records_df = rule_disabled_records_df.filter(rule_disabled_records_df["disabled_type"] == 'prj_src') ##disable_type=='prj_src'

prj_src_disabled_df = pd_df.join(filtered_rule_disabled_records_df, (pd_df.master_project_code == filtered_rule_disabled_records_df.master_project_code) & (pd_df.child_source == filtered_rule_disabled_records_df.key2), "inner") \
                       .select(pd_df.project_code,filtered_rule_disabled_records_df.key2)

print(edq_df.count())
print("number of distinct project codes getting disabled for src : "+str(prj_src_disabled_df.count()))
edq_df = edq_df.join(prj_src_disabled_df, 
                                             (edq_df["key1"] == prj_src_disabled_df["project_code"]) & 
                                             (edq_df["key2"] == prj_src_disabled_df["key2"]), 
                                             "leftanti")
print(edq_df.count())
# display(prj_src_disabled_df)

filtered_rule_disabled_records_df1 = rule_disabled_records_df.filter(rule_disabled_records_df["disabled_type"] == 'prj_rule') ##disable_type=='prj_rule'

prj_rule_disabled_df = pd_df.join(filtered_rule_disabled_records_df1, (pd_df.master_project_code == filtered_rule_disabled_records_df1.master_project_code) , "inner").join(rules_df, (rules_df.key4 == filtered_rule_disabled_records_df1.key4) , "inner") \
    .select(pd_df.project_code,filtered_rule_disabled_records_df1.key4,filtered_rule_disabled_records_df1.master_project_code)

print("number of distinct project codes getting disabled for rule : "+str(prj_rule_disabled_df.count()))
edq_df = edq_df.join(prj_rule_disabled_df, 
                                             (edq_df["key1"] == prj_rule_disabled_df["project_code"]) & 
                                             (edq_df["key4"] == prj_rule_disabled_df["key4"]), 
                                             "leftanti")
print(edq_df.count())
# display(edq_df)


# COMMAND ----------

table_name = f"{catalogue_env}.synhdq_work.edh_query_details_final_stg"
edq_df.write.mode("overwrite").saveAsTable(table_name)

# COMMAND ----------

spark.sql(f"""MERGE INTO {catalogue_env}.synhdq_work.edh_query_details_final_stg AS stg
USING (
  SELECT DISTINCT key2, key4, CAST(COALESCE(priority, 0) AS INT) AS Rule_priority 
  FROM {catalogue_env}.synhdq_work.edh_rules
) AS src
ON stg.key2 = src.key2 AND stg.key4 = src.key4
WHEN MATCHED THEN
UPDATE SET flag_priority = CAST(
  CASE 
    WHEN days_open >= 0 AND days_open <= 6 THEN Rule_priority
    WHEN days_open >= 7 AND days_open <= 13 THEN Rule_priority + 1
    WHEN days_open >= 14 AND days_open <= 20 THEN Rule_priority + 2
    WHEN days_open >= 21 AND days_open <= 27 THEN Rule_priority + 3
    WHEN days_open >= 28 AND days_open <= 34 THEN Rule_priority + 4
    WHEN days_open >= 35 AND days_open <= 41 THEN Rule_priority + 5
    WHEN days_open >= 42 AND days_open <= 48 THEN Rule_priority + 6
    WHEN days_open >= 49 AND days_open <= 55 THEN Rule_priority + 7
    WHEN days_open >= 56 AND days_open <= 62 THEN Rule_priority + 8
    WHEN days_open >= 63 AND days_open <= 69 THEN Rule_priority + 9
    WHEN days_open >= 70 THEN Rule_priority + 10
  END AS INT
)""")

# COMMAND ----------

spark.sql(f"""
insert overwrite {catalogue_env}.synhdq_encur.snap_edq_query_details
select * from {catalogue_env}.synhdq_work.edh_query_details_final_stg""")

# COMMAND ----------

spark.sql(f"""
insert overwrite {catalogue_env}.synhdq_encur.snap_edq_rule_disabled_records
select * from {catalogue_env}.synhdq_work.edh_rule_disabled_records""")

# COMMAND ----------

# MAGIC %md
# MAGIC score
# MAGIC

# COMMAND ----------

edq = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_query_details") \
           .withColumn("rn", row_number().over(Window.partitionBy("key1", "key2").orderBy(length(col("subject_area")).desc()))) \
           .filter(col("rn") == 1) \
           .drop("rn").alias("edq")

# Load and alias tables
es = spark.table(f"{catalogue_env}.synhdq_work.edh_score").alias("es")
epd = spark.table(f"{catalogue_env}.synhdq_encur.snap_edq_project_details").alias("epd")

# Perform left outer joins
joined_df = es.join(edq, 
                    (es["key1"] == edq["key1"]) & 
                    (es["key2"] == edq["key2"]) & 
                    (es["key4"] == edq["key4"]), 
                    "left")

joined_df = joined_df.join(epd, 
                           (es["key1"] == epd["project_code"]) & 
                           (epd["child_source"] == expr("IF(es.key2 = 'Enrollment Tracker', 'Salesforce', es.key2)")), 
                           "left")

# Perform final select with all required columns
result_df = joined_df.selectExpr(
    "'project' as entity_name",
    "es.key1",
    "es.key2",
    "es.key4",
    "es.failed_count",
    "es.pass_count",
    "es.extract_date",
    "(es.pass_count + es.failed_count) as no_of_evaluations",
    "epd.master_project_code",
    "SUM(CASE WHEN edq.status = 'A' THEN 1 ELSE 0 END) OVER (PARTITION BY edq.key1, edq.key2, edq.key4) as no_of_open_flags",
    "edq.subject_area",
    "SUM(CASE WHEN edq.exception_flag = 'Y' THEN 1 ELSE 0 END) OVER (PARTITION BY edq.key1, edq.key2, edq.key4) as exception_count",
    "IF(es.failed_count is null or es.failed_count = 0, 1, try_divide(es.pass_count, (no_of_evaluations - exception_count))) as dq_score"
)
result_df = result_df.withColumn("no_of_evaluations", col("no_of_evaluations").cast("integer"))

# result_df.filter(col("no_of_evaluations") == 0).display()

# COMMAND ----------

tbl= f"{catalogue_env}.synhdq_encur.snap_edq_fr_dq_score"
result_df.write.mode("overwrite").saveAsTable(tbl)
# spark.sql(f"drop table if exists {catalogue_env}.synhdq_encur.snap_edq_fr_dq_score")

# COMMAND ----------

from pyspark.sql import DataFrame

def vacuum_table(table_name: str, retain_days: int) -> DataFrame:
    return spark.sql(f"VACUUM {catalogue_env}.{table_name} RETAIN {retain_days} HOURS")

tables_to_vacuum = ['synhdq_encur.snap_edq_query_details', 'synhdq_encur.snap_edq_fr_dq_score','synhdq_encur.snap_edq_project_details']

for table in tables_to_vacuum:
    vacuum_table(table, 50 * 24)  # Convert days to hours
