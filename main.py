import sys, os, tweepy, time, json
from optparse import OptionParser
from listener import Listener
from analyzer import Analyzer

#os.chdir('data')

def main():
    # Input parser
    parser = OptionParser()

    parser.add_option("-f", "--stream_file", dest="streamFile",
                  help="Name for the output file of a twitter stream.",
                  metavar="FILE")
    parser.add_option("-t", "--tweets", dest="tweets",
                  help="Loads a tweets file", metavar="FILE")
    parser.add_option("-s", "--sentiments", dest="sentiments",
                  help="Load a sentiments file", metavar="FILE")
    parser.add_option("-o", "--analysis_output", dest="analysisOutput",
                  help="File name for the output file from analysis of data",
                  metavar="FILE")
    parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

    (options, args) = parser.parse_args()

    if args[0] == "tweet":
        li = Listener(options)
        stream = tweepy.Stream(auth=li.auth, listener=li)
        stream.filter(track=args[1:])
    elif args[0] == "analyze":
        al = Analyzer(options, args)
        dup_posts = "Total number of duplicate posts found in this .json file: "
        ufiltered = "Average sentiment of unfiltered tweets: "
        filtered = "Average sentiment of filtered tweets: "
        print("\n" + dup_posts + str(al.duplicate_post_number()))
        print("\n" + ufiltered + str(al.average_sentiment()))
        print("\n" + filtered + str(al.filtered_sentiment()))
    else:
        print("Example usage: python main.py --help")


if __name__ == '__main__':
    main()
