from praw import Reddit
import praw
import sys
from utils.constants import POST_FIELDS
import pandas as pd
import numpy as np

def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent
                             )
        print("connected to reddit")
        return reddit
    except Exception as e:
        print(e)
        sys.exit(1)
        
        
def extract_posts(reddit_instance:Reddit, subreddit:str, time_filter:str, limit:None):
    subreddit = reddit_instance.subreddit(subreddit)
    posts = subreddit.top(time_filter=time_filter, limit=limit)
    
    post_lists = []
    
    for post in posts:
        post_dict = vars(post) # __dict__  # vars([object]) -> dictionary
        # dictionary comprehension and dictionary #filtering
        post = {key: post_dict[key] for key in POST_FIELDS} # key: value 
        post_lists.append(post)     
        
    return post_lists


def transform_data(post_df: pd.DataFrame):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s') #input is in seconds
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode() #The mode is the value that appears most often
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]), post_df['edited'], edited_mode).astype(bool) #astype is used to covert the data tyoe to boolean
    # np.where(condition, x, y) i.e if post_df['edited'] value is in list True or False, pick post_df['edited'] else pick edited_mode
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    # post_df['upvote_ratio'] = post_df['upvote_ratio'].astype(int) #astype is used to convert the data type
    # post_df['selftext'] = post_df['selftext'].astype(str)
    post_df['title'] = post_df['title'].astype(str)
    return post_df
    
    
def load_data_to_csv(data: pd.DataFrame, path: str):
    """I changed it to parquet, instead of csv. 
    Parquet works better"""
    
    # data.to_csv(path, index=False)
    data.to_parquet(path, engine='pyarrow', index=False) #next time
    # data.to_parquet('output_file.parquet', engine='pyarrow') #next time
    
    
    