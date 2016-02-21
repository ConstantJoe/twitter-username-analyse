#!/bin/env python

#import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN =    '3862106309-Ta2UbYJHHHL63XwzuBRFLfJ9kLnUsFsqlZnswEK'#'YOUR ACCESS TOKEN"'
ACCESS_SECRET =   'e6xe6NySQCqslwirfCNmOzkwNiCnosxpkpdybKldfa46p' #'YOUR ACCESS TOKEN SECRET'
CONSUMER_KEY =    'N7aJMwQpUAt7N6bgZmNwHs7dD' #'YOUR API KEY'
CONSUMER_SECRET = 'Nah2IKCQDaPLIjPkGRrKwrowSCGvopi2IbcfrG61GrTgjfBQ66' #'ENTER YOUR API SECRET'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)
            
#load in the dictionary
f = open('/usr/share/dict/words', 'r')
save_file = open("remaining_names.txt", "w")

keep_going = True
while keep_going:
    words = []
    for x in range(0,100):
        w = f.readline()
        if w =="":
            keep_going = False
        w = w[:-1]    #remove newline character
        w = w.lower() #make all words lowercase
        words.append(w)
    #taking 100 words at a time, do a lookup to the twitter api

    badwords = []

    #remove words containing illegal characters (e.g. :')
    for x in words:
        if "'" in x:
            badwords.append(x)

    for x in badwords:
        words.remove(x)

    #create a string out of the words
    tempwords = []
    for x in words:
        tempwords.append(x + ',')

    words_as_string = ''.join(tempwords)
 
    #print("do a lookup")
    results = twitter.users.lookup(screen_name=words_as_string)
    #print("finished the lookup")

    for x in words:
        x = x.encode('ascii', 'ignore')    

    #only keep those who aren't matched
    for founduser in results:
        name = founduser["screen_name"].lower().encode('ascii', 'ignore')
        if name in words:
            words.remove(name) #problem: words is unicode, name is str
    #print("removed matched words") 
    #the remaining words may be from suspended accounts
    #the only way I've found to check is to do a "show" API call - this will tell you if the account is suspended or just hasn't been created yet
    
    #print(words)

    badwords = []
    for x in words:
        try:
            result = twitter.users.show(screen_name=x)
            #print("read remaining name")
        except TwitterHTTPError as err:
            err_code = err.args[0][-5:-3]
            #print("suspended account")
            #print(err.args[0])
            #print(err_code)
            #print(err.args[0][-5:-3])
            if err_code == "63" or err_code ==".'": #error code for suspended account - 'd has to be changed
                badwords.append(x)
            if err_code == "88" or err_code == "d'": #error code for over rate limit
                print("over rate limit")
  
    print("badwords")
    for x in badwords:
        print(x) 
        words.remove(x)

    print("remaining words:")
    print(words)
    #some of the remaining words (for example: bollywood) give a "Sorry, that page doesn't exist" message yet you're not allowed to create a page with that handle

    #for now save to a file
    for x in words:
        save_file.write(x + "\n")

f.close()
save_file.close()
