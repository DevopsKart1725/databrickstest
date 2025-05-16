# Databricks notebook source
cat = dbutils.widgets.get("cat")
# cat="dev"
print(cat)

# COMMAND ----------

# --Query Id = 57

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [0108] with non-active Site Status [Closed] has subject with Screening Number [203010806] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Query Id = 84

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [1702] with non-active Site Status [Closed] has subject with Screening Number [203170209] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Query id = 94

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [2103] with non-active Site Status [Closed] has subject with Screening Number [203210309] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Query id = 98

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [2206] with non-active Site Status [Closed] has subject with Screening Number [204220622] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Query id = 110

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In MCTMS, for Site Number [1510], COV information is present however there is no Site Status Change of Activated. (Site Management > Sites > Edit > History.)'
and key4 = 0036.00""")

# --Query id = 119

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In PDC, Project [1001897] has a Status of Cancelled or Closed. However, in CTMS for the same Project [1001897], Country [CHL], Site [0606] shows Subject Screening Number [203060609] has an Enrolled Date and/or Randomization Date of [24-Feb-2015]/[null] but has neither a Withdrawn Date or a Completed Date. A Project in a Terminal Status should not have an Active Subject. To resolve, contact the site to correct the missing entry for the Subject. If EDC is not integrated with CTMS, enter the missing Subject Event Date into CTMS.'
and key4 = 0564.10""")

# --Query id = 136

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In PDC, Project [1001897] has a Status of Cancelled or Closed. However, in CTMS for the same Project [1001897], Country [USA], Site [2329] shows Subject Screening Number [203232902] has an Enrolled Date and/or Randomization Date of [23-Sep-2014]/[null] but has neither a Withdrawn Date or a Completed Date. A Project in a Terminal Status should not have an Active Subject. To resolve, contact the site to correct the missing entry for the Subject. If EDC is not integrated with CTMS, enter the missing Subject Event Date into CTMS.'
and key4 = 0564.10""")

# --Query id = 187

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1003065 and key2 = 'CTMS'
and key3 = 'In CTMS, for Project [1003065], Country [United States], Site Number [206], Subject [206102] has an Informed Consent Date of [2016-11-29] and an Enrollment Date of [2015-08-03]. The Informed Consent Date is after the Enrollment Date. To resolve, contact the site to correct the incorrect entry for the Subject. If EDC is not integrated with CTMS, enter the correct subject event date into CTMS.'
and key4 = 0782.00""")

# --Query id = 190

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1003197 and key2 = 'CTMS'
and key3 = 'In CTMS, for Project [1003197], Country [United States], Site Number [217], Subject [042] has a Withdrawn Date [2014-12-09] but the Enrollment Date is blank. To resolve, contact the site to correct the missing entry for the Subject. If EDC is not integrated with CTMS, enter the correct subject event date into CTMS.'
and key4 = 0793.00""")

# --Query id= 212

spark.sql(f"""delete from iep_{cat}.synhdq_encur.snap_edq_query_details where key1 = 1003197 and key2 = 'CTMS'
and key3 = 'In MCTMS, for Site Number [217] at Activity Name [SMC], Recurrence [1], Visit Start Date [null], the Visit Start Date [null] should be valid, complete and not a future date. (Site Management > Site Visits > Edit. If the report is approved, contact the ServiceDesk for assistance.)'
and key4 = 0011.00""")

# COMMAND ----------

# --Update first record 57

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-06-03'  where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [0108] with non-active Site Status [Closed] has subject with Screening Number [203010806] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")


# --Second record 84

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-06-27' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [1702] with non-active Site Status [Closed] has subject with Screening Number [203170209] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Third record 94

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-05-20' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [2103] with non-active Site Status [Closed] has subject with Screening Number [203210309] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Fourth Record 98

spark.sql(f"""update  iep_{cat}.synhdq_work.edh_query_details set extract_date ='2024-05-14' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In CTMS, Site [2206] with non-active Site Status [Closed] has subject with Screening Number [204220622] showing as Standard Status [Enrolled]. To resolve, change the Site Status in CTMS or change the Subject Status in EDC. (Site Management > Sites > Edit >Standard Status)'
and key4 = 0562.00""")

# --Fifth Record 110

spark.sql(f"""Update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-05-06' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In MCTMS, for Site Number [1510], COV information is present however there is no Site Status Change of Activated. (Site Management > Sites > Edit > History.)'
and key4 = 0036.00""")

# --Sixth record 119

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-04-30' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In PDC, Project [1001897] has a Status of Cancelled or Closed. However, in CTMS for the same Project [1001897], Country [CHL], Site [0606] shows Subject Screening Number [203060609] has an Enrolled Date and/or Randomization Date of [24-Feb-2015]/[null] but has neither a Withdrawn Date or a Completed Date. A Project in a Terminal Status should not have an Active Subject. To resolve, contact the site to correct the missing entry for the Subject. If EDC is not integrated with CTMS, enter the missing Subject Event Date into CTMS.'
and key4 = 0564.10""")

# /--Seventh Record 136

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-04-23' where key1 = 1001897 and key2 = 'CTMS'
and key3 = 'In PDC, Project [1001897] has a Status of Cancelled or Closed. However, in CTMS for the same Project [1001897], Country [USA], Site [2329] shows Subject Screening Number [203232902] has an Enrolled Date and/or Randomization Date of [23-Sep-2014]/[null] but has neither a Withdrawn Date or a Completed Date. A Project in a Terminal Status should not have an Active Subject. To resolve, contact the site to correct the missing entry for the Subject. If EDC is not integrated with CTMS, enter the missing Subject Event Date into CTMS.'
and key4 = 0564.10""")

# --Tenth record 212

spark.sql(f"""update iep_{cat}.synhdq_work.edh_query_details set extract_date = '2024-04-01' where key1 = 1003197 and key2 = 'CTMS'
and key3 = 'In MCTMS, for Site Number [217] at Activity Name [SMC], Recurrence [1], Visit Start Date [null], the Visit Start Date [null] should be valid, complete and not a future date. (Site Management > Site Visits > Edit. If the report is approved, contact the ServiceDesk for assistance.)'
and key4 = 0011.00""")

# COMMAND ----------

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 10 where key2 = 'CTMS' and key4 = 0562.00""")

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 20 where key2 = 'CTMS' and key4 = 0036.00""")

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 30 where key2 = 'CTMS' and key4 = 0564.10""")

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 40 where key2 = 'CTMS' and key4 = 0782.00""")

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 50 where key2 = 'CTMS' and key4 = 0793.00""")

spark.sql(f"""update iep_{cat}.synhdq_work.edh_rules set priority = 60 where key2 = 'CTMS' and key4 = 0011.00""")
