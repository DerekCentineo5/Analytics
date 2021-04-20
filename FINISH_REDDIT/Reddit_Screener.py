
    auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
    auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)


    if option == 'twitter':

        def DownloadData(self):
            # authenticating
            consumerKey = 'your key here'
            consumerSecret = 'your key here'
            accessToken = 'your key here'
            accessTokenSecret = 'your key here'
            auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
            auth.set_access_token(accessToken, accessTokenSecret)
            api = tweepy.API(auth)

            # input for term to be searched and how many tweets to search
            searchTerm = input("Enter Keyword/Tag to search about: ")
            NoOfTerms = int(input("Enter how many tweets to search: "))

            # searching for tweets
            tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)

            # creating some variables to store info
            polarity = 0
            positive = 0
            negative = 0
            neutral = 0

            # iterating through tweets fetched
            for tweet in tweets:
                # print (tweet.text.translate(non_bmp_map))    #print tweet's text
                analysis = TextBlob(tweet.text)
                # print(analysis.sentiment)  # print tweet's polarity
                polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

                if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                    neutral += 1
                elif (analysis.sentiment.polarity > 0.00):
                    positive += 1
                elif (analysis.sentiment.polarity < 0.00):
                    negative += 1

            # finding average of how people are reacting
            positive = percentage(positive, NoOfTerms)
            negative = percentage(negative, NoOfTerms)
            neutral = percentage(neutral, NoOfTerms)

            labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                    'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
            sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
            colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
            plt.axis('equal')
            plt.tight_layout()
            plt.show()


            # printing out data
            print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")




            print("General Report: ")

            if (polarity == 0):
                print("Neutral")
            elif (polarity > 0 and polarity <= 0.3):
                print("Weakly Positive")
            elif (polarity > 0.3 and polarity <= 0.6):
                print("Positive")
            elif (polarity > 0.6 and polarity <= 1):
                print("Strongly Positive")
            elif (polarity > -0.3 and polarity <= 0):
                print("Weakly Negative")
            elif (polarity > -0.6 and polarity <= -0.3):
                print("Negative")
            elif (polarity > -1 and polarity <= -0.6):
                print("Strongly Negative")

            print()
            print("Detailed Report: ")
            print(str(positive) + "% people thought it was positive")
            print(str(wpositive) + "% people thought it was weakly positive")
            print(str(spositive) + "% people thought it was strongly positive")
            print(str(negative) + "% people thought it was negative")
            print(str(wnegative) + "% people thought it was weakly negative")
            print(str(snegative) + "% people thought it was strongly negative")
            print(str(neutral) + "% people thought it was neutral")

            self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms)


        def cleanTweet(self, tweet):
            # Remove Links, Special Characters etc from tweet
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

        # function to calculate percentage
        def percentage(self, part, whole):
            temp = 100 * float(part) / float(whole)
            return format(temp, '.2f')

        def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms):
            labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                    'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
            sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
            colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
            patches, texts = plt.pie(sizes, colors=colors, startangle=90)
            plt.legend(patches, labels, loc="best")
            plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
            plt.axis('equal')
            plt.tight_layout()
            plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.DownloadData()