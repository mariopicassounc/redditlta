import requests
from datetime import datetime, timezone
import json

def reddit_parser(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        posts = data['data']['children']
        parsed_posts = []

        for post in posts:
            post_data = post['data']
            title = post_data['title']
            description = post_data['selftext']
            
            utc_date = post_data['created_utc']
            # Convert UTC date to local date
            date = datetime.fromtimestamp(utc_date, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            link = post_data['url']

            parsed_posts.append({
                'title': title,
                'description': description,
                'date': date,
                'link': link
            })

        return parsed_posts

    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    urls=["https://www.reddit.com/r/Jobs4Bitcoins/.json","https://www.reddit.com/r/forhire/.json","https://www.reddit.com/r/hiring/.json"]
    for url in urls:
        posts = reddit_parser(url)

        if posts:
            print("Last 40 posts from r/Jobs4Bitcoins:")
            for post in posts:
                # if title contains hiring and not contents onlyfans
                if "hiring" in post['title'].lower() and "onlyfans" not in post['title'].lower():
                    print("Title:", post['title'])
                    print("Description:", post['description'][:200])  # Truncate description to 200 characters
                    print("Date:", post['date'])
                    print("Link:", post['link'])
                    print("=============================================================================================")    
                
                
        else:
            print("Failed to fetch posts from " + url)