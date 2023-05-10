

import tweepy
import regex as re
from textblob import TextBlob
import config
from flask import Flask, render_template, request
import os
print(os.getcwd())


# Twitter API credentials
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_secret

# Set up Twitter API authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Flask app setup
app = Flask(__name__, template_folder='templates')

# Home route
@app.route('/')
def home():
    return render_template('home4.html')

# Search route
@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    tweets = tweepy.Cursor(api.search_tweets, q = query ,lang="en", tweet_mode='extended').items(25)
    # Perform sentiment analysis on each tweet
    tweet_sentiments = []
    subject_sentiment = []
    for tweet in tweets:
        text =  tweet.full_text
        text = cleanTweets(text)
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        tweet_sentiments.append((text, sentiment))
        subject_sentiment.append((sentiment, subjectivity))

    positive_tweets = [s for s in tweet_sentiments if s[1] > 0]
    negative_tweets = [s for s in tweet_sentiments if s[1] < 0]
    neutral_tweets = [s for s in tweet_sentiments if s[1] == 0]
    
    positive_percentage = len(positive_tweets) / len(tweet_sentiments) * 100
    negative_percentage = len(negative_tweets) / len(tweet_sentiments) * 100     
    neutral_percentage = len(neutral_tweets) / len(tweet_sentiments) * 100 
        
    
    return render_template('search1.html', tweets=tweets, 
                           query=query, subject_sentiment=subject_sentiment,
                           tweet_sentiments=tweet_sentiments, 
                           positive_percentage=positive_percentage, 
                           negative_percentage=negative_percentage,
                           neutral_percentage=neutral_percentage)

#clean the tweets with a function
def cleanTweets(text):
    text = re.sub('@[A-Za-z0-9_]+', '', text) #removes @mentions
    text = re.sub('#','',text) #removes hastag '#' symbol
    text = re.sub('RT[\s]+','',text)
    text = re.sub('https?:\/\/\S+', '', text) 
    text = re.sub('\n',' ',text)
    return text

    
    
if __name__ == '__main__':
    app.run()
    