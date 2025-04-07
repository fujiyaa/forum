import requests
from bs4 import BeautifulSoup
import certifi

def get_forum_text(topic_id, max_batches=10, start_from_post=1):
    all_text = []
    last_post = start_from_post
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    seen_posts = set()  

    for batch in range(max_batches):
        print(f"🔄 Loading {batch + 1} (posts {last_post}–{last_post + 49})...")
        url = f"https://osu.ppy.sh/community/forums/topics/{topic_id}?n={last_post}"

        try:
            response = requests.get(url, headers=headers, verify=certifi.where(), timeout=10)
            response.raise_for_status()
        except requests.exceptions.SSLError:
            print(f"⚠️ SSL")
            response = requests.get(url, headers=headers, verify=False, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"❌ {e}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", class_="forum-post__body")

        unique_posts = []
        for post in posts:
            text = post.get_text(strip=True, separator="\n")
            if text not in seen_posts:  
                unique_posts.append(text)
                seen_posts.add(text)

        if not unique_posts:
            print(f"✅ Job Done.")
            break

        all_text.extend(unique_posts)
        print(f"✅ Loaded {len(unique_posts)} posts.")

        if len(unique_posts) < 50:
            print(f"✅ Thread end reached.")
            break

        last_post += 50 

    return "\n\n".join(all_text)


topic_id = 1107801  # offtop ver.18
start_from_post = 6000


forum_text = get_forum_text(topic_id, 200, start_from_post)

with open("I:\OT\\fresh\\raw.txt", "w", encoding="utf-8") as f:
    f.write(forum_text)

print("🎉 raw.txt saved.")
