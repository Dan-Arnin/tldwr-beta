import json
import requests
import googletrans
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