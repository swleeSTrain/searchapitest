import datetime
import logging
import os
import sys
import urllib.request
import pandas as pd
import json
import csv
import re
import sys
import time
import azure.functions as func
from encodings import utf_8_sig  # 액셀파일에서 한글깨질때

import azure.functions as func

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
encText = urllib.parse.quote("치킨")

start = 1
end = 10
display = 10


sys.path.append('./')
def main(mytimer: func.TimerRequest, tablePath:func.Out[str]) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    idx = 0
    shop=[]
    for start_index in range(start, end, display):
        url = "https://openapi.naver.com/v1/search/shop?query=" + encText \
            + "&dislay=" + str(display) \
            + "&start=" + str(start_index)  # JSON 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            response_dict = json.loads(response_body.decode('utf-8'))
            items = response_dict['items']
            for item_index in range(0,len(items)):
                #remove_tag = re.compile('<,*?>')
                #title = re.sub(remove_tag, '',items[item_index]['title'])
                title = items[item_index]['title']
                lprice = items[item_index]['lprice']  
                idx += 1
                result = {
                    "제품명": title,
                    "최저가": lprice,
                    "PartitionKey": idx,
                    "RowKey": time.time()
                    
                }
                shop.append(result)
        else:
            print("Error Code:" + rescode)

    tablePath.set(json.dumps(shop))

     