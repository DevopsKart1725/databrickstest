
# Databricks notebook source
# MAGIC %md #Common Configurations
# COMMAND ----------


clientid = dbutils.widgets.get("paramclientid")
clientsecret = dbutils.widgets.get("paramclientsecret")
endpoint = dbutils.widgets.get("paramendpoint")

# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": clientid,
           "fs.azure.account.oauth2.client.secret": clientsecret,
           "fs.azure.account.oauth2.client.endpoint": endpoint}


# COMMAND ----------

# MAGIC %md #Mounting Raw Container

# COMMAND ----------

# Define the variables used for creating connection strings
adlsAccountName = "iepdlz01devraw"
adlsContainerName = dbutils.widgets.get("paramadlsContainerName")
mountPoint = "/mnt/raw_layer"
 
source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/"
 
# Mount ADLS Storage to DBFS only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)
    

# COMMAND ----------

# MAGIC %md #Mounting Work Container

# COMMAND ----------

# Define the variables used for creating connection strings
adlsAccountName = "iepdlz01devwork"
adlsContainerName = "demodp"
mountPoint = "/mnt/work_layer"

source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" 
# Mount ADLS Storage to DBFS only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)

# COMMAND ----------

# MAGIC %md #Mounting Curated Container

# COMMAND ----------

# Define the variables used for creating connection strings
adlsAccountName = "iepdlz01devencur"
adlsContainerName = "demodp"
mountPoint = "/mnt/curated_layer"
 
source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" 
# Mount ADLS Storage to DBFS only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)