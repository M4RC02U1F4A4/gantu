import feedparser
import re

def parse_ransomfeed():
    ransomfeed_url = "https://ransomfeed.it/rss-complete.php"

    ransomfeed_parsed = feedparser.parse(ransomfeed_url)   

    for e in ransomfeed_parsed['entries']:
        country_match = re.search(r'The target comes from <b>(.*?)</b>', e['summary_detail']['value'])
        hash_match = re.search(r'We identify this attack with following <b>hash code</b>: <i>(.*?)</i>', e['summary_detail']['value'])
        website_match = re.search(r'Target victim <b>website</b>: <i>(.*?)</i>', e['summary_detail']['value'])

        result = {
            "hash": hash_match.group(1) if hash_match else "",
            "victim": f"{e['title']}",
            "country": country_match.group(1) if country_match else "",
            "website": website_match.group(1) if website_match else "",
            "group": f"{e['tags'][0]['term']}"
        }
        print(result)
    

if __name__ == '__main__':
    parse_ransomfeed()