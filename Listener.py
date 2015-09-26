import json, time, sys, os
import tweepy

class Listener(tweepy.StreamListener):

    consumer_key = '9IgePYjgkXvWBYjFBtu3DRg0X'
    consumer_secret = '8yArPE8GxBKhcwZcvL8Kw2MNfCRgSqDJfx7yiFyRyVAsrAj9zQ'
    access_token = '1670954952-e2DejjpVFzN5OPXvzltJ6cos0gseRZYfrekDhhM'
    access_token_secret = 'mP9CgwEWXc8ByiFZkXj1Pv36K2ofz9DngfMRLaMFio3BG'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth, retry_count=3, retry_delay=10, timeout=240)

    def __init__(self, options):

        self.counter = 0
        if options.streamFile:
            self.fprefix = options.streamFile
        else:
            self.fprefix = "streamoutput"

        self.output  = open(self.fprefix + '.' 
                         + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')

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
