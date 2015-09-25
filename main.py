import sys, os, tweepy, time, json
from optparse import OptionParser
from listener import Listener
from analyzer import Analyzer

os.chdir('data')

def main():
    # Input parser
    parser = OptionParser()
    parser.add_option("-f", "--outputfile", dest="filename",
                  help="filter for key words", metavar="FILE")
    parser.add_option("-t", "--tweets", dest="tweets",
                  help="tweets file", metavar="FILE")
    parser.add_option("-s", "--sentiments", dest="sentiments",
                  help="sentiments file", metavar="FILE")
    parser.add_option("-o", "--output", dest="output",
                  help="output file", metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()
    li = Listener(options, args)



    stream = tweepy.Stream(auth=li.auth, listener=li)
    stream.filter(track=args)

if __name__ == '__main__':
    main()
