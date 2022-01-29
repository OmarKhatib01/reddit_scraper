import requests
import pandas as pd
import datetime as dt

base_url = 'https://api.pushshift.io/reddit/search/'

# Pushshift parameters at link: https://github.com/pushshift/api

# define parameters here
data_type = 'comment'
subreddit = 'Conservative'
query = 'trump'
before = '1d'
after = '5d'
size = 400


def get_data(subreddit, query, befor, after, size=100, data_type='comment'):

    data = requests.get(f'{base_url}{data_type}/?q={query}&subreddit={subreddit}&before={before}&after={after}&size={size}')
    df = pd.json_normalize(data.json()['data'])
    df.head()
    df['datetime'] = df['created_utc'].map(lambda t: dt.datetime.fromtimestamp(t))
    filtered_df = df[['author', 'datetime', 'score', 'subreddit', 'body', 'permalink']]
    filtered_df.head()
    filtered_df.to_csv('comments.csv')

get_data(subreddit, query, before, after, size)