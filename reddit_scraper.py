# import requests
# import pandas as pd
#
# query="seo" #Define Your Query
# url = f"https://api.pushshift.io/reddit/search/comment/?q={query}"
# request = requests.get(url)
# json_response = request.json()
# json_response
#
#
# def get_pushshift_data(data_type, **kwargs):
#     """
#     Gets data from the pushshift api.
#
#     data_type can be 'comment' or 'submission'
#     The rest of the args are interpreted as payload.
#
#     Read more: https://github.com/pushshift/api
#     """
#
#     base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"
#     payload = kwargs
#     request = requests.get(base_url, params=payload)
#     return request.json()
#
# data_type="comment"         # give me comments, use "submission" to publish something
# query="liberal"             # Add your query
# before="30d"
# after ="105d"
# size=1                   # maximum 1000 comments
# sort_type="score"           # Sort by score (Accepted: "score", "num_comments", "created_utc")
# sort="desc"                 # sort descending
# subreddit="Conservative"    #"author", "link_id", "created_utc", "subreddit"
#
# data = get_pushshift_data(data_type=data_type,
#                           q=query,
#
#                           size=size,
#                           )
# print(data)
# df = pd.DataFrame.from_records(data)[0:10]
#
# print(df)


from psaw import PushshiftAPI  # library Pushshift
import datetime as dt  # library for date management
import p  # library for data manipulation
import pandas as pd

api = PushshiftAPI()  # Object of the API

# """FOR POSTS"""
# def data_prep_posts(subreddit, start_time, end_time, filters, limit):
#     if(len(filters) == 0):
#         filters = ['id', 'author', 'created_utc',
#                    'domain', 'url',
#                    'title', 'num_comments']
#                    #We set by default some useful columns
#
#     posts = list(api.search_submissions(
#         subreddit=subreddit,   #Subreddit we want to audit
#         after=start_time,      #Start date
#         before=end_time,       #End date
#         filter=filters,        #Column names we want to retrieve
#         limit=limit))          ##Max number of posts
#
#     return pd.DataFrame(posts) #Return dataframe for analysis


"""FOR COMMENTS"""


# def data_prep_comments(term, subreddit, start_time, end_time, filters, size):
#     if (len(filters) == 0):
#         filters = ['id', 'author', 'created_utc',
#                    'body', 'score', 'permalink', 'subreddit']
#         # We set by default some usefull columns
#
#     comments = list(api.search_comments(
#         q=term,  # term to look for
#         subreddit=subreddit,  # Subreddit we want to audit
#         after=start_time,  # Start date
#         before=end_time,  # End date
#         filter=filters,  # Column names we want to retrieve
#         size=size))  # Max number of comments
#     print(comments)
#     return pd.DataFrame(comments)  # Return dataframe for analysis
#
#
# def main():
#     term = 'liberal'  # Term we want to search for
#     subreddit = "Conservative"  # Subreddit we are auditing
#     start_time = int(dt.datetime(2021, 1, 1).timestamp())
#     # Starting date for our search
#     end_time = int(dt.datetime(2021, 1, 31).timestamp())
#     # Ending date for our search
#     # filters = ['author', 'body', 'score', 'created_utc', 'subreddit', 'url']  # We don´t want specific filters
#     filters = []
#     size = 10  # Elelemts we want to recieve
#
#     # """Here we are going to get subreddits for a brief analysis"""
#     # #Call function for dataframe creation of comments
#     # df_p = data_prep_posts(subreddit,start_time,
#     #                      end_time,filters,limit)
#     #
#     # #Drop the column on timestamp format
#     # df_p['datetime'] = df_p['created_utc'].map(
#     #     lambda t: dt.datetime.fromtimestamp(t))
#     # df_p = df_p.drop('created_utc', axis=1)
#     # #Sort the Row by datetime
#     # df_p = df_p.sort_values(by='datetime')
#     # #Convert timestamp format to datetime for data analysis
#     # df_p["datetime"] = pd.to_datetime(df_p["datetime"])
#     """Here we are going to get comments for a brief analysis"""
#
#     df_c = data_prep_comments(term, subreddit, start_time,
#                               end_time, filters, size)
#                             # Call function for dataframe creation of comments
#     print(df_c)
#     df_c.to_csv()
#
# main()



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


def get_data(sub, q, b4, aftr, num, datatype='comment'):

    data = requests.get(f'{base_url}{datatype}/?q={q}&subreddit={sub}&before={b4}&after={aftr}&size={num}')
    df = pd.json_normalize(data.json()['data'])
    df.head()
    df['datetime'] = df['created_utc'].map(lambda t: dt.datetime.fromtimestamp(t))
    filtered_df = df[['author', 'datetime', 'score', 'subreddit', 'body', 'permalink']]
    filtered_df.head()
    filtered_df.to_csv('comments.csv')

get_data(subreddit, query, before, after, size)