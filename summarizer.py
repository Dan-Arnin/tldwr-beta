from youtube_transcript_api import YouTubeTranscriptApi
import urllib.request
import json
import urllib
from bs4 import BeautifulSoup
import requests
from googletrans import Translator
translator = Translator()
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def Text_sum(article):
    ret=translator.translate(article,dest="en")
    art=ret.text
    output = query({
    "inputs": "{}".format(art)})
    return(output[0]['summary_text'])

def sum_button_translator(link,nwords):
    l1=link[:23]
    if(l1=='https://www.youtube.com'):
        new_link = link[32:]
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % new_link}
        url = "https://www.youtube.com/oembed"
        print(link)
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            #print('Titel: ' + data['title'])

        # retrieve the available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(new_link)
        l = []
        # iterate over all available transcripts
        for transcript in transcript_list:
            # fetch the actual transcript data
            data = transcript.fetch()
            #print(data)
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
            new_subs_list.append(subs_list[i]+" ")
        # print(new_subs_list)
        act_subs = ""
        for i in new_subs_list:
            i.strip("\n")
            act_subs += i
        ARTICLE = act_subs[:500]
        #print(youtube_captions)
    else:
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(['h1', 'p'])
        text = [result.text for result in results]
        ARTICLE = ' '.join(text)
    summary=Text_sum(ARTICLE)
    ret=translator.translate(summary,dest="en")
    return(ret.text)