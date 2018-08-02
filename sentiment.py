# python 2D plotting library
import matplotlib.pyplot as plot
# handles authentication
from tweepy import OAuthHandler
# enables communication with twitter
import tweepy
# python natural language processing toolkit
from textblob import TextBlob
# import for regular expression
import re

class Sentiment(object):

    def __init__(self):
        # autehtication key,toekn,secret and token secret

        key = 'TLhSM4BjBroZiQn4OMRaDwLah'
        secret = 'Ylu4OxbVmUmxJdw7bxB2P8ug7TChpOV9alBahEnzulJhOhq6KC'
        token = '302678753-sdnAofMQxJIzWhbJ1LmcFR7DpmFKoVYjMDXGK6Bb'
        token_secret = '8uGTuPiqxWV2dRqkuaD3X60eoy074WgT8JjTI1aCRIqw6'


        try:
            # trying to establish a connection
            self.auth = OAuthHandler(key,secret)
            self.auth.set_access_token(token, token_secret)
            self.api = tweepy.API(self.auth)

        except:
            # print if connection is not established
            print("some error encountered check internet connection and try again")




    def get_tweets(self, query, count=100):
        #stores tweets after analysis
        twitter_tweets = []

        try:
            gather_tweets = self.api.search(q=query, count=count)

            for tweet in gather_tweets:
                store_tweet = {}

                store_tweet['text'] = tweet.text
                store_tweet['sentiment'] = self.analyse(tweet.text)

                if tweet.retweet_count > 0:
                    if store_tweet not in twitter_tweets:
                        twitter_tweets.append(store_tweet)
                else:
                    twitter_tweets.append(store_tweet)


            return twitter_tweets

        except tweepy.TweepError as error:
            print("something is wrong" + str(error))



    def remove_specialcharacters(self, tweet_text):
        # remove special character from tweets
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w +:\ / \ / \S +)", " ", tweet_text).split())



    def analyse(self, tweet_sentiment):

        tweet_analysis = TextBlob(self.remove_specialcharacters(tweet_sentiment))
        if tweet_analysis.sentiment.polarity > 0:
            return 'positive'
        elif tweet_analysis.sentiment.polarity < 0:
            return 'negative'


def main():
    class_object = Sentiment()
    tweets = class_object.get_tweets(query='bitcoin', count=100)

    negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

    positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']


    print("\n\n POSITIVE TWEETS\n\n\n")
    for twitter_tweet in positive_tweets[:10]:
        # print positive tweets
        print("\n",twitter_tweet['text'])

    print("\n\n NEGATIVE TWEETS \n\n\n ")
    for twitter_tweet in negative_tweets[:10]:
        # print negative tweets
        print("\n",twitter_tweet['text'])


    # color for each portion on pie chart
    colors = ['g', 'r']
    label = ['positive tweets','negative tweets']
    # portion on pie chart
    portion = [len(positive_tweets),len(negative_tweets)]


    # plotting the pie chart
    plot.pie(portion, labels=label, colors=colors,
            startangle=90, shadow=True,
            radius=1.2, autopct='%1.1f%%')

    plot.legend()
    plot.show()






if __name__ == "__main__":
    #  main function call
    main()
