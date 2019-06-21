from bs4 import BeautifulSoup
import requests
import re
import sys
import pprint
import json

lst = []
printed = False

url = "http://news.naver.com/main/hotissue/read.nhn?mode=LSD&mid=shm&sid1=100&oid=002&aid=0002094580&m_view=1" 

def usage():
    print ("Get the replies from news")
    print ("python3 reply.py <output filename> <oid> <aid start> <num of news>")
    exit(1)

def crawl(of, o, a):
    page = 1     
    header = { 
        "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
        "referer":url, 
         
    }  

    oid = "%03d" % o
    aid = "%010d" % a

    while True : 
        c_url = "https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
        r = requests.get(c_url,headers=header) 
        cont = BeautifulSoup(r.content,"html.parser")
        total_comm = str(cont).split('comment":')[1].split(",")[0] 
        username = str(cont).split('userName":')
        sympathy = str(cont).split('sympathyCount":')
        antipathy = str(cont).split('antipathyCount":')
        comments = str(cont).split('contents":')

        for i in range(len(username)):
            if i == 0:
                continue
            user = username[i].split(",")[0]
            sym = int(sympathy[i].split(",")[0])
            anti = int(antipathy[i].split(",")[0])
            comm = comments[i].split(",")[0]
            s = "%s, %s, %s, %d, %d, %s\n" % (oid, aid, user, sym, anti, comm)
            print (s)
            of.write(s)

        if int(total_comm) <= ((page) * 20): 
            break 
        else :  
            page += 1

def main():
    if len(sys.argv) != 5:
        usage()

    ofname = sys.argv[1]
    oid = int(sys.argv[2])
    start = int(sys.argv[3])
    num = int(sys.argv[4])

    of = open(ofname, "w")

    for aid in range(start, start + num):
        crawl(of, oid, aid)

    of.close()

if __name__ == "__main__":
    main()
