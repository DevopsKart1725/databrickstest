# Databricks notebook source
catalogue_env = dbutils.widgets.get("adb_catalogue_env")
secret = dbutils.widgets.get("secret")
url = dbutils.widgets.get("url")

# COMMAND ----------

cdm_jdbcDatabase = "cdm"
sbi_jdbcDatabase = "sbi_presentation"
jdbcUsername="token"
jdbcPassword=secret # replace your token
jdbcUrl = url

# COMMAND ----------

cdm_project_mapping = spark.read.jdbc(jdbcUrl, cdm_jdbcDatabase+".project_mapping",properties={"driver":"com.simba.spark.jdbc.Driver","user": jdbcUsername,"password": jdbcPassword})

# sbi_child_source_mapping = spark.read.jdbc(jdbcUrl, sbi_jdbcDatabase+".child_source_mapping",properties={"driver":"com.simba.spark.jdbc.Driver","user": jdbcUsername,"password": jdbcPassword})

# COMMAND ----------

cdm_project_mapping.write.mode("overwrite").saveAsTable(catalogue_env+".synhdq_work.cdm_project_mapping")
# sbi_child_source_mapping.write.mode("overwrite").saveAsTable(catalogue_env+".synhdq_work.sbi_child_source_mapping")
