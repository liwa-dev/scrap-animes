import requests
from bs4 import BeautifulSoup
import utils
import time
import json
import re
import certifi
cafile = certifi.where()


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
# "You can change the link as needed; just make the necessary modifications to the code."
url_template = "https://o.anime-slayer.com/?search_param=animes&s={}"
datas = utils.select("animes", column_list="title, mal_id, episodes")
num_datas = len(datas)

try:
    f=open('index.json',"r")
    data = json.load(f)
    i=int(data["num_page"])
    k=int(data["episode"])
    print('Script will continue from',str(i),'with episode',str(k))
    f.close()
except FileNotFoundError:
    i=0
    k=0


for j in range(i,num_datas):
    data = datas[j]
    url = url_template.format(data["title"])
    utils.insert('Episode', data_dict={
        "mal_id": data["mal_id"],
        "episode_count": data["episodes"],
    }, upsert=True)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    finds = soup.findAll("div", class_="anime-card-title")
    for find in finds:
        ahref = soup.find("a", class_="overlay")
        if ahref is None:
            continue
        ahref = ahref["href"]
        response = requests.get(ahref, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        mal_link = soup.find("a", class_="anime-mal")
        if mal_link is None:
            continue
        mal_id_match = re.search(r'\d+', mal_link.get("href"))
        if mal_id_match is None:
            continue
        mal_id = mal_id_match.group()
        if (int(mal_id) == int(data["mal_id"])):
            #CONDITION CHECK MAL ID
            episodes = soup.findAll("div", class_="episodes-card-title")
            for w in range(k,len(episodes)):
                episodeName = episodes[w].find("a").text
                Servers = episodes[w].find("a")["href"]
                response = requests.get(Servers, headers=headers)
                soup = BeautifulSoup(response.content, "html.parser")
                linkServers = soup.findAll("a" ,attrs={"data-ep-url": True})
                for linkServer in linkServers:
                    #try:
                    #    response = requests.get(linkServer["data-ep-url"], stream=True, verify=cafile)
                        #if (response.status_code == 200):
                    #print('Streaming URL is working')
                    selectquery = utils.select("Server", condition_dict={"link_server": linkServer['data-ep-url'],"server_name": linkServer.text,"mal_id" : data["mal_id"]})
                    print("Episode",episodeName,"LinkServer",linkServer["data-ep-url"],"ServerName",linkServer.text)
                    if len(selectquery) > 0:
                        print("Skipping already exists in the Server table.", data["title"])
                    else:
                        utils.insert('Server', data_dict={
                            "link_server": linkServer['data-ep-url'],
                            "server_name": linkServer.text,
                            "mal_id": data["mal_id"],
                            "Episode" : episodeName
                        })
                    #     else:
                    #         print("Streaming URL is not working. Status code: ", response.status_code)
                    # except requests.exceptions.ConnectionError:
                    #     print("Streaming URL is not working. Status code: ", response.status_code)



                f=open('index.json',"w")
                k = k + 1
                index = {"num_page" : str(i), "episode" : str(k)}
                json.dump(index,f)
                f.close()

    time.sleep(1)
    f=open('index.json',"w")
    print("NEXT")
    k = 0
    i = i + 1
    index = {"num_page" : str(i), "episode" : str(k)}
    json.dump(index,f)
    f.close()

    
