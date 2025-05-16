# Databricks notebook source
iep_catalogue_env = dbutils.widgets.get("adb_catalogue_env")
edl_catalog_env = dbutils.widgets.get("edl_catalogue_env")

# COMMAND ----------

# iep_catalogue_env="iep_dev"

# COMMAND ----------

tables_to_copy = [
    "account_code__c",
    "account",
    "case",
    "project_information__c",
    "internal_financial_request__c",
    "opportunity"
]

for table in tables_to_copy:
    source_df = spark.table(f"{edl_catalog_env}.raw_sfdc_c.{table}")
    source_df.write.mode("overwrite").saveAsTable(f"{iep_catalogue_env}.synhdq_encur.{table}")

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Load the data
opportunity_df = spark.table(f"{iep_catalogue_env}.synhdq_encur.opportunity").filter(
    (F.col("project_code__c").isNotNull()) & 
    (F.col("project_sub_code__c").isNotNull())
)

account_code_df = spark.table(f"{iep_catalogue_env}.synhdq_encur.account_code__c")
project_information_df = spark.table(f"{iep_catalogue_env}.synhdq_encur.project_information__c")

windowSpec = Window.partitionBy("o.project_sub_code__c").orderBy(
    F.when((F.col("pi.project_start_date__c").isNotNull()) & (F.col("pi.project_end_date__c").isNotNull()), 1)
    .when(F.col("pi.project_end_date__c").isNotNull(), 2)
    .when(F.col("pi.project_start_date__c").isNotNull(), 3)
    .when(F.col("pi.sponsor_name__c") == F.col("ac.HQ_Account_Name__c"), 4)
    .otherwise(5),
    F.col("pi.project_end_date__c").desc(),
    F.col("pi.project_start_date__c").desc()
)

work_bench_sf_shrink_dup = opportunity_df.alias("o") \
    .join(account_code_df.alias("ac"), F.col("o.account_code__c") == F.col("ac.account_code__c"), "left") \
    .join(project_information_df.alias("pi"), F.col("o.id") == F.col("pi.opportunity__c"), "left") \
    .select(
        F.col("o.project_code__c"),
        F.col("o.project_sub_code__c"),
        F.col("o.opportunity_code__c"),
        F.col("o.primary_therapeutic_area_l2l__c"),
        F.col("o.secondary_therapeutic_area_l2l__c"),
        F.col("o.stagename"),
        F.col("o.owning_business_area__c"),
        F.col("o.owning_business_line__c"),
        F.col("o.owning_business_unit__c"),
        F.col("o.owning_sub_business_line__c"),
        F.col("o.owning_sub_business_unit__c"),
        F.col("o.closedate"),
        F.col("o.contracted_project_start_date__c"),
        F.col("o.contracted_project_end_date__c"),
        F.col("o.contract_attributes__c"),
        F.col("pi.sponsor_name__c").alias("sponsor"),
        F.col("ac.HQ_Account_Name__c").alias("sponsor_parent_company_name"),
        F.col("pi.project_status__c"),
        F.col("pi.project_start_date__c"),
        F.col("pi.project_end_date__c"),
        F.row_number().over(windowSpec).alias("rn")
    ).where(F.col("rn") == 1).drop("rn").distinct()

# display(work_bench_sf_shrink_dup)
work_bench_sf_shrink_dup.write.mode("overwrite").saveAsTable(f"{iep_catalogue_env}.synhdq_encur.snap_workbench_salesforce_details")
