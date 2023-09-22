import feedparser
import re
from datetime import datetime
import requests
import itertools
from bs4 import BeautifulSoup

def parse_ransomfeed():
    ransomfeed_url = "https://ransomfeed.it/rss-complete.php"

    ransomfeed_parsed = feedparser.parse(ransomfeed_url)   
    
    result = []
    for e in ransomfeed_parsed['entries']:
        country_match = re.search(r'The target comes from <b>(.*?)</b>', e['summary_detail']['value'])
        hash_match = re.search(r'We identify this attack with following <b>hash code</b>: <i>(.*?)</i>', e['summary_detail']['value'])
        website_match = re.search(r'Target victim <b>website</b>: <i>(.*?)</i>', e['summary_detail']['value'])

        temp_result = {
            "_id": hash_match.group(1) if hash_match else "N/D",
            "victim": f"{e['title']}",
            "country": country_match.group(1) if country_match else "N/D",
            "website": website_match.group(1) if website_match else "N/D",
            "group": f"{e['tags'][0]['term']}",
            "notified": False,
            "published": datetime.strptime(f"{e['published']}", "%a, %d %b %Y %H:%M:%S UTC")
        }
        result.append(temp_result)
    return result
    
def all_ransomfeed():
    url = "https://ransomfeed.it/index.php?page=post_details&id_post="

    result = []
    for i in itertools.count(0):
        response = requests.get(f"{url}{i}")

        soup = BeautifulSoup(response.text, 'html.parser')
        temp_result = {"notified": True}
        bf_result = soup.find('h2')
        
        if bf_result:      
            hash = soup.find_all('p')
            for h in hash:
                if "Hash di rilevamento:" in str(h):
                    temp_result['_id'] = str(h).replace('<p><b>Hash di rilevamento:</b> ','').split(' <br/>')[0]
                    temp_result['victim'] = str(bf_result).replace("<h2><span class=\"badge badge-info\">Vittima:</span> ", "").replace("</h2>", "")
                    temp_result['country'] = str(h).split('<b>Vittima localizzata in:</b>')[1].replace("</p>", "")
                    
                if "Sito web:" in str(h):
                    temp_result['website'] = str(h).replace("<p><b>Sito web:</b> ", "").replace("</p>", "")
            bf_result = soup.find('div', class_='infocard').find('h6')
            temp_result['published'] = datetime.strptime(str(bf_result).split(" dal gruppo <span")[0].replace("<h6>", "").replace("rilevato il ", ""), "%d-%m-%Y %H:%M:%S")
        result.append(temp_result)
    return result

if __name__ == '__main__':
    # print(parse_ransomfeed())
    all_ransomfeed()