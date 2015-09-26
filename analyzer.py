import json

class Analyzer():

    def __init__(self, options, args):
        self.tweets = self.load_tweets(args[1])
        self.sentiments = self.load_sentiments(args[2])
        self.output_file = options.sentiments
        self.tweets_sentiment = self.generate_sentiment_list()

    ### Removes Unicode formatting from raw data. ###

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

    def load_tweets(self, file_name):

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

        sentiments = {}
        for line in open(file_name):
            word, score = line.split(',')
            sentiments[word] = float(score.strip())
        return sentiments

    def create_csv(self, tweet_list):

        csv_file = open(self.output, 'w')
        for item in tweet_list:
            time, text = item
            csv_file.write(str(time) + ',' + str(text) + '\n')

    def generate_sentiment_list(self):
        tweets_sentiment = []

        for i in range(len(self.tweets)):
            tweets_sentiment.append(((self.tweets[i]['created_at'],
                    self.tweet_sentiment(self.extract_text(self.tweets[i]), self.sentiments))))
        return tweets_sentiment

        ### PUBLIC METHODS ###
    def print_average_sentiment(self):
        sumVar = 0

        for (time, sentiment) in self.tweets_sentiment:
            sumVar += sentiment
        print(sumVar / len(self.tweets_sentiment))

    def print_duplicate_post_number(self):
        tweetList = []
        count = 0
        totalCount = 0

        for tweetId in self.tweets:
            tweetList.append(self.tweets[tweetId]['text'])

        for tweet in tweetList:
            count = tweetList.count(tweet)
            if count > 1:
                totalCount += 1
                print(tweet)

        print(totalCount)





