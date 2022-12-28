from fastapi import FastAPI,Request
import json

from summarizer import sum_button_translator
from pdf_summariser import pdf_to_sum
from playlist_summ import playlist_yt

application = FastAPI()

@application.get("/")                                   #Returns the status of the server
async def root():
    return {"message": "Server Active"}

@application.post("/summarize")                         #decorator that summarizes websites and yt videos based on the summary type from the json file
async def summarize_web(sum_dict: Request):
   
    sum_data = await sum_dict.json()

    if sum_data['type_of_summarization'] == 'website':
        summary = sum_button_translator(sum_data["summary_url"], sum_data["n_words"])

    else:
        summary = "Invalid parameters"

    return {'Summary': summary}


@application.post("/pdf_summarizer")                        #decorator that translates and summarizes websites and yt videos based on the summary type from the json file
async def pdf_summ(sum_dict: Request):

    sum_data = await sum_dict.json()

    if sum_data["type_of_summarization"] == 'pdf_summarizer':
        summary = pdf_to_sum(sum_data["summary_data"])
    
    else:
        return{"Error":"Invalid response"}

    return {'Summary': summary}


@application.post("/playlist")
async def playlist(sum_dict: Request):

    sum_data = await sum_dict.json()

    if sum_data["type_of_summarization"] == 'yt_playlist':
        summary = playlist_yt(sum_data["summary_url"])
        print('result', summary)

    else:
        return{"Error":"Invalid response"}

    return {'Summary': summary}









