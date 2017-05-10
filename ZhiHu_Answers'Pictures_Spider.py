from urllib import request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import json
import os

limit = 20
anonymity = 0


def download_picture(response, answers_num):
    global anonymity
    global left
    global limit

    for i in range(0, answers_num):
        bsObj = BeautifulSoup(response.get("data")[i]["content"], "lxml")
        author_name = response.get("data")[i]["author"].get("name")
        url_token = response.get("data")[i]["author"].get("url_token")
        if url_token == "":
            author_name = str(anonymity) + "号匿名用户"
            anonymity += 1
        left -= 1
        print(author_name+":"+url_token+"       "+"answers_left:",left)

        images = bsObj.findAll("img", {"class": "origin_image zh-lightbox-thumb"})
        count = 0
        for image in images:
            print(image["data-original"])
            request.urlretrieve(image["data-original"], author_name+str(count)+".jpg")
            count += 1

    if left > 0:
        url = request.Request(response.get("paging")["next"])
        url.add_header("authorization", "oauth c3cef7c66a1843f8b3a9e6a1e3160e20")
        html = request.urlopen(url)
        response = json.load(html)
        if left > 20:
            download_picture(response, limit)
        else:
            download_picture(response, left)


while True:
    try:
        question_id = input("please input the question id:\n")
        include = "data%5B*%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B*%5D.author.badge%5B%3F(type%3Dbest_answerer)%5D.topics"
        start_url = "https://www.zhihu.com/api/v4/questions/{question_id}/answers?include={include}&offset=&limit={limit}&sort_by=default"
        url = request.Request(start_url.format(question_id=question_id, include=include, limit=limit))
        url.add_header("authorization", "oauth c3cef7c66a1843f8b3a9e6a1e3160e20")
        html = request.urlopen(url)
        break
    except HTTPError:
        continue

response = json.load(html)
total = response.get("paging")["totals"]
left = total

if total >= 0:
    path = os.getcwd()+"/"+question_id
    if os.path.exists(path) is False:
        os.mkdir(path)
    os.chdir(path)
else:
    print("no answers here!")

if total < 20:
    download_picture(response, total)
else:
    download_picture(response, limit)
