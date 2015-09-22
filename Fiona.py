import json, time, sys, os
import tweepy

class Fiona(tweepy.StreamListener):

    def __init__(self, options, args):


        self.counter = 0
        if options.filename:
            self.fprefix = options.filename
            self.output  = open(self.fprefix + '.' 
                         + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.delout  = open('delete.txt', 'a')

        if options.tweets and options.sentiments and options.output:
            self.tweets = self.load_tweets(options.tweets)
            self.sentiments = self.load_sentiments(options.sentiments)
            self.output = options.output
            self.create_csv(self.generate_sentiment_list())
        else:
            print("Please provide a option or argument(s) to run the application, see -h --help.")

    def on_data(self, data):
        self.print_data(data)


        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        self.output.write(status + "\n")

        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../streaming_data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return

    def print_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return

#################################################################
# From main.py                                                  #
#################################################################

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
        tweets_sentiment = []

        for i in range(len(self.tweets)):
            tweets_sentiment.append(((self.tweets[i]['created_at'],
                    self.tweet_sentiment(self.extract_text(self.tweets[i]), self.sentiments))))
        return tweets_sentiment
    
#   def stream_sentiment(self, data):
#      return tweet_sentiment(self.byteify(json.loads(line)), self.sentiments)

    def load_tweets(self, file_name=None):

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
