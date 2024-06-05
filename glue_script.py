import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import concat_ws
from awsglue import DynamicFrame

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1717512076121 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ","}, connection_type="s3", format="csv", connection_options={"paths": ["s3://reddit-data-ben/raw/reddit_20240604.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1717512076121")

#convert DynamicFrame to Dataframe
df = AmazonS3_node1717512076121.toDF()

#concatenate the three columns into a single column
df_combined = df.withColumn('ESS_updated', concat_ws('-', df['edited'], df['spoiler'], df['stickied']))
df_combined = df_combined.drop('edited', 'spoiler', 'stickied')

#convert back to DynamicFrame
S3bucket_node_combined = DynamicFrame.fromDF(df_combined, glueContext, 'S3bucket_node_combined')

# Script generated for node Amazon S3
AmazonS3_node1717512080545 = glueContext.write_dynamic_frame.from_options(frame=S3bucket_node_combined, connection_type="s3", format="csv", connection_options={"path": "s3://reddit-data-ben/transformed/", "partitionKeys": []}, transformation_ctx="AmazonS3_node1717512080545")

job.commit()