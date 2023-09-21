from rss_parser import Parser
from dateutil.relativedelta import relativedelta
import feedparser, datetime, re, requests, time, redis, json

url = "https://ransom.insicurezzadigitale.com/rss-complete.php"
feed = feedparser.parse(url)

def rss():
    r = requests.get(url)
    victims = []

    for i in range(0,100):
        reg = "The target comes from <b>Italy</b>"
        if reg in feed.entries[i].summary:
            victims.append(feed.entries[i].title_detail.value)
    for j in range(0, len(victims)):
        v = victims[j]
        info(v)

def info(vict):
    search = r".*" + re.escape(vict) + r".*"
    result = False

    for i in range(0, 3):
        date = datetime.datetime.today() - relativedelta(months=i)
        year = date.year
        month = date.month
        
        url = f"https://api.ransomware.live/victims/{year}/{month}"
        headers = {'accept': 'application/json'}
        res = requests.get(url=url, headers=headers)
 
        if res.status_code == 200:
            data = res.json()
            for item in data:
                post_title = item["post_title"]
                if re.search(search, post_title, re.IGNORECASE):
                    print("Trovata corrispondenza:", post_title)
                    group = item["group_name"]
                    print("Group Name:", group)
                    time_nf = item["published"]
                    #ToDo: Cancellare millisec per unificare il tempo 
                    print("Published:", time_nf)
                    print("Screenshot:", item["screenshot"])
                    print("Found on: ransomware.live")
                    result = True
                    # Json da passare a DB 
                    data = {
                        "group_name": group,
                        "published": time_nf,
                        "website": find_website(vict),
                        "found_on": "ransomware.live"
                    }
                    vict_json = json.dumps({"victim": vict, "info": data}, indent=4)
                    print("------------------------")
        else:
            print('Error:', res.status_code)
    
#    conn(vict_json)

    if result is False:
        rss_pro(vict)

def rss_pro(vict):
    for i in range(0,100):
        v = feed.entries[i]
        if v.title_detail.value == vict:
            time_rss = time.strftime("%Y-%m-%d %H:%M:%S", v.published_parsed)
            print("Trovata corrispondenza:", vict)
            print("Group Name:", v.tags[0].term)
            print("Published:", time_rss)
            print("Found on: ransom.insicurezzadigitale.com")
            find_website(vict)
            print("------------------------")
            

def find_website(vict):
    for i in range(0,100):
        v = feed.entries[i]
        if v.title_detail.value == vict:
            website = re.search(r'<i>(https?://\S+)</i>', v.summary_detail.value)
            if website:
                print("Website:", website.group(1))
                return website.group(1)
            else:
                print("No Website found.")
                return "No Website found."
            
#def conn(json):
#    redis.json().set('db:0', '$RSM', json)
#    print("Connection effettuata")

if __name__ == "__main__":
    #rss_pro("Municipality-of-Ferrara")
    rss()