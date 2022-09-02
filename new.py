from flask import Flask,jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def gagan():
    a="https://api.openweathermap.org/data/2.5/onecall?lat=18.4575&lon=73.8508&exclude=current,minutely,hourly,alerts&appid=f390c2cbd5a464b871f0ffabefb193ac"
    response=requests.get(url=a)
    data=response.json()
    print('Weather api activated',data['daily'][2]['weather'][0]['main'])
    m=str(data['daily'][2]['weather'][0]['main'])
    final_list=[]
    final_list.append("It's "+str(m)+" today")    
    for i in range(1,6):
        if str(data['daily'][i]['weather'][0]['main'])=="Rain":
            if i ==1:
                final_list.append("Although, its raining tommorow")
            elif i==2:
                final_list.append("Although, it's raining the day after tommorow")
            else:
                final_list.append("Although, it's going to rain in "+str(i)+' days')
    return(final_list)



def econews():
    l = []
    for i in range(10):
        try:
            print("econews function activated")
            response = requests.get(url="https://economictimes.indiatimes.com/industry")
            soup = BeautifulSoup(response.text,"html.parser")
            title = str(((soup.find_all("li", itemprop="itemListElement"))[int(i)]).find("a").getText())
            link = (((soup.find_all("li", itemprop="itemListElement"))[int(i)].find("a").get("href")))
            m=f"https://economictimes.indiatimes.com/industry{link}"
            title_str = title+"\n\n"
            
            response2 = requests.get(url=m)
            soup = BeautifulSoup(response2.text,"html.parser")
            
            article_str=soup.find("div", class_="edition clearfix").find("article").find("div",class_="artText").getText()
            m = {
                "Title":title_str,
                "Article":article_str,
            }
            l.append(m)
        except:
            pass
    return l

def gold():
    print("gold")
    response = requests.get(url="https://rankajewellers.in/pages/todays-gold-rates-in-chinchwad-pune")
    soup =  BeautifulSoup(response.text,"html.parser")
    t = soup.find("div",class_="p").find("table").find_all("td")
    m = list(map(lambda t:str(t.getText()),t))
    # print(m)
    l=[]
    for g in range(7):
        i=g
        i =g*3
        l.append(str(m[i]+" "+m[i+1]+" "+m[i+2]))
    return l

def link_news():
    report = []
    if True:
        #pune
        response=requests.get(url="https://timesofindia.indiatimes.com/rssfeeds/-2128821991.cms")
        local = []
        for i in range(20):
            try:
                news_title = (response.text.split("<item>")[i].split("<title>")[1].split("</title>")[0])
                news_text=(response.text.split("<item>")[i].split(";")[4].split("</description>")[0])
                news_link = response.text.split("<item>")[i].split(";")[4].split("</link>")[1].split("<guid>")[1].split("</guid>")[0]
                local.append({"Title":news_title,"Article":news_text,"Link":news_link})
            except:
                pass

      
        #top
        imp = []
        response=requests.get(url="https://timesofindia.indiatimes.com/rssfeedstopstories.cms")
        for i in range(20):
            try:
                news_title = response.text.split("<item>")[i].split("<title>")[1].split("</title>")[0]
                news_description = response.text.split("<item>")[i].split("<description>")[1].split("</description>")[0]
                news_link = (response.text.split("<item>")[1].split("<title>")[1].split("<link>")[1].split("</link>")[0])
                imp.append({"Title":news_title,"Article":news_text,"Link":news_link})
            except:
                pass

        
        # global
        world = []
        response=requests.get(url="https://timesofindia.indiatimes.com/rssfeeds/296589292.cms")
        for i in range(20):
            try:
                world_title = (response.text.split("<item>")[1].split("<guid>")[1].split("</guid>")[0])
                world_description = response.text.split("<item>")[i].split("<description>")[1].split("</description>")[0].split(";")[4]
                # world_link = response.text.split("<item>")[i].split("<link>")[1].split("</link>")[0]
                world_link="abc"
                world.append({"Title":world_title,"Article":world_description,"Link":world_link})
            except:
                pass

        # Country
        country = []
        response=requests.get(url="https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms")
        for i in range(20):
            try:
                news_title = response.text.split("<item>")[i].split("<title>")[1].split("</title>")[0]
                news_description = response.text.split("<item>")[i].split("<description>")[1].split("</description>")[0].split(";")[8]
                news_link = response.text.split("<item>")[1].split("<title>")[1].split("<guid>")[1].split("</guid>")[0]
                # news_link="abc"
                country.append({"Title":news_title,"Article":news_description,"Link":news_link}) 
            except:
                pass
    report.append(local)
    report.append(imp)
    report.append(country)
    report.append(world)
    report.append(local)
    return report
key = '650dcdb8-21d0-46ed-8cf7-aeb613675c40'
website = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

url = website

parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD',
}

headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': key,
}

response = requests.get(url,params=parameters,headers=headers)
data = response.json()


def single_coin_info(i):
  name = data['data'][i]['symbol']
  prices = (data['data'][i]['quote']['USD'])
  price_keys=list(prices.keys())
  price_index = [0,3,4,5]
  final_list= []
  final_list.append(name)
  temp = { }
  for m in price_index:
    temp.update({price_keys[m] : round(prices[str(price_keys[m])],2)})
    
  final_list.append(temp)
  return final_list

def all_coin_info(i):
  final_list = []
  for _ in range(i):
    final_list.append(single_coin_info(_))
  return final_list
# @app.route('/econews/<int:i>')
@app.route('/')
def allthethings():
    m = {
        "Weather":gagan(),
        "EcoNews":econews(),
        "Gold":gold(),
        "Link_news":link_news(),
        "Bitcoins":all_coin_info(10),
    }

    return jsonify(m )

if __name__=="__main__":
    app.run(debug=True)


