from django.shortcuts import render
from googlesearch import search
import urllib
import requests,random
from bs4 import BeautifulSoup
import time,json
from urllib.parse import urljoin
# Create your views here.

def googleCustomSearch(term,fileFormat,*start):
    BASE_URL='https://www.googleapis.com/customsearch/v1?'
    if start:
        PARAMS={'fileType':fileFormat,
            'safe':"active",
            'key':'key',
            'cx':'id',
            'q':term,
            'start':start,
        }
    else:
        PARAMS={'fileType':fileFormat,
            'safe':"active",
            'key':'AIzaSyCRnZPkS3zDBbzFL8Bn5vb2In8oFijBIs4',
            'cx':'010825230688325870404:28ddwsmp3uq',
            'q':term,
        }
    r = requests.get(BASE_URL,PARAMS)
    data = r.json()
    results=[]
    numberOfResults=data['queries']['request'][0]['count']
    startIndex=data['queries']['request'][0]['startIndex']
    print(numberOfResults)
    for i in range(numberOfResults):
        if data['items']:
            item = {
                    "title": data['items'][i]['title'],
                    "link": data['items'][i]['link'],
                    "description":data['items'][i]['snippet']
                }
            fileValidators=['.'+fileFormat,'='+fileFormat]
            for validator in fileValidators:
                if validator in item['link']:
                    results.append(item)
    context={'results':results,'startIndex':startIndex}
    return results



def home(request):
    return render(request,'find/index.html')

def results(request):
    search_term=request.POST.get('search')
    file_format=request.POST.get('format')
    results=googleCustomSearch(search_term,file_format)
    print(file_format)
    context={'result':results}
    return render(request,'find/results.html',context)

def terms(request):
    return render(request,'find/terms.html')
def privacy(request):
    return render(request,'find/privacy.html')
