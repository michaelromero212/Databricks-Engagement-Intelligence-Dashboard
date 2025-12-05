# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest Engagements Data (Embedded)
# MAGIC This notebook contains sample data inline and creates a Delta table.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType
from pyspark.sql.functions import col, to_date

# Sample Data (Embedded)
raw_data = [
  {
    "id": "ENG-001",
    "customer": "MediaStream",
    "notes": "Successfully migrated to Terraform. Performance improved by 30%.",
    "feedback": "Excellent guidance on Terraform architecture.",
    "technologies": [
      "Terraform",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-11-12"
  },
  {
    "id": "ENG-002",
    "customer": "EduTech Solutions",
    "notes": "Team is struggling with MLflow adoption. Recommended training.",
    "feedback": "Implementation took longer than expected due to MLflow complexity.",
    "technologies": [
      "MLflow",
      "Databricks SQL",
      "Terraform",
      "Structured Streaming"
    ],
    "status": "at-risk",
    "date": "2025-10-06"
  },
  {
    "id": "ENG-003",
    "customer": "EduTech Solutions",
    "notes": "Customer faced issues with Terraform. Resolved by optimizing configuration.",
    "feedback": "Encountered some bugs with Terraform preview features.",
    "technologies": [
      "Terraform",
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-11-02"
  },
  {
    "id": "ENG-004",
    "customer": "FinTech Corp",
    "notes": "POC for Auto Loader was successful. Moving to production next week.",
    "feedback": "Excellent guidance on Auto Loader architecture.",
    "technologies": [
      "Auto Loader"
    ],
    "status": "completed",
    "date": "2025-09-19"
  },
  {
    "id": "ENG-005",
    "customer": "EduTech Solutions",
    "notes": "Optimized Unity Catalog jobs to reduce costs by 20%.",
    "feedback": "Would recommend Databricks for Unity Catalog workloads.",
    "technologies": [
      "Unity Catalog",
      "Delta Lake",
      "PySpark",
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-10-06"
  },
  {
    "id": "ENG-006",
    "customer": "FinTech Corp",
    "notes": "Customer requested best practices for PySpark scaling.",
    "feedback": "Encountered some bugs with PySpark preview features.",
    "technologies": [
      "PySpark",
      "Delta Lake",
      "Databricks SQL",
      "Auto Loader"
    ],
    "status": "in-progress",
    "date": "2025-09-08"
  },
  {
    "id": "ENG-007",
    "customer": "MediaStream",
    "notes": "POC for Structured Streaming was successful. Moving to production next week.",
    "feedback": "Encountered some bugs with Structured Streaming preview features.",
    "technologies": [
      "Structured Streaming",
      "Auto Loader",
      "PySpark"
    ],
    "status": "completed",
    "date": "2025-08-31"
  },
  {
    "id": "ENG-008",
    "customer": "CyberSecure",
    "notes": "Governance review highlighted gaps in Auto Loader implementation.",
    "feedback": "Impressed with the performance of Auto Loader.",
    "technologies": [
      "Auto Loader"
    ],
    "status": "completed",
    "date": "2025-09-08"
  },
  {
    "id": "ENG-009",
    "customer": "RetailGiant",
    "notes": "Customer requested best practices for Auto Loader scaling.",
    "feedback": "Great experience, but Auto Loader documentation could be better.",
    "technologies": [
      "Auto Loader",
      "MLflow",
      "Delta Lake",
      "Serverless"
    ],
    "status": "planned",
    "date": "2025-10-25"
  },
  {
    "id": "ENG-010",
    "customer": "HealthPlus",
    "notes": "Implemented PySpark for real-time analytics dashboard.",
    "feedback": "Implementation took longer than expected due to PySpark complexity.",
    "technologies": [
      "PySpark",
      "Databricks SQL",
      "Serverless"
    ],
    "status": "in-progress",
    "date": "2025-11-01"
  },
  {
    "id": "ENG-011",
    "customer": "GreenEnergy",
    "notes": "POC for Unity Catalog was successful. Moving to production next week.",
    "feedback": "Great experience, but Unity Catalog documentation could be better.",
    "technologies": [
      "Unity Catalog"
    ],
    "status": "at-risk",
    "date": "2025-10-22"
  },
  {
    "id": "ENG-012",
    "customer": "GreenEnergy",
    "notes": "Implemented Structured Streaming for real-time analytics dashboard.",
    "feedback": "Excellent guidance on Structured Streaming architecture.",
    "technologies": [
      "Structured Streaming",
      "Delta Lake"
    ],
    "status": "planned",
    "date": "2025-09-10"
  },
  {
    "id": "ENG-013",
    "customer": "HealthPlus",
    "notes": "Governance review highlighted gaps in Auto Loader implementation.",
    "feedback": "Would recommend Databricks for Auto Loader workloads.",
    "technologies": [
      "Auto Loader"
    ],
    "status": "in-progress",
    "date": "2025-09-04"
  },
  {
    "id": "ENG-014",
    "customer": "DataDriven Co",
    "notes": "Successfully migrated to PySpark. Performance improved by 30%.",
    "feedback": "Implementation took longer than expected due to PySpark complexity.",
    "technologies": [
      "PySpark",
      "Unity Catalog",
      "Databricks SQL",
      "Structured Streaming"
    ],
    "status": "completed",
    "date": "2025-11-14"
  },
  {
    "id": "ENG-015",
    "customer": "Global Logistics",
    "notes": "Implemented Serverless for real-time analytics dashboard.",
    "feedback": "Would recommend Databricks for Serverless workloads.",
    "technologies": [
      "Serverless",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-09-20"
  },
  {
    "id": "ENG-016",
    "customer": "RetailGiant",
    "notes": "Team is struggling with PySpark adoption. Recommended training.",
    "feedback": "Impressed with the performance of PySpark.",
    "technologies": [
      "PySpark",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-09-21"
  },
  {
    "id": "ENG-017",
    "customer": "MediaStream",
    "notes": "Debugging Unity Catalog errors took significant time. Root cause was network configuration.",
    "feedback": "Smooth transition to Unity Catalog.",
    "technologies": [
      "Unity Catalog"
    ],
    "status": "completed",
    "date": "2025-11-19"
  },
  {
    "id": "ENG-018",
    "customer": "RetailGiant",
    "notes": "Customer faced issues with Structured Streaming. Resolved by optimizing configuration.",
    "feedback": "Encountered some bugs with Structured Streaming preview features.",
    "technologies": [
      "Structured Streaming",
      "Unity Catalog",
      "Auto Loader",
      "Terraform"
    ],
    "status": "in-progress",
    "date": "2025-10-12"
  },
  {
    "id": "ENG-019",
    "customer": "Global Logistics",
    "notes": "Governance review highlighted gaps in Unity Catalog implementation.",
    "feedback": "Implementation took longer than expected due to Unity Catalog complexity.",
    "technologies": [
      "Unity Catalog"
    ],
    "status": "in-progress",
    "date": "2025-10-05"
  },
  {
    "id": "ENG-020",
    "customer": "EduTech Solutions",
    "notes": "Debugging MLflow errors took significant time. Root cause was network configuration.",
    "feedback": "The team was very helpful in resolving our MLflow issues.",
    "technologies": [
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-10-12"
  },
  {
    "id": "ENG-021",
    "customer": "RetailGiant",
    "notes": "Implemented Databricks SQL for real-time analytics dashboard.",
    "feedback": "Implementation took longer than expected due to Databricks SQL complexity.",
    "technologies": [
      "Databricks SQL",
      "PySpark",
      "Terraform",
      "Auto Loader"
    ],
    "status": "in-progress",
    "date": "2025-11-18"
  },
  {
    "id": "ENG-022",
    "customer": "GreenEnergy",
    "notes": "Governance review highlighted gaps in MLflow implementation.",
    "feedback": "Looking forward to expanding MLflow usage.",
    "technologies": [
      "MLflow",
      "Delta Lake",
      "Structured Streaming"
    ],
    "status": "completed",
    "date": "2025-09-10"
  },
  {
    "id": "ENG-023",
    "customer": "Global Logistics",
    "notes": "Customer requested best practices for Unity Catalog scaling.",
    "feedback": "Encountered some bugs with Unity Catalog preview features.",
    "technologies": [
      "Unity Catalog",
      "Delta Lake",
      "Databricks SQL"
    ],
    "status": "in-progress",
    "date": "2025-11-03"
  },
  {
    "id": "ENG-024",
    "customer": "FinTech Corp",
    "notes": "Team is struggling with Auto Loader adoption. Recommended training.",
    "feedback": "Great experience, but Auto Loader documentation could be better.",
    "technologies": [
      "Auto Loader"
    ],
    "status": "completed",
    "date": "2025-11-15"
  },
  {
    "id": "ENG-025",
    "customer": "MediaStream",
    "notes": "Team is struggling with PySpark adoption. Recommended training.",
    "feedback": "Encountered some bugs with PySpark preview features.",
    "technologies": [
      "PySpark",
      "Photon",
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-09-05"
  },
  {
    "id": "ENG-026",
    "customer": "HealthPlus",
    "notes": "Governance review highlighted gaps in Auto Loader implementation.",
    "feedback": "Great experience, but Auto Loader documentation could be better.",
    "technologies": [
      "Auto Loader",
      "Photon",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-11-17"
  },
  {
    "id": "ENG-027",
    "customer": "MediaStream",
    "notes": "Customer requested best practices for Unity Catalog scaling.",
    "feedback": "Would recommend Databricks for Unity Catalog workloads.",
    "technologies": [
      "Unity Catalog",
      "Auto Loader",
      "Serverless"
    ],
    "status": "at-risk",
    "date": "2025-09-08"
  },
  {
    "id": "ENG-028",
    "customer": "DataDriven Co",
    "notes": "Team is struggling with PySpark adoption. Recommended training.",
    "feedback": "The team was very helpful in resolving our PySpark issues.",
    "technologies": [
      "PySpark",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-10-30"
  },
  {
    "id": "ENG-029",
    "customer": "FinTech Corp",
    "notes": "Optimized Photon jobs to reduce costs by 20%.",
    "feedback": "Excellent guidance on Photon architecture.",
    "technologies": [
      "Photon",
      "Serverless",
      "Unity Catalog",
      "Databricks SQL"
    ],
    "status": "planned",
    "date": "2025-09-27"
  },
  {
    "id": "ENG-030",
    "customer": "GreenEnergy",
    "notes": "Team is struggling with Delta Lake adoption. Recommended training.",
    "feedback": "The team was very helpful in resolving our Delta Lake issues.",
    "technologies": [
      "Delta Lake",
      "MLflow"
    ],
    "status": "at-risk",
    "date": "2025-10-06"
  },
  {
    "id": "ENG-031",
    "customer": "FinTech Corp",
    "notes": "Governance review highlighted gaps in Photon implementation.",
    "feedback": "Would recommend Databricks for Photon workloads.",
    "technologies": [
      "Photon",
      "Auto Loader"
    ],
    "status": "completed",
    "date": "2025-10-28"
  },
  {
    "id": "ENG-032",
    "customer": "FinTech Corp",
    "notes": "Debugging Unity Catalog errors took significant time. Root cause was network configuration.",
    "feedback": "Looking forward to expanding Unity Catalog usage.",
    "technologies": [
      "Unity Catalog",
      "PySpark",
      "Serverless"
    ],
    "status": "completed",
    "date": "2025-10-28"
  },
  {
    "id": "ENG-033",
    "customer": "AutoMotive Inc",
    "notes": "Governance review highlighted gaps in Serverless implementation.",
    "feedback": "Impressed with the performance of Serverless.",
    "technologies": [
      "Serverless",
      "PySpark",
      "Photon"
    ],
    "status": "in-progress",
    "date": "2025-10-05"
  },
  {
    "id": "ENG-034",
    "customer": "RetailGiant",
    "notes": "Governance review highlighted gaps in Terraform implementation.",
    "feedback": "Impressed with the performance of Terraform.",
    "technologies": [
      "Terraform",
      "Structured Streaming",
      "Databricks SQL"
    ],
    "status": "completed",
    "date": "2025-10-07"
  },
  {
    "id": "ENG-035",
    "customer": "AutoMotive Inc",
    "notes": "Customer faced issues with Delta Lake. Resolved by optimizing configuration.",
    "feedback": "Smooth transition to Delta Lake.",
    "technologies": [
      "Delta Lake",
      "Databricks SQL",
      "Auto Loader",
      "Photon"
    ],
    "status": "completed",
    "date": "2025-10-23"
  },
  {
    "id": "ENG-036",
    "customer": "GreenEnergy",
    "notes": "Customer faced issues with MLflow. Resolved by optimizing configuration.",
    "feedback": "Smooth transition to MLflow.",
    "technologies": [
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-11-19"
  },
  {
    "id": "ENG-037",
    "customer": "Global Logistics",
    "notes": "Successfully migrated to Terraform. Performance improved by 30%.",
    "feedback": "Smooth transition to Terraform.",
    "technologies": [
      "Terraform",
      "MLflow"
    ],
    "status": "completed",
    "date": "2025-10-06"
  },
  {
    "id": "ENG-038",
    "customer": "AutoMotive Inc",
    "notes": "Successfully migrated to Delta Lake. Performance improved by 30%.",
    "feedback": "Would recommend Databricks for Delta Lake workloads.",
    "technologies": [
      "Delta Lake",
      "Serverless"
    ],
    "status": "completed",
    "date": "2025-11-20"
  },
  {
    "id": "ENG-039",
    "customer": "GreenEnergy",
    "notes": "POC for Databricks SQL was successful. Moving to production next week.",
    "feedback": "Would recommend Databricks for Databricks SQL workloads.",
    "technologies": [
      "Databricks SQL",
      "Photon"
    ],
    "status": "in-progress",
    "date": "2025-11-12"
  },
  {
    "id": "ENG-040",
    "customer": "Global Logistics",
    "notes": "POC for Auto Loader was successful. Moving to production next week.",
    "feedback": "Looking forward to expanding Auto Loader usage.",
    "technologies": [
      "Auto Loader",
      "Structured Streaming",
      "Serverless",
      "Terraform"
    ],
    "status": "completed",
    "date": "2025-11-23"
  },
  {
    "id": "ENG-041",
    "customer": "AutoMotive Inc",
    "notes": "POC for MLflow was successful. Moving to production next week.",
    "feedback": "Encountered some bugs with MLflow preview features.",
    "technologies": [
      "MLflow",
      "Photon",
      "Serverless",
      "Terraform"
    ],
    "status": "in-progress",
    "date": "2025-09-22"
  },
  {
    "id": "ENG-042",
    "customer": "EduTech Solutions",
    "notes": "Initial setup of MLflow was challenging due to legacy data formats.",
    "feedback": "Smooth transition to MLflow.",
    "technologies": [
      "MLflow",
      "PySpark"
    ],
    "status": "completed",
    "date": "2025-11-13"
  },
  {
    "id": "ENG-043",
    "customer": "Global Logistics",
    "notes": "Customer faced issues with Serverless. Resolved by optimizing configuration.",
    "feedback": "Excellent guidance on Serverless architecture.",
    "technologies": [
      "Serverless",
      "PySpark",
      "Terraform",
      "Databricks SQL"
    ],
    "status": "completed",
    "date": "2025-09-14"
  },
  {
    "id": "ENG-044",
    "customer": "CyberSecure",
    "notes": "Customer faced issues with Structured Streaming. Resolved by optimizing configuration.",
    "feedback": "Encountered some bugs with Structured Streaming preview features.",
    "technologies": [
      "Structured Streaming"
    ],
    "status": "completed",
    "date": "2025-11-25"
  },
  {
    "id": "ENG-045",
    "customer": "FinTech Corp",
    "notes": "Customer faced issues with Databricks SQL. Resolved by optimizing configuration.",
    "feedback": "Smooth transition to Databricks SQL.",
    "technologies": [
      "Databricks SQL"
    ],
    "status": "at-risk",
    "date": "2025-10-27"
  },
  {
    "id": "ENG-046",
    "customer": "MediaStream",
    "notes": "Initial setup of PySpark was challenging due to legacy data formats.",
    "feedback": "The team was very helpful in resolving our PySpark issues.",
    "technologies": [
      "PySpark",
      "Photon"
    ],
    "status": "completed",
    "date": "2025-11-04"
  },
  {
    "id": "ENG-047",
    "customer": "CyberSecure",
    "notes": "Optimized Databricks SQL jobs to reduce costs by 20%.",
    "feedback": "Would recommend Databricks for Databricks SQL workloads.",
    "technologies": [
      "Databricks SQL",
      "PySpark",
      "Delta Lake",
      "Structured Streaming"
    ],
    "status": "completed",
    "date": "2025-11-02"
  },
  {
    "id": "ENG-048",
    "customer": "GreenEnergy",
    "notes": "POC for PySpark was successful. Moving to production next week.",
    "feedback": "Excellent guidance on PySpark architecture.",
    "technologies": [
      "PySpark",
      "Delta Lake"
    ],
    "status": "completed",
    "date": "2025-09-08"
  },
  {
    "id": "ENG-049",
    "customer": "MediaStream",
    "notes": "Implemented Structured Streaming for real-time analytics dashboard.",
    "feedback": "Encountered some bugs with Structured Streaming preview features.",
    "technologies": [
      "Structured Streaming",
      "Unity Catalog",
      "PySpark"
    ],
    "status": "planned",
    "date": "2025-09-26"
  },
  {
    "id": "ENG-050",
    "customer": "DataDriven Co",
    "notes": "Optimized Delta Lake jobs to reduce costs by 20%.",
    "feedback": "Implementation took longer than expected due to Delta Lake complexity.",
    "technologies": [
      "Delta Lake",
      "MLflow"
    ],
    "status": "in-progress",
    "date": "2025-09-03"
  }
]

# Define schema
schema = StructType([
    StructField("id", StringType(), True),
    StructField("customer", StringType(), True),
    StructField("notes", StringType(), True),
    StructField("feedback", StringType(), True),
    StructField("technologies", ArrayType(StringType()), True),
    StructField("status", StringType(), True),
    StructField("date", StringType(), True),
    StructField("sentiment", StructType([
        StructField("sentiment_type", StringType(), True),
        StructField("sentiment_score", FloatType(), True)
    ]), True),
    StructField("topic", StructType([
        StructField("topic", StringType(), True),
        StructField("confidence", FloatType(), True)
    ]), True)
])

# COMMAND ----------

# Create DataFrame
df = spark.createDataFrame(raw_data, schema=schema)
display(df)

# COMMAND ----------

# Create table
table_name = "engagements"
df_processed = df.withColumn("date", to_date(col("date")))
df_processed.write.format("delta").mode("overwrite").saveAsTable(table_name)

print(f"Successfully created table '{table_name}' with {len(raw_data)} records.")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM engagements;
