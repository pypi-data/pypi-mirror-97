import json
import requests
from langdetect import detect
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from textblob_de import TextBlobDE
import re
from urllib.parse import urlparse, parse_qs

class YTSentimentAnalysis():
    """YouTube Sentiment Analysis class for extract comments from youtube video
    and analysis comments to get sentiments

    Attributes:
        api (string): api needed to get comments from youtube video
        url (string): url of the video to be analyzed
    """


    def __init__(self, api, url):
        self.api = api
        self.url = url

    def _get_data(self, url):
        """ get the a json data from an url """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        return data

    def _get_video_id(self):
        """ get the video id from url """
        query = urlparse(self.url)
        if query.hostname == 'youtu.be': return query.path[1:]
        if query.hostname in {'www.youtube.com', 'youtube.com'}:
            if query.path == '/watch': return parse_qs(query.query)['v'][0]
            if query.path[:7] == '/embed/': return query.path.split('/')[2]
            if query.path[:3] == '/v/': return query.path.split('/')[2]
        return None

    def get_video_title(self):
        """ get the video title """
        id = self._get_video_id()
        api_key = self.api
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
        data = self._get_data(url)
        return data["items"][0]["snippet"]["title"]

    def get_video_thumbnail(self):
        """ get video thumbnail """
        id = self._get_video_id()
        api_key = self.api
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={api_key}"
        data = self._get_data(url)
        return data["items"][0]["snippet"]["thumbnails"]['high']['url']

    def _get_video_comments(self):
        id = self._get_video_id()
        api_key = self.api
        url_comments = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&textFormat=plainText&videoId={id}&key={api_key}"
        data = self._get_data(url_comments)
        comments = []
        while True:
            for item in data['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            if 'nextPageToken' in data:
                nextPageToken = data['nextPageToken']
                url_nextPage = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&pageToken={nextPageToken}&videoId={id}&key={api_key}"
                data = self._get_data(url_nextPage)
            else:
                break
        return comments

    def comments_analyse(self):
        comments = self._get_video_comments()
        allcomments = []
        polarity = []
        for comment in comments:
            allcomments.append(comment)
            try:
                if detect(comment) == 'de':
                    text = TextBlobDE(comment)  
                    x = text.sentiment.polarity
                    polarity.append(x)
                elif detect(comment) == 'fr':
                    blob = TextBlob(comment, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
                    x = blob.sentiment[0]
                    polarity.append(x)
                else:
                    text = TextBlob(comment)  
                    x = text.sentiment.polarity
                    polarity.append(x)
            except:
                text = TextBlob(comment)  
                x = text.sentiment.polarity
                polarity.append(x)

        return allcomments, polarity
        
    def sentiment_summary(self):
        _, polarity = self.comments_analyse()
        pos = neg = neu = 0 
        for x in polarity:
            if x > 0:
                pos += 1
            elif x < 0:
                neg += 1
            else:
                neu += 1
        return pos,neg,neu