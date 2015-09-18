import sys, os, tweepy, time, json
from optparse import OptionParser
from slistener import SListener

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="filter for key words", metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    ta = Twitterlyzer(options.filename, 'sentiments.csv', args)


class Twitterlyzer(object):
    # Consumer keys and access tokens, used for OAuth
    consumer_key = '9IgePYjgkXvWBYjFBtu3DRg0X'
    consumer_secret = '8yArPE8GxBKhcwZcvL8Kw2MNfCRgSqDJfx7yiFyRyVAsrAj9zQ'
    access_token = '1670954952-e2DejjpVFzN5OPXvzltJ6cos0gseRZYfrekDhhM'
    access_token_secret = 'mP9CgwEWXc8ByiFZkXj1Pv36K2ofz9DngfMRLaMFio3BG'

    def __init__(self, tweet_file, sentiments_file, filter_string):
        if tweet_file:
            self.tweets = self.load_tweets(tweet_file)
        if sentiments_file:
            self.sentiments = self.load_sentiments(sentiments_file)
        if filter_string:
            self.stream = self.initialize_slistener(filter_string)
        else:
            print("Error: Please provide some arguments.")

    def initialize_slistener(self, filter_string):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        l = SListener(api, filterString[0])
        stream = tweepy.Stream(auth, l)
        stream.filter(track=filterString)

    def byteify(self, input):
        if isinstance(input, dict):
            return {self.byteify(key):self.byteify(value) for key,value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def extract_text(self, tweet):
        return tweet['text'].lower().split()

    def tweet_sentiment(self, tweet, sentiments):
        averageSentiment = False
        wordCount = 0
        keys = sentiments.keys()

        for word in tweet:
            if word in keys:
                averageSentiment += sentiments[word]
                wordCount += 1
        if wordCount == 0:
            return 0
        else:
            return averageSentiment / wordCount

    def generate_sentiment_list(self):
        tweetsSentiment = []

        for i in range(len(self.tweets)):
            tweetsSentiment.append(((self.tweets[i]['created_at'], self.tweet_sentiment(self.extract_text(self.tweets[i]), self.sentiments))))
        return tweetsSentiment
    
    def stream_sentiment(self, data):
        return tweet_sentiment(self.byteify(json.loads(line)), self.sentiments)

    def load_tweets(self, file_name=None):
        """Loads tweet from json file to python dictionary"""
        tweets = {}
        tweet_id = 0
        line_number = 0
        for line in open(file_name, 'r'):
            if line_number % 2 == 0:
                tweets[tweet_id] = self.byteify(json.loads(line))
                tweet_id += 1
            line_number += 1
        return tweets

    def load_sentiments(self, file_name):
        """Read the sentiment file and return a dictionary containing the sentiment
        score of each word, a value from -1 to +1.
        """
        sentiments = {}
        for line in open(file_name):
            word, score = line.split(',')
            sentiments[word] = float(score.strip())
        return sentiments

    def create_csv(self, tweet_list, filename):
        """Create CSV file from tweet list and average sentiments for each tweet"""
        csv_file = open(filename, 'w')
        for item in tweet_list:
            time, text = item
            csv_file.write(str(time) + ',' + str(text) + '\n')

if __name__ == '__main__':
    main()
