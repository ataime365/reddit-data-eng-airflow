from utils.constants import SECRET, CLIENT_ID, OUTPUT_PATH
from etls.reddit_etl import connect_reddit, extract_posts, transform_data, load_data_to_csv
import pandas as pd


def reddit_pipeline(file_name:str, subreddit:str, time_filter='day', limit=None):
    """Main function: We will be returning a particular instance of reddit"""
    
    # connecting to reddit instance
    instance = connect_reddit(CLIENT_ID, SECRET, 'Ataime Agent')
    
    #extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    #transformation
    post_df = transform_data(post_df)
    # loading to csv
    # file_path = f"{OUTPUT_PATH}/{file_name}.csv"
    file_path = f"{OUTPUT_PATH}/{file_name}.parquet"
    load_data_to_csv(post_df, file_path)
    
    return file_path
    
    