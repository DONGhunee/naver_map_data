import os
import sys
import urllib.request
import json
import csv

#progress bar 
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
     formatStr = "{0:." + str(decimals) + "f}" 
     
     percent = formatStr.format(100 * (iteration / (total)))
     filledLength = int(round(barLength * iteration / (total)))
     bar = '#' * filledLength + '-' * (barLength - filledLength) 
     sys.stdout.write('\r%s |%s| %s%s' % (prefix, bar, percent, '%')),
     if (float(percent) ==100): 
        sys.stdout.write('\r%s |%s| %s%s %s!!' % (prefix, bar, percent, '%',suffix)) 
        sys.stdout.write('\n')
        sys.stdout.flush()


client_id = "입력해주세요" #api 아이디
client_secret = "입력해주세요"       #api secret
input = input("검색어를 입력해 주세요: ")
input.strip()
encText = urllib.parse.quote(input)  #검색어입력

display = "30"  #고정
cont = 0
# opencsv = open("output.csv",'w')
f = csv.writer(open("test.csv", "w+"))

def total():

    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText +"&"+"display="+display # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        json_parse = json.loads(response_body)
        total = int(json_parse["total"])
     
      
    else:
        print("Error Code:" + rescode)
    
    if total >= 1000:
        total = 999 
    return total


total = total()



for start in range(1,total,30):
    start = str(start)
    url = "https://openapi.naver.com/v1/search/local.json?query=" + encText +"&"+"display="+display+"&"+"start="+start # json 결과
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    
    if(rescode==200):
        response_body = response.read()
        json_parse = json.loads(response_body)
        

        items = json_parse["items"]
        
        if (((total-int(start))/30)) <=1:
            
          printProgress(total, total, 'Progress:', 'Complete', 1, 100)
        else:
          printProgress(int(start), total, 'Progress:', 'Complete', 1, 100)
        try:
            if cont ==0:
                f.writerow(items[0].keys())
                cont +=1
            
            for x in items:
                f.writerow(x.values())
        except IndexError:
            pass
    else:
        print("Error Code:" + rescode)
    
