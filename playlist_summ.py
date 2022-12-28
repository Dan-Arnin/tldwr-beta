import scrapetube
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import json
import urllib
import os
from googletrans import Translator
translator = Translator()
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def pdf_to_sum(text):
    summary = Text_sum(text)
    return(summary)

def Text_sum(article):
    ret=translator.translate(article,dest="en")
    art=ret.text
    output = query({
    "inputs": "{}".format(art)})
    return(output[0]['summary_text'])

def yt_next_check(VideoID, nwords):
    new_link = VideoID[32:]
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % new_link}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        # print('Titel: ' + data['title'])

    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(new_link)
    l = []
    # iterate over all available transcripts
    for transcript in transcript_list:
        # fetch the actual transcript data
        data = transcript.fetch()
        # print(data)
        l.append(data)
    # print(l)
    subs_list = []
    for i in l:
        for j in i:
            for k in j:
                # print(j[k])
                subs_list.append(j[k])
    # print(subs_list)
    new_subs_list = []
    for i in range(0, len(subs_list), 3):
        new_subs_list.append(subs_list[i])
    # print(new_subs_list)
    act_subs = ""
    for i in new_subs_list:
        i.strip("\n")
        act_subs += i + ","
    youtube_captions = act_subs[:500]
    return(Text_sum(youtube_captions))
    #transcript = transcript_list.find_transcript(['en'])

def playlist_yt(pl):
    pl = pl[49:]
    videos = scrapetube.get_playlist(pl)
    l=[]
    for video in videos:
        l.append(video["videoId"])
    l=l[:5]
    l_new=[]
    for i in l:
        m="https://www.youtube.com/watch?v="+str(i)
        l_new.append(yt_next_check(m,40))
    playlist_text=""
    j=1
    for i in l_new:
        playlist_text+="\n"+"video"+str(j)+": "+i+"\n"
        j=j+1
    return(playlist_text)