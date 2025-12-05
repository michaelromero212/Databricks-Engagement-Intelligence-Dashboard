import json

# Read sample data
with open('backend/sample_data/engagements_sample.json') as f:
    data = json.load(f)[:50] # Take 50 records

# Create notebook content
notebook_content = f"""# Databricks notebook source
# MAGIC %md
# MAGIC # Ingest Engagements Data (Embedded)
# MAGIC This notebook contains sample data inline and creates a Delta table.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType
from pyspark.sql.functions import col, to_date

# Sample Data (Embedded)
raw_data = {json.dumps(data, indent=2)}

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

print(f"Successfully created table '{{table_name}}' with {{len(raw_data)}} records.")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM engagements;
"""

with open('notebooks/ingest_engagements.py', 'w') as f:
    f.write(notebook_content)

print("Generated notebooks/ingest_engagements.py with embedded data.")
