import fileinput
import sys
import os
import random
import logging
import time
import getopt
import tweepy

def update_file(quotes_file, quotes):
    # remove the old quotes file
    os.remove(quotes_file)

    # create the new quotes file, without the
    # posted qyote and any quotes of which
    # the content was too long
    with open(quotes_file, 'wb') as f:
        for quote in quotes:
            f.write(quote)

    logging.info('Wrote new quotes file: {0}'.format(quotes_file))

def get_twitter_api(tokens_file):
    # read customer keys and
    # account tokens from input file
    with open(tokens_file) as f:
        tokens = f.read().splitlines()

    # setup the tweepy api
    auth = tweepy.OAuthHandler(tokens[0], tokens[1])
    auth.set_access_token(tokens[2], tokens[3])
    api = tweepy.API(auth)

    return api

def process_quote(quote, tokens_file, hashtag):
    # get the character (auto) and content
    # of the quote
    character = quote[0]
    content = quote[1]

    # get the twitter api use to post
    # the quote on twitter
    api = get_twitter_api(tokens_file)

    # get the tweet in the right quoting format
    tweet = '"{0}" - {1} #{2}'.format(content, character, hashtag)

    # post the quote to twitter
    api.update_status(status=tweet)
    
    logging.info('Tweet has been posted to twitter')
    logging.info('Tweet content: {0}'.format(tweet))

def get_random_quote(quotes, hashtag_length):
    quote = ''

    # continue to fetch a new quote,
    # until one is found that fits
    # inside the 140-character Twitter limit
    while(True):
        # check if the quotes list is empty.
        # if so, exit the program
        if not quotes:
            logging.error('There are no new quotes, program will exit!')
            sys.exit(0)

        # choose a random quote
        index = random.randrange(len(quotes))
        quote = quotes.pop(index)

        # if the quote is not to large,
        # use it (by breaking the while-loop)
        if (len(quote) <= (136 - hashtag_length)):
            break

    logging.info('Retrieved new quote')

    # strip newlines from quote
    quote = quote.rstrip()

    # split quote author and text
    quote = quote.split('|')
    
    return quote

def get_quotes(file):
    # prepare new list which will
    # contain all quotes from the file
    quotes = []
    # open the input file
    with open(file) as f:
        # add the lines from this file to the overall list
        quotes.extend(f.readlines())
    logging.info('Quotes have been read from {0}'.format(file))

    return quotes

def set_logging_config():
    # get current day
    # (for one logging file per day)
    day = time.strftime('%Y%m%d')
    logfile = 'log' + day + '.txt'
    
    # set logging configuration
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] %(asctime)s - %(message)s',
                        filename='log/' + logfile)

def print_usage():
    # print the program usage to the user
    print 'Usage: -q <quotes file> -t <tokens file> -h <hashtag>'
    print 'Long arguments:'
    print '-q: --quotes'
    print '-t: --tokens'
    print '-h: --hashtags'
    sys.exit(2)

def check_command_line_arguments(argv):
    # check if the correct command line arguments
    # have been specified.
    # if not, print the desired usage
    try:
        opts, args = getopt.getopt(argv, 'q:t:h:', ['quotes=', 'tokens=', 'hashtag='])
        return opts
    except getopt.GetoptError:
        print_usage()

def main(argv):
    set_logging_config()

    # parse command line arguments and
    # fill quotes_file and tokens_file variables
    opts = check_command_line_arguments(argv)
    for opt, arg in opts:
        if opt in ('-q', '--quotes'):
            quotes_file = arg
        elif opt in ('-t', '--tokens'):
            tokens_file = arg
        elif opt in ('-h', '--hashtag'):
            hashtag = arg
        else:
            print_usage()
    if not 'quotes_file' in locals() or not 'tokens_file' in locals() or not 'hashtag' in locals():
        print_usage()
     
    # retrieve all quotes from input file
    quotes = get_quotes(quotes_file)
    
    # get random quote, total length cannot be longer than
    # the resulting tweet.
    # this length includes some added quote symbols (")
    # and the hashtag including the hash symbol (#)
    quote = get_random_quote(quotes, len(hashtag) + 1)

    # process quote
    process_quote(quote, tokens_file, hashtag)

    # write new quotes file,
    # minus this random quote
    update_file(quotes_file, quotes)
    
if __name__ == "__main__":
    main(sys.argv[1:])
