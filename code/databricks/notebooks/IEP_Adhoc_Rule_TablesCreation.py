# Databricks notebook source
dbutils.widgets.text("adb_catalogue_env","")

# COMMAND ----------

import datetime
from pyspark.sql.functions import col,lit

catalogue_env=dbutils.widgets.get("adb_catalogue_env")

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
folders_rule_attribute_df = dbutils.fs.ls("/Volumes/"+catalogue_env+"/synhdq_raw/synhdq_raw/raw_data/EDQ.IEP_RULE_ATTRIBUTE_RAW/"+date_str)
folders_RuleModelMapping_df = dbutils.fs.ls("/Volumes/"+catalogue_env+"/synhdq_raw/synhdq_raw/raw_data/EDQ.IEP_RULE_MODEL_MAPPING_RAW/"+date_str)
# Sort the list of folders by their modification time in descending order
sorted_folders_rule_attribute = sorted(folders_rule_attribute_df, key=lambda x: x.modificationTime, reverse=True)
sorted_folders_RuleModelMapping = sorted(folders_RuleModelMapping_df, key=lambda x: x.modificationTime, reverse=True)
# Get the latest folder
latest_folder_rule_attribute = sorted_folders_rule_attribute[0]
latest_folder_RuleModelMapping = sorted_folders_RuleModelMapping[0]
# Extract the path of the latest folder
latest_folder_path_rule_attribute = latest_folder_rule_attribute.path
latest_folder_path_RuleModelMapping = latest_folder_RuleModelMapping.path
# Print the path of the latest folder
print(latest_folder_path_rule_attribute)
print(latest_folder_path_RuleModelMapping)

# COMMAND ----------

# Reading rule_attribute file 
rule_attribute_df=spark.read.format("parquet").option("inferSchema",True).option("header",True).load(latest_folder_path_rule_attribute)
# Reading RuleModelMapping file 
RuleModelMapping_df=spark.read.format("parquet").option("inferSchema",True).option("header",True).load(latest_folder_path_RuleModelMapping)


# COMMAND ----------

spark.sql(f"USE CATALOG {catalogue_env}")
spark.sql("use schema synhdq_encur")
spark.sql("drop table if exists iep_rule_attribute")
rule_attribute_df.write.saveAsTable("iep_rule_attribute")
spark.sql("drop table if exists iep_rule_model_mapping")
RuleModelMapping_df.write.saveAsTable("iep_rule_model_mapping")
