import feedparser

def update():
    ransomfeed_url = "https://ransomfeed.it/rss-complete.php"

    ransomfeed_parsed = feedparser.parse(ransomfeed_url)

    for e in ransomfeed_parsed['entries']:
        if "The target comes from <b>Italy</b>" in e['summary']:
            print(f"{e['title']} - {e['tags'][0]['term']}")


def main():
    update()

if __name__ == '__main__':
    main()