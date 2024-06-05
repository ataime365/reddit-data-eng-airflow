
## Reddit data Enginnering End-to-End Data Engineering/ETL project on AWS.
(Reddit API, Airflow, Redis, Postgres, Docker, Spark, Python, AWS S3, Glue, Redshift Serverless, Athena)

This project makes use of DAG's in our Airlow to extract data from Reddit API. The Airflow depends on redis and Postgres and runs on docker. S3, Glue, Redshift and Athena are also used

The Aim of this project is to build an ELT pipeline using Reddit data, Airflow and docker and save the data to an S3 bucket in AWS. We then transform the data by merging some columns and dropping some columns we don't need/
We used Glue crawler to crawl the S3 bucket and make the data available in Glue Data Catalog tables and then made the data available to Redshift data warehouse using external schema(Redshift spectrum), to enable the data to be easily visaulized by end users or Data Analyst using PowerBI or any other BI tool




The tools used includes:
1. AirFlow for Orchestration/Automation (Airflow depended on postgres and Redis)
2. Spark for transforming the data
3. AWS S3 for storage
4. Glue Crawler for crawling the S3 bucket and making the data available in Glue Data Catalog tables
5. Amazon Redshift Serverless for data warehouse
6. Athena for querying the data from the Data catalog
7. Docker compose was used to manage different containers (Postgres, redis, Airflow)