import feedparser
import re
from datetime import datetime
import os
import logging

LOGLEVEL = os.getenv('LOGLEVEL').upper()
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=LOGLEVEL)

def parse_ransomfeed(notified):
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
            "country": country_match.group(1).lower().strip() if country_match else "N/D",
            "website": website_match.group(1) if website_match else "N/D",
            "group": f"{e['tags'][0]['term']}",
            "notified": notified,
            "published": datetime.strptime(f"{e['published']}", "%a, %d %b %Y %H:%M:%S UTC")
        }
        result.append(temp_result)
    return result

if __name__ == '__main__':
    print(parse_ransomfeed())