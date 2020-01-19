import tweepy
import datetime, time
import requests
import os
from collections import defaultdict

# Authenticate to Twitter
auth = tweepy.OAuthHandler("ptgs5klWT9Y21gfeixUKt6f9K", "qfmj3fvi6xUkx9Tw75TRESQuFzExVKmtTYYPDDmyqP1eTSNN80")
auth.set_access_token("1218695420773167104-e8rzJ8fJmMENf0QbHUzcEyskGQYYzL", "2Mrr4MeDmb24DH2WTTj3WNzgIK8BQe0bxsdnSpxVyqCd0")
# Create API object
api = tweepy.API(auth)
# Current Dates
today = time.strftime('%m-%d')
date_List = ['01-21','09-20','12-9',]
# List of ID to Reply
ids = []
# Function posting main fact
def tweetMainFact(adict):
    url = adict[1]['Image']
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
            status = f"Happy birthday {adict[1]['Name']}! Born in {adict[1]['Born']} on {adict[0]}! \n \n{adict[1]['Facts'][0]}"
            api.update_with_media(filename, status)
            image.close()
            os.remove(filename)
def tweetNextFact(adict):
    status = f"{adict[1]['Facts'][ct]}"
    api.update_status(status, ids[-1])
def addID():
    for status in api.user_timeline():
        ids.append(status.id)
        break
# Dictionary
pointer = ''
counter = 0
womenTxt = open('women.txt')
womenDict = defaultdict(dict)
for i in womenTxt.readlines():
    temp = i.split()
    if counter == 0:
        pointer = temp[0] + " " + temp[1].replace(',', '')
        counter += 1
    elif counter < 3:
        womenDict[pointer][temp[0].replace(':', '')] = " ".join(temp[1:])
        counter += 1
    elif counter == 3:
        womenDict[pointer][temp[0].replace(':', '')] = temp[1]
        counter += 1
    elif counter == 4:
        womenDict[pointer]['Facts'] = []
        womenDict[pointer]['Facts'].append(" ".join(temp[1:]))
        counter += 1
    elif counter < 7:
        womenDict[pointer]['Facts'].append(" ".join(temp[1:]))
        counter += 1
    elif counter == 7:
        womenDict[pointer]['Facts'].append(" ".join(temp[1:]))
        counter = 0
todaysDate = " ".join(datetime.date.today().strftime("%B %d, %Y").split()[0:2]).rstrip(',')
if todaysDate in womenDict.keys():
    for i in womenDict.items():
        if i[0] == todaysDate:
            tweetMainFact(i)
            totalFacts = len(i[1]['Facts'])
            ct = 0
            for _ in range(totalFacts):
                addID()
                tweetNextFact(i)
                ct += 1
            break
else:
    api.update_status('No significant birthdays yet):')





