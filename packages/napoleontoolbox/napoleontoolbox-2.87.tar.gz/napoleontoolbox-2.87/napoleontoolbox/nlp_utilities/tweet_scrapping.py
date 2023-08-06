import GetOldTweets3 as got
import pandas as pd

# Function that pulls tweets based on a specific user and turns to dataframe
# Parameters: (username you want to get tweets from), (max number of most recent tweets to pull from)
def username_tweets_to_df(username='', count=100):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username) \
        .setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(user_tweets, columns=['Datetime', 'Text'])

    return tweets_df


# Function that pulls tweets based on a general search query and turns to dataframe
# Parameters: (text query you want to search), (max number of most recent tweets to pull from)
def text_query_to_df(text_query='', count=100):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(text_query) \
        .setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    text_tweets = [[tweet.date, tweet.text] for tweet in tweets]

    # Creation of dataframe from tweets
    tweets_df = pd.DataFrame(text_tweets, columns=['Datetime', 'Text'])


    return tweets_df